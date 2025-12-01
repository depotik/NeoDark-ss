import os
import sys
import random
from datetime import datetime, timedelta

def print_header():
    """Выводит заголовок программы"""
    print("📜 Просмотр истории действий")
    print("=" * 40)

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

def generate_demo_history():
    """Генерирует демонстрационную историю действий"""
    print("🔍 Получение истории действий...")
    
    actions = [
        "Запуск программы",
        "Проверка обновлений",
        "Сканирование системы",
        "Очистка кэша",
        "Синхронизация с облаком",
        "Изменение настроек",
        "Установка продукта",
        "Удаление продукта",
        "Проверка лицензии",
        "Резервное копирование",
        "Восстановление из резервной копии",
        "Обновление продукта",
        "Проверка безопасности",
        "Оптимизация системы",
        "Анализ производительности"
    ]
    
    products = [
        "NeoDark Core",
        "NeoDark Security",
        "NeoDark Media",
        "NeoDark DevTools",
        "NeoDark Cloud"
    ]
    
    statuses = ["Успешно", "Ошибка", "Предупреждение", "В процессе"]
    
    history = []
    current_time = datetime.now()
    
    # Генерируем историю за последние 30 дней
    for i in range(50):
        action_time = current_time - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        history.append({
            "timestamp": action_time,
            "action": random.choice(actions),
            "product": random.choice(products) if random.choice([True, False]) else "Система",
            "status": random.choice(statuses),
            "details": f"Детали операции #{random.randint(1000, 9999)}"
        })
    
    # Сортируем по времени
    history.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return history

def display_history(history, page=1, per_page=10):
    """Отображает историю действий"""
    print(f"\n📋 История действий (страница {page}):")
    print("-" * 60)
    
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    page_history = history[start_index:end_index]
    
    status_icons = {
        "Успешно": "✅",
        "Ошибка": "❌",
        "Предупреждение": "⚠️",
        "В процессе": "🔄"
    }
    
    for i, record in enumerate(page_history, start_index + 1):
        icon = status_icons.get(record['status'], "⚪")
        timestamp = record['timestamp'].strftime("%Y-%m-%d %H:%M")
        
        print(f"   {i:2d}. {icon} [{timestamp}]")
        print(f"       {record['action']}")
        print(f"       Продукт: {record['product']}")
        print(f"       Статус: {record['status']}")
        print(f"       {record['details']}")
        print()

def show_history_statistics(history):
    """Показывает статистику истории"""
    print("📊 Статистика истории:")
    print("-" * 25)
    
    total_actions = len(history)
    successful_actions = len([h for h in history if h['status'] == 'Успешно'])
    failed_actions = len([h for h in history if h['status'] == 'Ошибка'])
    
    print(f"   Всего действий: {total_actions}")
    print(f"   Успешных: {successful_actions}")
    print(f"   С ошибками: {failed_actions}")
    
    # Самые частые действия
    action_counts = {}
    for record in history:
        action = record['action']
        action_counts[action] = action_counts.get(action, 0) + 1
    
    most_common = sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    print("\n   Самые частые действия:")
    for action, count in most_common:
        print(f"   • {action}: {count} раз")

def filter_history(history):
    """Фильтрация истории по критериям"""
    print("\n🔍 Фильтрация истории:")
    print("-" * 25)
    
    print("   Критерии фильтрации:")
    print("   [1] По дате")
    print("   [2] По продукту")
    print("   [3] По статусу")
    print("   [4] По типу действия")
    print()
    
    choice = input("Выберите критерий (1-4): ").strip()
    
    if choice == "1":
        date_str = input("Введите дату (ГГГГ-ММ-ДД): ").strip()
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            filtered = [h for h in history if h['timestamp'].date() == target_date.date()]
            print(f"   Найдено записей: {len(filtered)}")
            return filtered
        except ValueError:
            print("   ❌ Неверный формат даты")
            return history
    elif choice == "2":
        product = input("Введите название продукта: ").strip()
        filtered = [h for h in history if product.lower() in h['product'].lower()]
        print(f"   Найдено записей: {len(filtered)}")
        return filtered
    elif choice == "3":
        status = input("Введите статус: ").strip()
        filtered = [h for h in history if status.lower() in h['status'].lower()]
        print(f"   Найдено записей: {len(filtered)}")
        return filtered
    elif choice == "4":
        action = input("Введите тип действия: ").strip()
        filtered = [h for h in history if action.lower() in h['action'].lower()]
        print(f"   Найдено записей: {len(filtered)}")
        return filtered
    else:
        print("   ❌ Неверный выбор")
        return history

def main():
    """Главная функция просмотра истории действий"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Генерируем демонстрационную историю
        history = generate_demo_history()
        
        # Показываем статистику
        show_history_statistics(history)
        
        # Отображаем первую страницу истории
        current_page = 1
        per_page = 10
        total_pages = (len(history) + per_page - 1) // per_page
        
        while True:
            display_history(history, current_page, per_page)
            
            print(f"Страница {current_page} из {total_pages}")
            print("\nДействия:")
            print(" [N] Следующая страница")
            print(" [P] Предыдущая страница")
            print(" [F] Фильтровать")
            print(" [R] Сбросить фильтр")
            print(" [0] Выход")
            
            choice = input("\nВыберите действие: ").strip().upper()
            
            if choice == "N" and current_page < total_pages:
                current_page += 1
            elif choice == "P" and current_page > 1:
                current_page -= 1
            elif choice == "F":
                history = filter_history(history)
                current_page = 1
                total_pages = (len(history) + per_page - 1) // per_page
            elif choice == "R":
                history = generate_demo_history()  # Сброс к полной истории
                current_page = 1
                total_pages = (len(history) + per_page - 1) // per_page
            elif choice == "0":
                break
            else:
                print("❌ Неверный выбор")
        
        print(f"\n✅ Просмотр истории завершен!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Просмотр прерван пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()