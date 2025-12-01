import os
import sys
import platform
import time
import json
from datetime import datetime
from pathlib import Path

def print_header():
    """Выводит заголовок программы"""
    print("🌙 Спящий режим для продуктов NeoDark")
    print("=" * 50)

def get_neodark_banner():
    """Возвращает баннер NeoDark"""
    return [
        "███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗",
        "████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝",
        "██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ ",
        "██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ ",
        "██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗",
        "╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝"
    ]

def show_neodark_logo():
    """Показывает логотип NeoDark"""
    banner = get_neodark_banner()
    for line in banner:
        print(f"\033[96m{line}\033[0m")
    print()

def list_products():
    """Получает список продуктов"""
    # Симуляция списка продуктов
    products = [
        {
            "id": "neodark-core",
            "name": "NeoDark Core",
            "version": "1.2.5",
            "status": "active",
            "last_activity": "2023-12-07 14:30:22"
        },
        {
            "id": "neodark-security",
            "name": "NeoDark Security Suite",
            "version": "3.0.1",
            "status": "active",
            "last_activity": "2023-12-07 10:15:45"
        },
        {
            "id": "neodark-media",
            "name": "NeoDark Media Pack",
            "version": "2.4.0",
            "status": "active",
            "last_activity": "2023-12-06 09:22:18"
        },
        {
            "id": "neodark-devtools",
            "name": "NeoDark Developer Tools",
            "version": "1.0.0",
            "status": "active",
            "last_activity": "2023-12-05 16:45:33"
        }
    ]
    
    return products

def display_products(products):
    """Отображает список продуктов"""
    print("📦 Доступные продукты:")
    print("-" * 60)
    
    for i, product in enumerate(products, 1):
        status_icon = "🟢" if product['status'] == 'active' else "🔴"
        print(f" [{i}] {status_icon} {product['name']} (v{product['version']})")
        print(f"     ID: {product['id']}")
        print(f"     Последняя активность: {product['last_activity']}")
        print()

def select_products_for_sleep(products):
    """Позволяет пользователю выбрать продукты для перевода в спящий режим"""
    print("Выберите продукты для перевода в спящий режим:")
    print(" Введите номера продуктов через пробел (например: 1 3)")
    print(" Или 'all' для выбора всех продуктов")
    print()
    
    choice = input("Ваш выбор: ").strip()
    
    if choice.lower() == 'all':
        return products
    
    try:
        selected_indices = [int(x) - 1 for x in choice.split()]
        selected_products = [products[i] for i in selected_indices if 0 <= i < len(products)]
        return selected_products
    except ValueError:
        print("❌ Неверный формат ввода")
        return []

def put_products_to_sleep(selected_products):
    """Переводит выбранные продукты в спящий режим"""
    print("\n🌙 Перевод продуктов в спящий режим...")
    print("-" * 50)
    
    sleep_log = []
    
    for product in selected_products:
        print(f"   Перевод {product['name']} в спящий режим...")
        
        # Симуляция процесса перевода в спящий режим
        time.sleep(0.5)
        
        # Обновляем статус продукта
        product['status'] = 'sleeping'
        product['sleep_start'] = datetime.now().isoformat()
        
        print(f"   ✅ {product['name']} переведен в спящий режим")
        
        # Добавляем запись в лог
        sleep_log.append({
            'product_id': product['id'],
            'product_name': product['name'],
            'sleep_start': product['sleep_start'],
            'timestamp': datetime.now().isoformat()
        })
    
    return sleep_log

def save_sleep_log(sleep_log):
    """Сохраняет лог спящего режима"""
    try:
        # Создаем директорию для логов если её нет
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Сохраняем лог
        log_file = log_dir / f"sleep_mode_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(sleep_log, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Лог спящего режима сохранен: {log_file}")
        return True
    except Exception as e:
        print(f"\n❌ Ошибка сохранения лога: {e}")
        return False

def show_sleep_info():
    """Показывает информацию о спящем режиме"""
    print("\nℹ️  Что такое спящий режим продуктов:")
    print("   Спящий режим позволяет временно отключить продукты,")
    print("   чтобы сэкономить ресурсы системы и повысить безопасность.")
    print()
    print("💡 Преимущества:")
    print("   • Экономия системных ресурсов")
    print("   • Повышенная безопасность")
    print("   • Уменьшение фоновой активности")
    print()
    print("🛠️  Как вывести продукт из спящего режима:")
    print("   • Используйте функцию 'Запустить продукт' в главном меню")
    print("   • Перезапустите NeoDark")
    print("   • Вручную измените статус в конфигурации")

def show_current_sleep_status(products):
    """Показывает текущий статус спящего режима продуктов"""
    sleeping_products = [p for p in products if p['status'] == 'sleeping']
    
    if sleeping_products:
        print("\n😴 Продукты в спящем режиме:")
        print("-" * 40)
        for product in sleeping_products:
            sleep_start = datetime.fromisoformat(product['sleep_start'])
            elapsed = datetime.now() - sleep_start
            print(f"   {product['name']} (с {sleep_start.strftime('%H:%M:%S')})")
            print(f"   В спящем режиме: {str(elapsed).split('.')[0]}")
            print()
    else:
        print("\n🟢 Нет продуктов в спящем режиме")

def main():
    """Главная функция спящего режима"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем заголовок и логотип
    show_neodark_logo()
    print_header()
    
    try:
        # Получаем список продуктов
        products = list_products()
        
        # Показываем текущий статус спящего режима
        show_current_sleep_status(products)
        
        # Отображаем список продуктов
        display_products(products)
        
        # Выбираем продукты для спящего режима
        selected_products = select_products_for_sleep(products)
        
        if not selected_products:
            print("❌ Не выбрано ни одного продукта")
            input("\nНажмите Enter для выхода...")
            return
        
        # Переводим продукты в спящий режим
        sleep_log = put_products_to_sleep(selected_products)
        
        # Сохраняем лог
        if sleep_log:
            save_sleep_log(sleep_log)
        
        # Показываем информацию о спящем режиме
        show_sleep_info()
        
        print(f"\n🎉 Спящий режим успешно активирован!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Операция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()