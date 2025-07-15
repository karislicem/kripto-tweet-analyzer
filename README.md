# 🐦 Kripto Tweet Analyzer

Gemini AI ile kripto para ve airdrop tweet'lerini analiz eden modern web uygulaması. Streamlit ile güçlendirilmiş!

## ✨ Özellikler

- 🌐 **Modern Web Arayüzü**: Streamlit ile kullanıcı dostu interface
- 🔗 **Airdrop Odaklı**: Kripto para ve airdrop haberlerine özel analiz
- 🇹🇷🇺🇸 **Çok Dilli Destek**: Türkçe ve İngilizce analiz sonuçları
- 🎯 **Akıllı Özetleme**: Gemini AI ile kripto projelerini anlama
- 📊 **Görsel İstatistikler**: Plotly ile interaktif grafikler
- 💾 **Sonuç İndirme**: Analiz sonuçlarını dosya olarak indirme
- ⚡ **Yüksek Performans**: Büyük tweet verilerini parça parça işler
- 📤 **Drag & Drop**: Basit dosya yükleme sistemi

## 📋 Gereksinimler

- Python 3.7+
- Gemini API anahtarı ([Google AI Studio](https://makersuite.google.com/app/apikey)'dan alabilirsiniz)

## 🚀 Kurulum

### Yerel Kurulum:
1. **Projeyi klonlayın veya indirin**
2. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

3. **API anahtarını ayarlayın:**
   - `.env` dosyasını düzenleyin VEYA
   - Streamlit secrets kullanın: `.streamlit/secrets.toml` dosyası oluşturun
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

### 🌐 Streamlit Cloud'da Deploy:
1. **GitHub'a push yapın:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Streamlit Cloud'a gidin:**
   - https://share.streamlit.io/ adresini ziyaret edin
   - GitHub hesabınızla giriş yapın
   - "New app" butonuna tıklayın

3. **Repo ayarlarını yapın:**
   - Repository: `your-username/x_analyzer`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

4. **Secrets'ı güvenli şekilde ekleyin:**
   - Advanced settings > Secrets kısmına gidin
   - Şu formatı kullanın:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

5. **Deploy butonuna tıklayın!**

## 📊 Kullanım

### Web Uygulaması (Önerilen)
```bash
streamlit run app.py
```

### Komut Satırı (Hala Mevcut)
```bash
python main.py your_tweets.json --language both
```

### Web Arayüzü Özellikleri
- 📤 **Dosya Yükleme**: JSON dosyalarını sürükle-bırak
- ⚙️ **Ayarlar**: Dil seçimi, tweet sayısı, parça boyutu
- 📊 **Analiz Sonuçları**: Türkçe/İngilizce analiz görüntüleme
- 📈 **İstatistikler**: Interaktif grafikler ve tablolar
- 💾 **İndirme**: Analiz sonuçlarını TXT olarak indirme

### Komut Satırı Parametreleri

| Parametre | Kısayol | Varsayılan | Açıklama |
|-----------|---------|------------|----------|
| `--language` | `-l` | `both` | Analiz dili (turkish/english/both) |
| `--max-tweets` | `-m` | `50` | Maksimum analiz edilecek tweet sayısı |
| `--no-save` | - | `False` | Sonuçları dosyaya kaydetme |
| `--chunk-size` | `-c` | `10` | Tweet parça boyutu |

## 📁 JSON Dosya Formatı

Program aşağıdaki JSON formatını bekler:

```json
[
  {
    "username": "kullanici_adi",
    "text": "Tweet metni",
    "timestamp": "2025-07-15T21:50:49.000Z",
    "scraped_at": "2025-07-16T02:10:11.731943"
  }
]
```

## 📊 Analiz Sonuçları

Program her analiz için şunları sunar:

### Türkçe Analiz:
- **Genel Özet**: Tweet'lerin genel konularının özeti
- **Ana Temalar**: Öne çıkan ana temaların listesi
- **Duygusal Analiz**: Genel duygu durumunun analizi
- **Önemli Olaylar**: Bahsedilen önemli olayların listesi
- **Sonuç**: Genel değerlendirme ve öneriler

### English Analysis:
- **General Summary**: Summary of main topics
- **Key Themes**: List of prominent themes
- **Sentiment Analysis**: General sentiment evaluation
- **Important Events**: List of mentioned important events
- **Conclusion**: General evaluation and recommendations

## 📁 Çıktı Dosyaları

Sonuçlar `results/` klasörüne kaydedilir:
- `analiz_tr_[dosya_adı]_[tarih_saat].txt` - Türkçe analiz
- `analysis_en_[dosya_adı]_[tarih_saat].txt` - İngilizce analiz

## ⚙️ Yapılandırma

`config.py` dosyasından aşağıdaki ayarları değiştirebilirsiniz:

```python
class Config:
    GEMINI_MODEL = 'gemini-pro'           # Kullanılacak Gemini model
    MAX_TWEETS_PER_ANALYSIS = 50         # Maksimum tweet sayısı
    CHUNK_SIZE = 10                      # Tweet parça boyutu
    OUTPUT_FORMAT = 'both'               # Çıktı formatı
    SAVE_RESULTS = True                  # Sonuçları kaydet
    RESULTS_DIR = 'results'              # Sonuçlar dizini
```

## 🔧 Sorun Giderme

### Yaygın Hatalar:

1. **GEMINI_API_KEY bulunamadı**
   - `.env` dosyasında API anahtarınızı doğru ayarladığınızdan emin olun

2. **Dosya bulunamadı**
   - JSON dosyanızın doğru yolda olduğundan emin olun

3. **JSON dosyası bozuk**
   - JSON dosyanızın geçerli bir format olduğundan emin olun

4. **Analiz hatası**
   - İnternet bağlantınızı kontrol edin
   - API anahtarınızın geçerli olduğundan emin olun

## 🎯 Örnekler

### Örnek Tweet JSON:
```json
[
  {
    "username": "bosunatiklama",
    "text": "Bu gece, Tekirdağ ve Çanakkale.",
    "timestamp": "2025-07-15T21:50:49.000Z",
    "scraped_at": "2025-07-16T02:10:11.731943"
  }
]
```

### Örnek Analiz Çıktısı:
```
📊 TWEET ANALİZ SONUÇLARI
📈 Analiz edilen tweet sayısı: 3
🕐 Analiz zamanı: 2025-07-16 15:30:45
════════════════════════════════════════════════════════════════════════════════

🇹🇷 TÜRKÇE ANALİZ
┌─────────────────────────────────────────────────────────────────────────────┐
│ GENEL ÖZET:                                                                │
│ Tweet'ler Tekirdağ ve Çanakkale'deki yangın olayları ile ilgili...         │
│                                                                            │
│ ANA TEMALAR:                                                               │
│ • Doğal afetler (yangın)                                                  │
│ • Siyasi tartışmalar                                                      │
│ • Bölgesel haberler                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🤝 Katkıda Bulunma

Bu proje açık kaynak kodludur. Katkılarınızı bekliyoruz!

## 📜 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🔗 Bağlantılar

- [Gemini API Dokümantasyonu](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/app/apikey)
- [Rich Kütüphanesi](https://rich.readthedocs.io/)

---

**Not**: Bu program, tweet verilerini analiz etmek için Gemini AI'yi kullanır. Lütfen Google'ın AI politikalarına uygun kullanım yapın. 

## 🔒 Güvenlik Garantileri

### API Anahtarınız TÜM GÜVENLİKTE:
- ✅ API anahtarı sadece Streamlit Cloud secrets'ta saklanır
- ✅ Secrets sadece app'in kendisi tarafından erişilebilir
- ✅ GitHub'a push edilmez (.gitignore ile korunur)
- ✅ Kullanıcılar API anahtarını göremez
- ✅ Streamlit Cloud SSL/TLS ile şifrelenmiş
- ✅ Logs'ta görünmez

### Streamlit Cloud Avantajları:
- 🌐 **Ücretsiz hosting** - Tamamen bedava
- 🔒 **Güvenli secrets** - API anahtarları korunur
- 🚀 **Otomatik deploy** - GitHub'a push = otomatik güncelleme
- 📈 **Sınırsız kullanım** - Herkes erişebilir
- 💾 **Kalıcı URL** - Değişmeyen link

## 🌍 Canlı Demo

Deploy ettikten sonra böyle bir URL alacaksınız:
```
https://your-app-name.streamlit.app/
```

Bu URL'yi herkesle paylaşabilirsiniz!

## 📊 Deploy Sonrası Özellikler

- 🔄 **Otomatik sync**: GitHub'a push = otomatik güncelleme
- 📱 **Mobile responsive**: Telefon/tablet uyumlu
- 🌍 **Global erişim**: Dünya genelinden erişilebilir
- 📈 **Analytics**: Streamlit Cloud'dan kullanım istatistikleri
- 🔒 **HTTPS**: Güvenli bağlantı
- ⚡ **Hızlı**: CDN ile optimize edilmiş

## 🚨 Önemli Notlar

1. **API anahtarı güvenliği**:
   - Asla GitHub'a push etmeyin
   - .gitignore kontrolü yapın
   - Sadece Streamlit secrets kullanın

2. **Kullanım limitleri**:
   - Gemini API'nin ücretsiz limitlerini unutmayın
   - Çok fazla kullanım olursa rate limiting olabilir

3. **Maintenance**:
   - Streamlit Cloud bazen restart yapabilir
   - Bu normal bir durumdur, endişelenmeyın

## 📞 Destek

Deploy sırasında sorun yaşarsanız:
- Streamlit Community: https://discuss.streamlit.io/
- GitHub Issues: Repo'da issue açın
- Streamlit Docs: https://docs.streamlit.io/

---

**🎉 Artık kripto tweet'lerinizi dünya genelinde analiz edebilirsiniz!** 