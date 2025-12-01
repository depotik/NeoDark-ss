import os
import sys
import random
from datetime import datetime

def print_header():
    """Выводит заголовок программы"""
    print("🔒 Блокировка/Разблокировка продуктов")
    print("=" * 45)

def get_neodark_banner():
    """Возвращает баннер NeoDark"""
    return '''\033[96m███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ 
██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝\033[0m'''

def show_neodark_logo():
    """Показывает логотип NeoDark"""
    print(get_neodark_banner())
    print()

def get_neodark_products():
    """Получает список продуктов NeoDark (демо)"""
    print("📦 Получение списка продуктов...")
    
    products = [
        {
            "id": "neodark-core",
            "name": "NeoDark Core",
            "version": "1.2.5",
            "status": "active",
            "license": "valid"
        },
        {
            "id": "neodark-security",
            "name": "NeoDark Security Suite",
            "version": "3.0.1",
            "status": "active",
            "license": "valid"
        },
        {
            "id": "neodark-media",
            "name": "NeoDark Media Pack",
            "version": "2.4.0",
            "status": "active",
            "license": "valid"
        },
        {
            "id": "neodark-devtools",
            "name": "NeoDark Developer Tools",
            "version": "1.0.0",
            "status": "active",
            "license": "trial"
        },
        {
            "id": "neodark-cloud",
            "name": "NeoDark Cloud Services",
            "version": "2.1.3",
            "status": "blocked",
            "license": "expired"
        }
    ]
    
    return products

def display_products(products):
    """Отображает список продуктов"""
    print("\n📋 Продукты NeoDark:")
    print("-" * 50)
    
    status_icons = {
        "active": "🟢",
        "blocked": "🔴",
        "inactive": "⚪"
    }
    
    license_icons = {
        "valid": "✅",
        "trial": "⏳",
        "expired": "❌"
    }
    
    for i, product in enumerate(products, 1):
        status_icon = status_icons.get(product['status'], "❓")
        license_icon = license_icons.get(product['license'], "❓")
        
        print(f"   {i}. {status_icon} {license_icon} {product['name']} (v{product['version']})")
        print(f"      ID: {product['id']}")
        print(f"      Статус: {product['status']}")
        print(f"      Лицензия: {product['license']}")
        print()

def block_product_demo(products):
    """Демонстрация блокировки продукта"""
    print("🔐 Блокировка продукта (демо):")
    print("-" * 35)
    
    try:
        # Выбор продукта для блокировки
        product_num = input("Введите номер продукта для блокировки (1-5): ").strip()
        
        if not product_num.isdigit() or not (1 <= int(product_num) <= len(products)):
            print("❌ Неверный номер продукта")
            return False
        
        product_index = int(product_num) - 1
        product = products[product_index]
        
        if product['status'] == 'blocked':
            print(f"⚠️ Продукт '{product['name']}' уже заблокирован")
            return False
        
        # Имитация блокировки
        print(f"🔒 Блокировка продукта '{product['name']}'...")
        
        import time
        steps = [
            "Проверка прав доступа",
            "Проверка лицензии",
            "Создание записи блокировки",
            "Обновление конфигурации",
            "Применение изменений"
        ]
        
        for i, step in enumerate(steps, 1):
            print(f"   [{i}/{len(steps)}] {step}...")
            time.sleep(0.5)
        
        # Обновляем статус продукта
        product['status'] = 'blocked'
        print(f"✅ Продукт '{product['name']}' успешно заблокирован")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка блокировки продукта: {e}")
        return False

def unblock_product_demo(products):
    """Демонстрация разблокировки продукта"""
    print("🔓 Разблокировка продукта (демо):")
    print("-" * 35)
    
    try:
        # Выбор продукта для разблокировки
        blocked_products = [p for p in products if p['status'] == 'blocked']
        if not blocked_products:
            print("✅ Нет заблокированных продуктов")
            return False
        
        print("Заблокированные продукты:")
        for i, product in enumerate(blocked_products, 1):
            print(f"   {i}. {product['name']}")
        
        product_num = input("Введите номер продукта для разблокировки: ").strip()
        
        if not product_num.isdigit() or not (1 <= int(product_num) <= len(blocked_products)):
            print("❌ Неверный номер продукта")
            return False
        
        product_index = int(product_num) - 1
        product = blocked_products[product_index]
        
        # Имитация разблокировки
        print(f"🔓 Разблокировка продукта '{product['name']}'...")
        
        import time
        steps = [
            "Проверка прав доступа",
            "Проверка лицензии",
            "Удаление записи блокировки",
            "Обновление конфигурации",
            "Применение изменений"
        ]
        
        for i, step in enumerate(steps, 1):
            print(f"   [{i}/{len(steps)}] {step}...")
            time.sleep(0.5)
        
        # Обновляем статус продукта
        product['status'] = 'active'
        print(f"✅ Продукт '{product['name']}' успешно разблокирован")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка разблокировки продукта: {e}")
        return False

def show_blocking_info():
    """Показывает информацию о блокировке продуктов"""
    print("\nℹ️ Информация о блокировке:")
    print("-" * 30)
    print("   Блокировка продуктов позволяет:")
    print("   • Ограничить доступ к функциям")
    print("   • Предотвратить использование")
    print("   • Защитить от несанкционированного доступа")
    print("   • Управлять лицензиями")
    print()
    print("   Причины блокировки:")
    print("   • Истечение срока лицензии")
    print("   • Нарушение условий использования")
    print("   • Подозрительная активность")
    print("   • Административные решения")

def main():
    """Главная функция блокировки/разблокировки продуктов"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Получаем список продуктов
        products = get_neodark_products()
        
        # Отображаем продукты
        display_products(products)
        
        # Показываем информацию
        show_blocking_info()
        
        # Меню действий
        print("\nВыберите действие:")
        print(" [1] Заблокировать продукт")
        print(" [2] Разблокировать продукт")
        print(" [0] Выход")
        print()
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            block_product_demo(products)
        elif choice == "2":
            unblock_product_demo(products)
        elif choice == "0":
            print("👋 Выход...")
        else:
            print("❌ Неверный выбор")
        
        print(f"\n✅ Работа завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Операция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()