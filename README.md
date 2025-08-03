# Google Docs File Reader

Bu proje, LLM işlevselliği veya API anahtarları gerektirmeden Google Docs'tan belgeleri okumak ve indekslemek için tasarlanmıştır.

## 🚀 Özellikler

- Google API'sini kullanarak Google Docs'tan belgeleri okuma.
- Belgeleri verimli bir şekilde geri almak için indeksleme.
- LLM bağımlılıkları olmadan basitleştirilmiş kurulum.

## 📋 Gereksinimler

- Python 3.10 veya daha yenisi
- Streamlit
- Google API Python Client

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

## 📚 Kullanım

1. Google API kimlik bilgilerinizi `credentials.json` dosyasına ayarlayın.
2. Streamlit uygulamasını çalıştırın:
   ```bash
   streamlit run main.py
   ```
3. Okumak ve indekslemek için Google Belgesi Kimliğini girin.

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