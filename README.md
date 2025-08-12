# Google Docs Semantic Reader (LlamaIndex)

Bu uygulama:
1. GoogleDocsReader (llama-index-readers-google) ile 1+ Google Doc ID okur.
2. HuggingFaceEmbedding (`all-MiniLM-L6-v2`) ile embedding üretir (API key gereksiz).
3. VectorStoreIndex oluşturur.
4. QueryEngine üzerinden semantik arama ve kaynak chunk gösterir.

## Kurulum
```bash
pip install -r requirements.txt
streamlit run main.py
```

## Credentials
- Google Cloud Console → Docs API enable
- Service Account → JSON key indir
- JSON içeriğini uygulamada sol sidebar'a yapıştır
- Belge(ler)i Service Account e-postası ile paylaş (Reader izni)

## Kullanım
1. Doc ID'leri (her satıra bir ID) gir → Load & Index
2. Sorgu kutusuna arama / soru yaz → Search

