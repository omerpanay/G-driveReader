# Google Docs File Reader

Bu proje, LLM işlevselliği veya API anahtarları gerektirmeden Google Docs'tan belgeleri okumak ve indekslemek için tasarlanmıştır.

## 🚀 Özellikler

- Google API'sini kullanarak Google Docs'tan belgeleri okuma
- Belge içeriğini görüntüleme ve analiz etme
- Streamlit tabanlı kullanıcı dostu arayüz
- LLM bağımlılıkları olmadan basitleştirilmiş kurulum
- Güvenli credential yönetimi

## 📋 Gereksinimler

- Python 3.10 veya daha yenisi
- Streamlit
- Google API Python Client
- Google Cloud hesabı ve Service Account

## 🛠️ Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/omerpanay/G-driveReader.git
   ```
2. Proje dizinine gidin:
   ```bash
   cd G-driveReader
   ```
3. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Google Cloud Kurulumu

1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin
2. Yeni bir proje oluşturun veya mevcut bir projeyi seçin
3. **Google Docs API**'sini etkinleştirin:
   - "APIs & Services" > "Library" bölümüne gidin
   - "Google Docs API" aratın ve etkinleştirin
4. **Service Account** oluşturun:
   - "APIs & Services" > "Credentials" bölümüne gidin
   - "Create Credentials" > "Service Account" seçin
   - Service Account ismini girin ve oluşturun
5. **JSON Key** dosyasını indirin:
   - Oluşturulan Service Account'a tıklayın
   - "Keys" sekmesine gidin
   - "Add Key" > "Create new key" > "JSON" seçin
   - Dosyayı indirin

## 📚 Kullanım

1. Streamlit uygulamasını çalıştırın:
   ```bash
   streamlit run main.py
   ```

2. Tarayıcınızda açılan uygulamada:
   - Sol panelden JSON credentials dosyanızın içeriğini yapıştırın
   - Google Docs belgenizin ID'sini girin
   - "Belgeyi Oku" butonuna tıklayın

### Google Docs ID'si nasıl bulunur?

Google Docs URL'sinde `/d/` ve `/edit` arasındaki kısım document ID'sidir:
```
https://docs.google.com/document/d/[DOCUMENT_ID]/edit
```

Örnek:
```
https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
```
Bu örnekte document ID: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

## 🔒 Güvenlik

- Credentials dosyası geçici olarak yerel dizinde saklanır
- Uygulama kapatıldığında credentials dosyası otomatik olarak temizlenir
- Service Account sadece okuma yetkisine sahip olmalıdır

## 🚀 Gelişmiş Özellikler

### Programmatik Kullanım

```python
from google_docs.chat_interface import run_documents_chat

# Belge okuma
document_id = "your-document-id-here"
content = run_documents_chat(document_id)
print(content)
```

### Google Drive Klasöründen Çoklu Belge Okuma

```python
from google_docs.embedding_method import GoogleDriveEmbeddingMethod

# Drive klasöründen belgeleri oku
folder_id = "your-folder-id-here"
embedding_method = GoogleDriveEmbeddingMethod(folder_id)
documents = embedding_method.get_documents()

for doc in documents:
    print(f"Belge: {doc.metadata['title']}")
    print(f"İçerik: {doc.text[:100]}...")
```

## 🐛 Sorun Giderme

### Yaygın Hatalar

1. **"API error occurred: 403"**
   - Google Docs API'sinin etkinleştirildiğinden emin olun
   - Service Account'un doğru yetkilere sahip olduğunu kontrol edin

2. **"Document not found"**
   - Document ID'sinin doğru olduğunu kontrol edin
   - Belgenin herkese açık veya Service Account ile paylaşıldığından emin olun

3. **"Invalid credentials"**
   - JSON dosyasının doğru formatda olduğunu kontrol edin
   - Service Account JSON key dosyasını kullandığınızdan emin olun

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

## 🔄 Changelog

### v1.1.0 (Mevcut)
- ✅ Import hatalarını düzeltildi
- ✅ LlamaIndex bağımlılığı kaldırıldı
- ✅ Gelişmiş hata yakalama eklendi
- ✅ Credential doğrulama eklendi
- ✅ Türkçe kullanıcı arayüzü
- ✅ Detaylı dokümantasyon

### v1.0.0 (Başlangıç)
- ✅ Temel Google Docs okuma işlevselliği
- ✅ Streamlit arayüzü