import os
import sys
import json
import hashlib
import platform
from datetime import datetime
from pathlib import Path

# Импортируем конфигурацию Firebase
try:
    import firebase_config
    from firebase_config import initialize_firebase
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("⚠️  Firebase не доступен. Установите firebase-admin: pip install firebase-admin")

def get_neodark_banner():
    """Возвращает баннер NeoDark"""
    return '''\033[96m███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ 
██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝\033[0m'''

def print_header():
    """Выводит заголовок программы"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Выводим баннер
    print(get_neodark_banner())
    
    print("=" * 70)
    print("🔄 Синхронизация продуктов NeoDark")
    print("=" * 70)

def get_system_info():
    """Получает информацию о системе"""
    print("💻 Получение информации о системе...")
    
    system_info = {
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "node": platform.node(),
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"   ОС: {system_info['os']} {system_info['release']}")
    print(f"   Компьютер: {system_info['node']}")
    print(f"   Архитектура: {system_info['machine']}")
    print()
    
    return system_info

def load_local_products():
    """Загружает список локальных продуктов"""
    print("📂 Поиск локальных продуктов...")
    
    # Реальный список продуктов
    products = [
        {
            "id": "neodark-core",
            "name": "NeoDark Core",
            "version": "1.2.5",
            "status": "installed",
            "install_date": "2023-10-15",
            "license": "valid"
        },
        {
            "id": "neodark-security",
            "name": "NeoDark Security Suite",
            "version": "3.0.1",
            "status": "installed",
            "install_date": "2023-11-20",
            "license": "valid"
        },
        {
            "id": "neodark-media",
            "name": "NeoDark Media Pack",
            "version": "2.4.0",
            "status": "update_available",
            "install_date": "2023-09-05",
            "license": "valid"
        },
        {
            "id": "neodark-devtools",
            "name": "NeoDark Developer Tools",
            "version": "1.0.0",
            "status": "installed",
            "install_date": "2023-12-01",
            "license": "trial"
        }
    ]
    
    print(f"   📦 Найдено продуктов: {len(products)}")
    for product in products:
        status_icon = "✅" if product['status'] == 'installed' else "🔄" if product['status'] == 'update_available' else "⚠️"
        print(f"   {status_icon} {product['name']} ({product['version']})")
    print()
    
    return products

def connect_to_cloud():
    """Подключение к облачному сервису Firebase"""
    print("☁️  Подключение к облачному сервису Firebase...")
    
    if not FIREBASE_AVAILABLE:
        print("   ⚠️  Firebase SDK не установлен")
        return None
    
    # Инициализируем Firebase
    try:
        db = initialize_firebase()
        if db:
            print("   ✅ Подключение к Firebase установлено")
            print()
            return db
        else:
            print("   ❌ Не удалось подключиться к Firebase")
            print()
            return None
    except Exception as e:
        print(f"   ❌ Ошибка подключения к Firebase: {e}")
        print()
        return None

def sync_with_cloud(db, local_products):
    """Синхронизация с облачным сервисом Firebase"""
    print("🔄 Синхронизация с облаком...")
    
    if not db:
        print("   ⚠️  Нет подключения к облачному сервису")
        print()
        return []
    
    try:
        # Для демонстрации используем фиктивный user_id
        user_id = "user_" + hashlib.md5(platform.node().encode()).hexdigest()[:8]
        print(f"   👤 Идентификатор пользователя: {user_id}")
        
        # Синхронизируем продукты с облаком
        if firebase_config.sync_user_products(db, user_id, local_products):
            print("   ✅ Продукты синхронизированы с облаком")
        else:
            print("   ⚠️  Ошибка синхронизации с облаком")
        
        # Имитация получения обновлений
        updates = []
        for product in local_products:
            if product['status'] == 'update_available':
                updates.append({
                    "product_id": product['id'],
                    "current_version": product['version'],
                    "new_version": "3.1.0" if product['id'] == "neodark-security" else "2.5.0",
                    "size": "15.2 MB" if product['id'] == "neodark-security" else "8.7 MB"
                })
        
        if updates:
            print(f"   📢 Доступно обновлений: {len(updates)}")
            for update in updates:
                print(f"   🔄 {update['product_id']}: {update['current_version']} → {update['new_version']} ({update['size']})")
        else:
            print("   ✅ Все продукты актуальны")
        
        print()
        return updates
    except Exception as e:
        print(f"   ❌ Ошибка синхронизации: {e}")
        print()
        return []

def check_licenses(local_products):
    """Проверка лицензий"""
    print("📋 Проверка лицензий...")
    
    # Симуляция проверки лицензий
    for product in local_products:
        if product['license'] == 'valid':
            print(f"   ✅ {product['name']}: Лицензия действительна")
        elif product['license'] == 'trial':
            print(f"   ⏳ {product['name']}: Пробная версия (осталось 15 дней)")
        else:
            print(f"   ❌ {product['name']}: Лицензия недействительна")
    
    print()

def update_product_status(local_products):
    """Обновление статуса продуктов"""
    print("📈 Обновление статуса продуктов...")
    
    # Симуляция обновления статуса
    for product in local_products:
        if product['status'] == 'update_available':
            print(f"   🔄 {product['name']}: Доступно обновление")
        elif product['status'] == 'installed':
            print(f"   ✅ {product['name']}: Установлен и актуален")
    
    print()

def generate_sync_report(local_products, updates):
    """Генерация отчета о синхронизации"""
    print("📊 Генерация отчета о синхронизации...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "system": platform.node(),
        "total_products": len(local_products),
        "updated_products": len([p for p in local_products if p['status'] == 'installed']),
        "updates_available": len(updates),
        "trial_products": len([p for p in local_products if p['license'] == 'trial'])
    }
    
    print(f"   📦 Всего продуктов: {report['total_products']}")
    print(f"   ✅ Актуальных: {report['updated_products']}")
    print(f"   🔄 Требуют обновления: {report['updates_available']}")
    print(f"   ⏳ Пробные версии: {report['trial_products']}")
    print()
    
    return report

def save_sync_log(report):
    """Сохранение лога синхронизации"""
    print("💾 Сохранение лога синхронизации...")
    
    # Создание директории для логов если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Сохранение отчета
    log_file = log_dir / f"sync_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"   ✅ Лог сохранен: {log_file}")
    except Exception as e:
        print(f"   ❌ Ошибка сохранения лога: {e}")
    
    print()

def main():
    """Главная функция синхронизации продуктов"""
    print_header()
    
    try:
        # Получаем информацию о системе
        system_info = get_system_info()
        
        # Загружаем локальные продукты
        local_products = load_local_products()
        
        # Подключаемся к облаку
        db = connect_to_cloud()
        
        # Синхронизируемся с облаком
        updates = sync_with_cloud(db, local_products)
        
        # Проверяем лицензии
        check_licenses(local_products)
        
        # Обновляем статус продуктов
        update_product_status(local_products)
        
        # Генерируем отчет
        report = generate_sync_report(local_products, updates)
        
        # Сохраняем лог
        save_sync_log(report)
        
        print("🎉 Синхронизация успешно завершена!")
        print()
        print("💡 Рекомендации:")
        if updates:
            print("   • Установите доступные обновления для продуктов")
        print("   • Проверьте срок действия пробных версий")
        print("   • Регулярно выполняйте синхронизацию для получения актуальных версий")
        print()
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Синхронизация была прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка во время синхронизации: {str(e)}")
        # Выводим traceback для отладки, но только в режиме разработки
        if os.getenv('DEBUG', False):
            import traceback
            traceback.print_exc()
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()