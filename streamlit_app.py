import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import tempfile
import zipfile
from io import BytesIO
from analyzer import TweetAnalyzer
from config import Config

# Page config
st.set_page_config(
    page_title="🐦 Kripto Tweet Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .upload-section {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    .results-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'tweet_data' not in st.session_state:
        st.session_state.tweet_data = None

def setup_analyzer():
    """Setup the tweet analyzer"""
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY bulunamadı! Lütfen yöneticiye başvurun.")
        return None
    
    # Set environment variable for the analyzer
    os.environ["GEMINI_API_KEY"] = api_key
    
    try:
        analyzer = TweetAnalyzer()
        return analyzer
    except Exception as e:
        st.error(f"❌ Analyzer başlatılamadı: {str(e)}")
        return None

def load_tweets_from_json(file_content):
    """Load tweets from JSON file content"""
    try:
        tweets = json.loads(file_content)
        return tweets
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON dosyası geçersiz: {str(e)}")
        return None

def create_tweet_dataframe(tweets):
    """Create a pandas DataFrame from tweets"""
    if not tweets:
        return None
    
    df_data = []
    for tweet in tweets:
        df_data.append({
            'Kullanıcı': tweet.get('username', 'Bilinmeyen'),
            'Tweet': tweet.get('text', '')[:100] + '...' if len(tweet.get('text', '')) > 100 else tweet.get('text', ''),
            'Tarih': tweet.get('timestamp', 'Bilinmeyen'),
            'Karakter Sayısı': len(tweet.get('text', ''))
        })
    
    return pd.DataFrame(df_data)

def create_tweet_stats(tweets):
    """Create statistics and visualizations from tweets"""
    if not tweets:
        return None
    
    # Basic stats
    total_tweets = len(tweets)
    unique_users = len(set(tweet.get('username', '') for tweet in tweets))
    
    # Character count distribution
    char_counts = [len(tweet.get('text', '')) for tweet in tweets]
    
    # User distribution
    users = [tweet.get('username', 'Bilinmeyen') for tweet in tweets]
    user_counts = pd.Series(users).value_counts()
    
    return {
        'total_tweets': total_tweets,
        'unique_users': unique_users,
        'char_counts': char_counts,
        'user_counts': user_counts
    }

def create_download_file(results, filename, tweet_count):
    """Create downloadable file with results"""
    content = f"""KRIPTO TWEET ANALİZ SONUÇLARI
{"="*50}
Analiz Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Tweet Sayısı: {tweet_count}
{"="*50}

"""
    
    if 'turkish' in results:
        content += f"""🇹🇷 TÜRKÇE ANALİZ
{"-"*30}
{results['turkish']}

"""
    
    if 'english' in results:
        content += f"""🇺🇸 ENGLISH ANALYSIS
{"-"*30}
{results['english']}

"""
    
    return content

def main():
    """Main Streamlit application"""
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🐦 Kripto Tweet Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### 🚀 Gemini AI ile Kripto Tweet Analizi ve Airdrop Haberleri")
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <strong>📖 Nasıl Kullanılır:</strong><br>
        1. X scraper'ınızdan elde ettiğiniz JSON dosyasını yükleyin<br>
        2. Analiz ayarlarını yapın (dil, tweet sayısı)<br>
        3. Analizi başlatın ve sonuçları görüntüleyin<br>
        4. Sonuçları TXT dosyası olarak indirin
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Ayarlar")
        
        # Language selection
        language = st.selectbox(
            "📝 Analiz Dili",
            options=['both', 'turkish', 'english'],
            index=0,
            format_func=lambda x: {
                'both': '🌍 Her İki Dil',
                'turkish': '🇹🇷 Türkçe',
                'english': '🇺🇸 English'
            }[x]
        )
        
        # Analysis options
        st.subheader("🔧 Analiz Seçenekleri")
        max_tweets = st.slider("Maksimum Tweet Sayısı", 10, 200, 50)
        chunk_size = st.slider("İşlem Parça Boyutu", 5, 20, 10)
        
        # API Key status
        st.subheader("🔑 API Durumu")
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key:
            st.success("✅ API anahtarı mevcut")
        else:
            st.error("❌ API anahtarı bulunamadı")
        
        # Help section
        st.subheader("❓ Yardım")
        st.markdown("""
        **JSON Format:**
        ```json
        [
          {
            "username": "kullanici",
            "text": "tweet metni",
            "timestamp": "2025-01-16T10:30:00.000Z",
            "scraped_at": "2025-01-16T10:35:00.000Z"
          }
        ]
        ```
        """)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📤 Dosya Yükleme", "📊 Analiz Sonuçları", "📈 İstatistikler"])
    
    with tab1:
        st.header("📁 JSON Dosya Yükleme")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Kripto tweet JSON dosyanızı yükleyin",
            type=['json'],
            help="X scraper'ınızdan elde ettiğiniz JSON dosyasını yükleyin"
        )
        
        if uploaded_file is not None:
            # Load tweets
            file_content = uploaded_file.read().decode('utf-8')
            tweets = load_tweets_from_json(file_content)
            
            if tweets:
                st.session_state.tweet_data = tweets
                st.success(f"✅ {len(tweets)} tweet başarıyla yüklendi!")
                
                # Show sample tweets
                if st.checkbox("📋 Örnek Tweet'leri Göster"):
                    df = create_tweet_dataframe(tweets[:5])
                    if df is not None:
                        st.dataframe(df, use_container_width=True)
                
                # Analysis button
                if st.button("🔍 Analizi Başlat", type="primary", use_container_width=True):
                    if not api_key:
                        st.error("⚠️ API anahtarı bulunamadı!")
                        return
                    
                    # Setup analyzer
                    analyzer = setup_analyzer()
                    if not analyzer:
                        return
                    
                    # Configure analyzer
                    analyzer.config.MAX_TWEETS_PER_ANALYSIS = max_tweets
                    analyzer.config.CHUNK_SIZE = chunk_size
                    analyzer.config.SAVE_RESULTS = False
                    
                    # Run analysis
                    with st.spinner("🔄 Analiz yapılıyor... Bu işlem birkaç dakika sürebilir."):
                        try:
                            results = analyzer.analyze_tweets(tweets, language)
                            
                            if 'error' not in results:
                                st.session_state.analysis_results = results
                                st.success("🎉 Analiz başarıyla tamamlandı!")
                                st.balloons()
                                # Auto-switch to results tab
                                st.rerun()
                            else:
                                st.error(f"❌ Analiz hatası: {results['error']}")
                                
                        except Exception as e:
                            st.error(f"❌ Beklenmeyen hata: {str(e)}")
    
    with tab2:
        st.header("📊 Analiz Sonuçları")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Turkish analysis
            if 'turkish' in results:
                st.subheader("🇹🇷 Türkçe Analiz")
                with st.expander("Detayları Göster", expanded=True):
                    st.markdown(results['turkish'])
            
            # English analysis
            if 'english' in results:
                st.subheader("🇺🇸 English Analysis")
                with st.expander("Show Details", expanded=True):
                    st.markdown(results['english'])
            
            # Download results
            st.subheader("💾 Sonuçları İndir")
            
            if st.session_state.tweet_data:
                download_content = create_download_file(
                    results, 
                    "analysis_results", 
                    len(st.session_state.tweet_data)
                )
                
                st.download_button(
                    label="📥 Analiz Sonuçlarını İndir",
                    data=download_content,
                    file_name=f"crypto_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.info("📝 Analiz sonucu bulunmuyor. Lütfen önce bir dosya yükleyip analiz yapın.")
    
    with tab3:
        st.header("📈 Tweet İstatistikleri")
        
        if st.session_state.tweet_data:
            tweets = st.session_state.tweet_data
            stats = create_tweet_stats(tweets)
            
            if stats:
                # Basic stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📊 Toplam Tweet", stats['total_tweets'])
                
                with col2:
                    st.metric("👥 Benzersiz Kullanıcı", stats['unique_users'])
                
                with col3:
                    avg_chars = sum(stats['char_counts']) / len(stats['char_counts'])
                    st.metric("📝 Ortalama Karakter", f"{avg_chars:.0f}")
                
                with col4:
                    st.metric("📏 Maksimum Karakter", max(stats['char_counts']))
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Karakter Sayısı Dağılımı")
                    if 'char_counts' in stats:
                        fig_chars = px.histogram(
                            x=stats['char_counts'],
                            nbins=20,
                            title="Tweet Karakter Sayısı Dağılımı"
                        )
                        fig_chars.update_layout(xaxis_title="Karakter Sayısı", yaxis_title="Tweet Sayısı")
                        st.plotly_chart(fig_chars, use_container_width=True)
                
                with col2:
                    st.subheader("👥 Kullanıcı Dağılımı")
                    if 'user_counts' in stats:
                        fig_users = px.pie(
                            values=stats['user_counts'].values,
                            names=stats['user_counts'].index,
                            title="Tweet'lerin Kullanıcılara Göre Dağılımı"
                        )
                        st.plotly_chart(fig_users, use_container_width=True)
                
                # Detailed table
                st.subheader("📋 Detaylı Tweet Tablosu")
                df = create_tweet_dataframe(tweets)
                if df is not None:
                    st.dataframe(df, use_container_width=True)
                
        else:
            st.info("📊 İstatistik göstermek için tweet verisi gerekli. Lütfen bir dosya yükleyin.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🚀 Kripto Tweet Analyzer | Powered by Gemini AI | Made with ❤️ in Turkey"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 