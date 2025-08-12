#!/usr/bin/env python3
"""
Google Docs Reader - Example Usage

Bu dosya, Google Docs Reader'ın programmatik olarak nasıl kullanılacağını gösterir.
"""

import os
import json
from google_docs.chat_interface import run_documents_chat
from google_docs.embedding_method import GoogleDriveEmbeddingMethod

def example_single_document():
    """Tek bir Google Docs belgesini okuma örneği"""
    print("=== Tek Belge Okuma Örneği ===")
    
    # Credentials dosyasının var olduğunu kontrol et
    if not os.path.exists("credentials.json"):
        print("❌ credentials.json dosyası bulunamadı!")
        print("Lütfen Google Service Account credentials dosyanızı 'credentials.json' olarak kaydedin.")
        return
    
    # Örnek document ID (gerçek bir ID ile değiştirin)
    document_id = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    
    print(f"📄 Belge okunuyor: {document_id}")
    
    try:
        # Belgeyi oku
        content = run_documents_chat(document_id)
        
        if content and not content.startswith("API error") and not content.startswith("An error"):
            print("✅ Belge başarıyla okundu!")
            print(f"📊 İçerik uzunluğu: {len(content)} karakter")
            print(f"📖 İlk 200 karakter: {content[:200]}...")
        else:
            print("❌ Belge okunamadı:", content)
            
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

def example_folder_documents():
    """Google Drive klasöründeki belgeleri okuma örneği"""
    print("\n=== Klasör Belgeleri Okuma Örneği ===")
    
    # Credentials dosyasının var olduğunu kontrol et
    if not os.path.exists("credentials.json"):
        print("❌ credentials.json dosyası bulunamadı!")
        return
    
    # Örnek folder ID (gerçek bir ID ile değiştirin)
    folder_id = "your-folder-id-here"
    
    print(f"📁 Klasör okunuyor: {folder_id}")
    
    try:
        # Embedding method ile klasör belgeleri oku
        embedding_method = GoogleDriveEmbeddingMethod(folder_id)
        documents = embedding_method.get_documents()
        
        if documents:
            print(f"✅ {len(documents)} belge bulundu!")
            
            for i, doc in enumerate(documents, 1):
                title = doc.metadata.get('title', 'Başlıksız')
                content_length = len(doc.text)
                
                print(f"{i}. 📄 {title}")
                print(f"   📊 İçerik uzunluğu: {content_length} karakter")
                print(f"   📖 İlk 100 karakter: {doc.text[:100]}...")
                print()
        else:
            print("❌ Klasörde belge bulunamadı veya erişim sorunu.")
            
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

def validate_credentials():
    """Credentials dosyasını doğrula"""
    print("=== Credentials Doğrulama ===")
    
    if not os.path.exists("credentials.json"):
        print("❌ credentials.json dosyası bulunamadı!")
        print("\n📝 Credentials dosyası oluşturmak için:")
        print("1. Google Cloud Console'a gidin")
        print("2. Service Account oluşturun")
        print("3. JSON key dosyasını indirin")
        print("4. Dosyayı 'credentials.json' olarak kaydedin")
        return False
    
    try:
        with open("credentials.json", "r", encoding="utf-8") as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in creds]
        
        if missing_fields:
            print(f"❌ Eksik alanlar: {', '.join(missing_fields)}")
            return False
        
        if creds.get('type') != 'service_account':
            print("❌ Credentials tipi 'service_account' olmalıdır")
            return False
        
        print("✅ Credentials dosyası geçerli!")
        print(f"📧 Service Account: {creds['client_email']}")
        print(f"🏗️ Proje ID: {creds['project_id']}")
        return True
        
    except json.JSONDecodeError:
        print("❌ Credentials dosyası geçerli JSON formatında değil!")
        return False
    except Exception as e:
        print(f"❌ Credentials doğrulama hatası: {e}")
        return False

def main():
    """Ana örnek fonksiyonu"""
    print("🚀 Google Docs Reader - Örnek Kullanım\n")
    
    # Credentials'ı doğrula
    if not validate_credentials():
        return
    
    print("\n" + "="*50)
    
    # Tek belge okuma örneği
    example_single_document()
    
    # Klasör okuma örneği (isteğe bağlı)
    # example_folder_documents()

if __name__ == "__main__":
    main()