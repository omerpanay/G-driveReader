# 🤖 LlamaIndex Chat System

Bu uygulama, Google Drive ve Google Docs'tan veri çekerek LlamaIndex ile chat yapmanızı sağlar.

## 🚀 Özellikler

- **Google Drive Entegrasyonu**: PDF ve diğer dosyaları Google Drive'dan indirip indexleme
- **Google Docs Entegrasyonu**: Google Docs belgelerini doğrudan okuyup chat yapma
- **Güvenli Credentials Yönetimi**: Credentials dosyasını güvenli şekilde yükleme
- **Streamlit Arayüzü**: Kullanıcı dostu web arayüzü
- **Çoklu Veri Kaynağı**: Drive ve Docs arasında geçiş yapabilme
- **Python 3.11 Uyumluluğu**: Stabil Python sürümü ile uyumlu

## 📋 Gereksinimler

- Python 3.11 (Önerilen)
- Google Cloud Project
- Google Drive API ve Google Docs API etkinleştirilmiş
- Service Account credentials

## 🛠️ Kurulum

### 1. Repository'yi klonlayın
```bash
git clone <repository-url>
cd LlamaIndexing
```

### 2. Python 3.11'i kurun
```bash
# Windows için
winget install Python.Python.3.11

# veya https://www.python.org/downloads/ adresinden indirin
```

### 3. Virtual Environment oluşturun
```bash
# Python 3.11 ile virtual environment oluşturun
py -3.11 -m venv venv

# Virtual environment'ı aktifleştirin
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Gerekli paketleri yükleyin
   ```bash
   pip install -r requirements.txt
```

### 5. Google Cloud Setup
1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin
2. Yeni bir proje oluşturun veya mevcut projeyi seçin
3. Google Drive API ve Google Docs API'yi etkinleştirin
4. Service Account oluşturun
5. JSON key dosyasını indirin

## 🚀 Kullanım

### 1. Uygulamayı başlatın
   ```bash
   streamlit run main.py
   ```

### 2. Credentials yükleyin
- Sidebar'da "Upload your credentials.json file" bölümünden credentials dosyanızı yükleyin

### 3. Veri kaynağı seçin
- **Google Drive**: Folder ID girin ve PDF'leri indexleyin
- **Google Docs**: Document ID girin ve belgeleri okuyun

### 4. Chat yapın
- Sorularınızı sorun ve AI'dan cevaplar alın

## 📁 Proje Yapısı

```
LlamaIndexing/
├── main.py                 # Ana uygulama
├── requirements.txt        # Gerekli paketler
├── README.md              # Dokümantasyon
├── .gitignore             # Git ignore dosyası
├── google_drive/          # Google Drive modülü
│   ├── chat_interface.py  # Drive chat arayüzü
│   ├── embedding_method.py # Drive embedding metodu
│   └── downloader.py      # Dosya indirme
├── google_docs/           # Google Docs modülü
│   ├── chat_interface.py  # Docs chat arayüzü
│   ├── embedding_method.py # Docs embedding metodu
│   └── api_client.py      # API istemcisi
└── shared/                # Paylaşılan modüller
    ├── config.py          # Konfigürasyon
    ├── llama_utils.py     # LlamaIndex yardımcıları
    └── protocol.py        # Protokol tanımları
```

## 🔧 Konfigürasyon

### Environment Variables
```bash
# Google API Key (opsiyonel)
GOOGLE_API_KEY=your_api_key

# Google Application Credentials (otomatik ayarlanır)
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### Varsayılan Ayarlar
- **Drive Folder ID**: `1zyKR8R9SxhOmp4wCqTlojNb9SZMZJfkF`
- **Docs Document ID**: `1sJjoOHvUMwFX7q0iU8aUnOS4d6889QDT_YTernsJgAk`
- **Embedding Model**: `BAAI/bge-small-en-v1.5`
- **LLM Model**: `gemini-1.5-flash`

## 🛠️ Sorun Giderme

### Python Sürüm Sorunları
- Python 3.11 kullanın (Python 3.13'te uyumluluk sorunları olabilir)
- Virtual environment kullanarak izole edin

### Credentials Sorunları
- Service Account'un doğru izinlere sahip olduğundan emin olun
- JSON dosyasının geçerli olduğunu kontrol edin

### API Limitleri
- Google API limitlerini kontrol edin
- Rate limiting için bekleyin

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

Sorularınız için issue açın veya iletişime geçin. 