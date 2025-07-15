import json
import os
from datetime import datetime
from typing import List, Dict, Any
import google.generativeai as genai
# Rich imports - optional for terminal output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
from config import Config

class TweetAnalyzer:
    def __init__(self):
        self.config = Config()
        self.console = Console() if HAS_RICH else None
        self.setup_gemini()
        self.create_results_dir()
    
    def setup_gemini(self):
        """Gemini API'sini yapılandır"""
        if not self.config.GEMINI_API_KEY:
            msg = "❌ GEMINI_API_KEY bulunamadı! .env dosyasını kontrol edin."
            if self.console:
                self.console.print(f"[red]{msg}[/red]")
            else:
                print(msg)
            raise ValueError("GEMINI_API_KEY gerekli")
        
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.config.GEMINI_MODEL)
        msg = "✅ Gemini API başarıyla yapılandırıldı"
        if self.console:
            self.console.print(f"[green]{msg}[/green]")
        else:
            print(msg)
    
    def create_results_dir(self):
        """Sonuçlar dizinini oluştur"""
        if not os.path.exists(self.config.RESULTS_DIR):
            os.makedirs(self.config.RESULTS_DIR)
    
    def load_tweets(self, json_file: str) -> List[Dict[str, Any]]:
        """JSON dosyasından tweet verilerini yükle"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                tweets = json.load(f)
            msg = f"📁 {len(tweets)} tweet başarıyla yüklendi"
            if self.console:
                self.console.print(f"[green]{msg}[/green]")
            else:
                print(msg)
            return tweets
        except FileNotFoundError:
            msg = f"❌ Dosya bulunamadı: {json_file}"
            if self.console:
                self.console.print(f"[red]{msg}[/red]")
            else:
                print(msg)
            return []
        except json.JSONDecodeError:
            msg = f"❌ JSON dosyası bozuk: {json_file}"
            if self.console:
                self.console.print(f"[red]{msg}[/red]")
            else:
                print(msg)
            return []
    
    def format_tweets_for_analysis(self, tweets: List[Dict[str, Any]]) -> str:
        """Tweet verilerini analiz için formatla"""
        formatted_tweets = []
        for i, tweet in enumerate(tweets, 1):
            formatted_tweet = f"""
Tweet {i}:
Kullanıcı: {tweet.get('username', 'Bilinmeyen')}
Zaman: {tweet.get('timestamp', 'Bilinmeyen')}
Metin: {tweet.get('text', '')}
---
"""
            formatted_tweets.append(formatted_tweet)
        
        return '\n'.join(formatted_tweets)
    
    def chunk_tweets(self, tweets: List[Dict[str, Any]], chunk_size: int) -> List[List[Dict[str, Any]]]:
        """Tweet verilerini parçalara böl"""
        chunks = []
        for i in range(0, len(tweets), chunk_size):
            chunks.append(tweets[i:i + chunk_size])
        return chunks
    
    def analyze_tweets_chunk(self, tweets_chunk: List[Dict[str, Any]], language: str) -> str:
        """Tweet parçasını analiz et"""
        formatted_tweets = self.format_tweets_for_analysis(tweets_chunk)
        
        if language == 'turkish':
            prompt = self.config.ANALYSIS_PROMPT_TR.format(tweets=formatted_tweets)
        else:
            prompt = self.config.ANALYSIS_PROMPT_EN.format(tweets=formatted_tweets)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            msg = f"❌ Analiz hatası: {str(e)}"
            if self.console:
                self.console.print(f"[red]{msg}[/red]")
            else:
                print(msg)
            return f"Analiz yapılamadı: {str(e)}"
    
    def analyze_tweets(self, tweets: List[Dict[str, Any]], language: str = 'both') -> Dict[str, str]:
        """Tweet verilerini analiz et"""
        if not tweets:
            return {"error": "Analiz edilecek tweet bulunamadı"}
        
        # Tweet sayısını sınırla
        if len(tweets) > self.config.MAX_TWEETS_PER_ANALYSIS:
            tweets = tweets[:self.config.MAX_TWEETS_PER_ANALYSIS]
            self.console.print(f"⚠️ [yellow]Tweet sayısı {self.config.MAX_TWEETS_PER_ANALYSIS} ile sınırlandı[/yellow]")
        
        # Tweet verilerini parçalara böl
        tweet_chunks = self.chunk_tweets(tweets, self.config.CHUNK_SIZE)
        
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            
            if language in ['turkish', 'both']:
                task = progress.add_task("🔍 Türkçe analiz yapılıyor...", total=len(tweet_chunks))
                
                turkish_analyses = []
                for chunk in tweet_chunks:
                    analysis = self.analyze_tweets_chunk(chunk, 'turkish')
                    turkish_analyses.append(analysis)
                    progress.update(task, advance=1)
                
                # Parçaları birleştir
                results['turkish'] = self.combine_analyses(turkish_analyses, 'turkish')
            
            if language in ['english', 'both']:
                task = progress.add_task("🔍 İngilizce analiz yapılıyor...", total=len(tweet_chunks))
                
                english_analyses = []
                for chunk in tweet_chunks:
                    analysis = self.analyze_tweets_chunk(chunk, 'english')
                    english_analyses.append(analysis)
                    progress.update(task, advance=1)
                
                # Parçaları birleştir
                results['english'] = self.combine_analyses(english_analyses, 'english')
        
        return results
    
    def combine_analyses(self, analyses: List[str], language: str) -> str:
        """Parçalanmış analizleri birleştir"""
        if len(analyses) == 1:
            return analyses[0]
        
        # Eğer birden fazla parça varsa, bunları özetlesin
        combined_text = "\n\n".join(analyses)
        
        if language == 'turkish':
            summary_prompt = f"""
            Aşağıdaki Twitter analizi parçalarını tek bir kapsamlı analiz halinde birleştir:
            
            {combined_text}
            
            Lütfen tutarlı, organize ve özetlenmiş bir analiz sun.
            """
        else:
            summary_prompt = f"""
            Combine the following Twitter analysis parts into one comprehensive analysis:
            
            {combined_text}
            
            Please provide a consistent, organized and summarized analysis.
            """
        
        try:
            response = self.model.generate_content(summary_prompt)
            return response.text
        except Exception as e:
            self.console.print(f"❌ [red]Birleştirme hatası: {str(e)}[/red]")
            return combined_text
    
    def display_results(self, results: Dict[str, str], tweet_count: int):
        """Sonuçları güzel bir formatta göster"""
        self.console.print("\n" + "="*80)
        self.console.print(f"📊 [bold blue]TWEET ANALİZ SONUÇLARI[/bold blue]")
        self.console.print(f"📈 Analiz edilen tweet sayısı: {tweet_count}")
        self.console.print(f"🕐 Analiz zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.console.print("="*80)
        
        if 'turkish' in results:
            panel = Panel(
                results['turkish'],
                title="🇹🇷 TÜRKÇE ANALİZ",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print(panel)
        
        if 'english' in results:
            panel = Panel(
                results['english'],
                title="🇺🇸 ENGLISH ANALYSIS",
                border_style="blue",
                padding=(1, 2)
            )
            self.console.print(panel)
    
    def save_results(self, results: Dict[str, str], filename: str, tweet_count: int):
        """Sonuçları dosyaya kaydet"""
        if not self.config.SAVE_RESULTS:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        
        # Her dil için ayrı dosya
        if 'turkish' in results:
            turkish_filename = f"{self.config.RESULTS_DIR}/analiz_tr_{base_filename}_{timestamp}.txt"
            with open(turkish_filename, 'w', encoding='utf-8') as f:
                f.write(f"TWEET ANALİZ SONUÇLARI (TÜRKÇE)\n")
                f.write(f"="*50 + "\n")
                f.write(f"Kaynak dosya: {filename}\n")
                f.write(f"Analiz edilen tweet sayısı: {tweet_count}\n")
                f.write(f"Analiz zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"="*50 + "\n\n")
                f.write(results['turkish'])
            
            self.console.print(f"💾 [green]Türkçe analiz kaydedildi: {turkish_filename}[/green]")
        
        if 'english' in results:
            english_filename = f"{self.config.RESULTS_DIR}/analysis_en_{base_filename}_{timestamp}.txt"
            with open(english_filename, 'w', encoding='utf-8') as f:
                f.write(f"TWEET ANALYSIS RESULTS (ENGLISH)\n")
                f.write(f"="*50 + "\n")
                f.write(f"Source file: {filename}\n")
                f.write(f"Analyzed tweet count: {tweet_count}\n")
                f.write(f"Analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"="*50 + "\n\n")
                f.write(results['english'])
            
            self.console.print(f"💾 [green]English analysis saved: {english_filename}[/green]")
    
    def analyze_file(self, json_file: str, language: str = 'both'):
        """Dosyayı analiz et (ana metod)"""
        self.console.print(f"🚀 [bold]Tweet analizi başlatılıyor...[/bold]")
        
        # Tweet verilerini yükle
        tweets = self.load_tweets(json_file)
        if not tweets:
            return
        
        # Tweet verilerini analiz et
        results = self.analyze_tweets(tweets, language)
        
        if 'error' in results:
            self.console.print(f"❌ [red]{results['error']}[/red]")
            return
        
        # Sonuçları göster
        self.display_results(results, len(tweets))
        
        # Sonuçları kaydet
        self.save_results(results, json_file, len(tweets))
        
        self.console.print(f"\n✅ [green]Analiz tamamlandı![/green]") 