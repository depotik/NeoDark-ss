import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys
from pathlib import Path
import json

def initialize_firebase():
    """
    Инициализирует Firebase SDK с учетными данными.
    Возвращает клиент Firestore.
    """
    try:
        # Проверяем, инициализировано ли уже приложение Firebase
        if not firebase_admin._apps:
            # Попытка использовать учетные данные по умолчанию (для разработки)
            try:
                # При попытке инициализации с Application Default Credentials
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {
                    'projectId': 'neodark-project',  # Замените на ваш ID проекта
                })
                print("✅ Используются учетные данные по умолчанию")
            except ValueError:
                # Если ADC недоступны, проверяем наличие файла учетных данных
                cred_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
                if cred_file and os.path.exists(cred_file):
                    cred = credentials.Certificate(cred_file)
                    firebase_admin.initialize_app(cred, {
                        'projectId': 'neodark-project',  # Замените на ваш ID проекта
                    })
                    print("✅ Используются учетные данные из файла")
                else:
                    # В рабочей среде вы должны использовать правильный файл учетных данных
                    print("⚠️  Используются тестовые учетные данные Firebase")
                    # Создаем минимальную конфигурацию для разработки
                    firebase_admin.initialize_app()
        
        # Получаем клиент Firestore
        db = firestore.client()
        print("✅ Подключение к Firebase установлено")
        return db
    except Exception as e:
        print(f"❌ Ошибка инициализации Firebase: {e}")
        print("💡 Убедитесь, что вы установили firebase-admin: pip install firebase-admin")
        return None

def get_products_collection(db):
    """
    Получает коллекцию продуктов из Firestore.
    """
    try:
        if db is None:
            return None
        return db.collection('products')
    except Exception as e:
        print(f"❌ Ошибка получения коллекции продуктов: {e}")
        return None

def get_user_products_collection(db, user_id):
    """
    Получает коллекцию продуктов пользователя из Firestore.
    """
    try:
        if db is None or not user_id:
            return None
        return db.collection('users').document(user_id).collection('products')
    except Exception as e:
        print(f"❌ Ошибка получения коллекции продуктов пользователя: {e}")
        return None

def sync_user_products(db, user_id, local_products):
    """
    Синхронизирует локальные продукты с Firestore.
    """
    try:
        if db is None or not user_id:
            print("⚠️  Невозможно синхронизировать продукты: нет подключения к Firebase или ID пользователя")
            return False
            
        user_products_ref = get_user_products_collection(db, user_id)
        if user_products_ref is None:
            print("⚠️  Невозможно получить коллекцию продуктов пользователя")
            return False
            
        # Обновляем или создаем документы для каждого продукта
        for product in local_products:
            product_id = product.get('id')
            if product_id:
                # Добавляем метку времени
                product['last_sync'] = firestore.SERVER_TIMESTAMP
                
                # Сохраняем или обновляем документ
                user_products_ref.document(product_id).set(product)
                
        print("✅ Продукты успешно синхронизированы с облаком")
        return True
    except Exception as e:
        print(f"❌ Ошибка синхронизации продуктов: {e}")
        return False

def get_user_data(db, user_id):
    """
    Получает данные пользователя из Firestore.
    """
    try:
        if db is None or not user_id:
            return None
            
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            return user_doc.to_dict()
        else:
            return None
    except Exception as e:
        print(f"❌ Ошибка получения данных пользователя: {e}")
        return None

def update_user_data(db, user_id, data):
    """
    Обновляет данные пользователя в Firestore.
    """
    try:
        if db is None or not user_id or not data:
            print("⚠️  Невозможно обновить данные пользователя: недостаточно параметров")
            return False
            
        data['last_updated'] = firestore.SERVER_TIMESTAMP
        db.collection('users').document(user_id).set(data)
        print("✅ Данные пользователя обновлены")
        return True
    except Exception as e:
        print(f"❌ Ошибка обновления данных пользователя: {e}")
        return False

def get_all_user_products(db, user_id):
    """
    Получает все продукты пользователя из Firestore.
    """
    try:
        if db is None or not user_id:
            return []
            
        user_products_ref = get_user_products_collection(db, user_id)
        if user_products_ref is None:
            return []
            
        docs = user_products_ref.stream()
        products = []
        for doc in docs:
            product_data = doc.to_dict()
            product_data['id'] = doc.id
            products.append(product_data)
            
        return products
    except Exception as e:
        print(f"❌ Ошибка получения продуктов пользователя: {e}")
        return []

def delete_user_product(db, user_id, product_id):
    """
    Удаляет продукт пользователя из Firestore.
    """
    try:
        if db is None or not user_id or not product_id:
            print("⚠️  Невозможно удалить продукт: недостаточно параметров")
            return False
            
        user_products_ref = get_user_products_collection(db, user_id)
        if user_products_ref is None:
            return False
            
        user_products_ref.document(product_id).delete()
        print(f"✅ Продукт {product_id} удален")
        return True
    except Exception as e:
        print(f"❌ Ошибка удаления продукта: {e}")
        return False

# Тестовая функция для проверки подключения
def test_firebase_connection():
    """
    Тестовая функция для проверки подключения к Firebase.
    """
    print("🔍 Тестирование подключения к Firebase...")
    db = initialize_firebase()
    
    if db:
        try:
            # Простая операция чтения для проверки подключения
            docs = db.collection('test').limit(1).get()
            print("✅ Подключение к Firebase работает корректно")
            return True
        except Exception as e:
            print(f"⚠️  Подключение установлено, но возникла ошибка при тестировании: {e}")
            return True
    else:
        print("❌ Не удалось подключиться к Firebase")
        return False

if __name__ == "__main__":
    # Тестирование подключения
    test_firebase_connection()