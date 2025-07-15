#!/usr/bin/env python3
"""
X (Twitter) Tweet Analyzer
Gemini API kullanarak tweet verilerini analiz eden program
"""

import argparse
import sys
import os
from pathlib import Path
from analyzer import TweetAnalyzer

def main():
    parser = argparse.ArgumentParser(
        description='X (Twitter) Tweet Analyzer - Gemini API ile tweet analizi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python main.py latest_tweets.json                    # Her iki dilde analiz
  python main.py data.json --language turkish          # Sadece Türkçe
  python main.py data.json --language english          # Sadece İngilizce
  python main.py data.json --max-tweets 100            # Maksimum tweet sayısı
        """
    )
    
    parser.add_argument(
        'json_file',
        help='Analiz edilecek JSON dosyasının yolu'
    )
    
    parser.add_argument(
        '--language', '-l',
        choices=['turkish', 'english', 'both'],
        default='both',
        help='Analiz dili (varsayılan: both)'
    )
    
    parser.add_argument(
        '--max-tweets', '-m',
        type=int,
        default=50,
        help='Maksimum analiz edilecek tweet sayısı (varsayılan: 50)'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Sonuçları dosyaya kaydetme'
    )
    
    parser.add_argument(
        '--chunk-size', '-c',
        type=int,
        default=10,
        help='Tweet parça boyutu (varsayılan: 10)'
    )
    
    args = parser.parse_args()
    
    # Dosya kontrolü
    if not os.path.exists(args.json_file):
        print(f"❌ Hata: Dosya bulunamadı: {args.json_file}")
        sys.exit(1)
    
    # API anahtarı kontrolü
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ Hata: GEMINI_API_KEY çevre değişkeni bulunamadı!")
        print("Lütfen .env dosyasını oluşturun ve API anahtarınızı ekleyin:")
        print("GEMINI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    try:
        # Analyzer'ı başlat
        analyzer = TweetAnalyzer()
        
        # Ayarları güncelle
        analyzer.config.MAX_TWEETS_PER_ANALYSIS = args.max_tweets
        analyzer.config.CHUNK_SIZE = args.chunk_size
        analyzer.config.SAVE_RESULTS = not args.no_save
        
        # Analizi başlat
        analyzer.analyze_file(args.json_file, args.language)
        
    except KeyboardInterrupt:
        print("\n⚠️ Analiz kullanıcı tarafından durduruldu.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 