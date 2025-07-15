import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Gemini API ayarları
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    # Analiz ayarları
    MAX_TWEETS_PER_ANALYSIS = 50
    CHUNK_SIZE = 10
    
    # Çıktı ayarları
    OUTPUT_FORMAT = 'both'  # 'turkish', 'english', 'both'
    SAVE_RESULTS = True
    RESULTS_DIR = 'results'
    
    def __init__(self):
        self.MAX_TWEETS_PER_ANALYSIS = 50
        self.CHUNK_SIZE = 10
        self.SAVE_RESULTS = True
    
    # Prompt şablonları
    ANALYSIS_PROMPT_TR = """
    Aşağıdaki kripto para ve airdrop tweet verilerini analiz et ve Türkçe olarak şunları yap:
    
    1. GENEL ÖZET: Tweetlerin genel konularını ve bahsedilen projeleri özetle
    2. AIRDROP BİLGİLERİ: Bahsedilen airdrop'lar, tarihler, koşullar ve detaylar
    3. PROJE VE TOKEN BİLGİLERİ: Bahsedilen kripto projeler, token'lar ve özellikleri
    4. ÖNEMLİ DUYURULAR: Önemli açıklamalar, güncelleme ve haberler
    5. SONUÇ: Genel değerlendirme ve öneriler
    
    Tweet verileri:
    {tweets}
    
    Lütfen analizi kripto para yatırımcıları için yararlı olacak şekilde detaylı ve organize bir şekilde sun.
    """
    
    ANALYSIS_PROMPT_EN = """
    Analyze the following cryptocurrency and airdrop tweet data and provide in English:
    
    1. GENERAL SUMMARY: Summarize the main topics and projects mentioned in the tweets
    2. AIRDROP INFORMATION: List airdrops mentioned, dates, requirements and details
    3. PROJECT AND TOKEN INFO: Crypto projects, tokens and their features mentioned
    4. IMPORTANT ANNOUNCEMENTS: Key announcements, updates and news
    5. CONCLUSION: General evaluation and recommendations
    
    Tweet data:
    {tweets}
    
    Please provide a detailed and organized analysis that would be useful for crypto investors.
    """ 