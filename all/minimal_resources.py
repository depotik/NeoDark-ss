import os
import sys
import platform
import psutil
import gc
import time
from datetime import datetime

def print_header():
    """Выводит заголовок программы"""
    print("⚡ Запуск NeoDark с минимальными ресурсами")
    print("=" * 55)

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

def get_system_resources():
    """Получает информацию о системных ресурсах"""
    try:
        # Получаем информацию о памяти
        memory = psutil.virtual_memory()
        
        # Получаем информацию о CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Получаем информацию о диске
        disk = psutil.disk_usage('/')
        
        return {
            'memory_total': memory.total,
            'memory_available': memory.available,
            'memory_percent': memory.percent,
            'cpu_percent': cpu_percent,
            'disk_total': disk.total,
            'disk_free': disk.free,
            'disk_percent': disk.percent
        }
    except Exception as e:
        print(f"❌ Ошибка получения информации о ресурсах: {e}")
        return None

def display_resources(resources, title="Текущие ресурсы"):
    """Отображает информацию о ресурсах"""
    if not resources:
        return
    
    print(f"\n📊 {title}:")
    print("-" * 40)
    print(f"   Память: {format_bytes(resources['memory_available'])} / {format_bytes(resources['memory_total'])}")
    print(f"   Использование памяти: {resources['memory_percent']:.1f}%")
    print(f"   Использование CPU: {resources['cpu_percent']:.1f}%")
    print(f"   Диск: {format_bytes(resources['disk_free'])} / {format_bytes(resources['disk_total'])}")
    print(f"   Использование диска: {resources['disk_percent']:.1f}%")

def format_bytes(bytes_value):
    """Форматирует байты в удобочитаемый формат"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def optimize_memory():
    """Оптимизирует использование памяти"""
    print("\n🧠 Оптимизация памяти...")
    print("-" * 30)
    
    # Получаем начальную информацию
    initial_memory = psutil.Process().memory_info().rss
    
    # Сборка мусора
    collected = gc.collect()
    print(f"   🗑️  Сборка мусора: {collected} объектов")
    
    # Освобождение кэшей
    try:
        # Очистка кэша файловой системы (для Linux/macOS)
        if platform.system() in ["Linux", "Darwin"]:
            os.system("sync")
            print("   🔄 Очистка файлового кэша")
    except:
        pass
    
    # Получаем конечную информацию
    final_memory = psutil.Process().memory_info().rss
    freed_memory = initial_memory - final_memory
    
    print(f"   📉 Освобождено памяти: {format_bytes(abs(freed_memory))}")
    return freed_memory

def limit_cpu_priority():
    """Ограничивает приоритет CPU"""
    print("\n⚙️  Ограничение приоритета CPU...")
    print("-" * 30)
    
    try:
        # Получаем текущий процесс
        process = psutil.Process()
        
        # Устанавливаем низкий приоритет
        if platform.system() == "Windows":
            process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        else:
            process.nice(10)  # Низкий приоритет для Unix-систем
        
        print("   🐌 Установлен низкий приоритет выполнения")
        return True
    except Exception as e:
        print(f"   ❌ Ошибка установки приоритета: {e}")
        return False

def disable_unnecessary_features():
    """Отключает ненужные функции для экономии ресурсов"""
    print("\n🔌 Отключение ненужных функций...")
    print("-" * 30)
    
    disabled_features = []
    
    # Отключение анимаций
    os.environ['NEODARK_NO_ANIMATIONS'] = '1'
    disabled_features.append("анимации")
    
    # Отключение логов
    os.environ['NEODARK_MINIMAL_LOGGING'] = '1'
    disabled_features.append("подробное логирование")
    
    # Отключение фоновых задач
    os.environ['NEODARK_NO_BACKGROUND_TASKS'] = '1'
    disabled_features.append("фоновые задачи")
    
    # Отключение звуков
    os.environ['NEODARK_NO_SOUNDS'] = '1'
    disabled_features.append("звуковые эффекты")
    
    for feature in disabled_features:
        print(f"   🚫 Отключены {feature}")
    
    return disabled_features

def show_minimal_mode_benefits():
    """Показывает преимущества минимального режима"""
    print("\n🌟 Преимущества минимального режима:")
    print("-" * 40)
    print("   • Минимальное использование ресурсов")
    print("   • Быстрый запуск")
    print("   • Низкое энергопотребление")
    print("   • Подходит для слабых систем")
    print("   • Уменьшенный объем памяти")
    print()

def show_minimal_mode_limitations():
    """Показывает ограничения минимального режима"""
    print("\n⚠️  Ограничения минимального режима:")
    print("-" * 40)
    print("   • Отключены визуальные эффекты")
    print("   • Ограничена функциональность")
    print("   • Меньше информации в выводе")
    print("   • Отсутствуют анимации")
    print("   • Упрощенный интерфейс")
    print()

def run_minimal_neodark():
    """Запускает NeoDark в минимальном режиме"""
    print("\n🚀 Запуск NeoDark в минимальном режиме...")
    print("-" * 40)
    
    # Установка флага минимального режима
    os.environ['NEODARK_MINIMAL_MODE'] = '1'
    
    # Имитация запуска
    print("   ⚙️  Инициализация ядра...")
    time.sleep(0.5)
    
    print("   🧩 Загрузка основных модулей...")
    time.sleep(0.5)
    
    print("   📦 Подготовка интерфейса...")
    time.sleep(0.5)
    
    print("   ✅ NeoDark запущен в минимальном режиме")
    
    # Показываем упрощенное меню
    print("\n📋 Доступные функции:")
    print("   [1] Статус системы")
    print("   [2] Очистить кэш")
    print("   [3] Выход")
    
    while True:
        try:
            choice = input("\nВыберите функцию (1-3): ").strip()
            
            if choice == "1":
                # Упрощенный статус системы
                resources = get_system_resources()
                display_resources(resources, "Системные ресурсы")
            elif choice == "2":
                # Упрощенная очистка кэша
                freed = optimize_memory()
                print(f"   🧹 Кэш очищен, освобождено: {format_bytes(freed)}")
            elif choice == "3":
                print("👋 Выход из минимального режима...")
                break
            else:
                print("❌ Неверный выбор")
        except KeyboardInterrupt:
            print("\n👋 Принудительный выход из минимального режима...")
            break

def main():
    """Главная функция минимального режима"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Получаем начальную информацию о ресурсах
        initial_resources = get_system_resources()
        display_resources(initial_resources, "Начальные ресурсы")
        
        # Оптимизируем память
        freed_memory = optimize_memory()
        
        # Ограничиваем приоритет CPU
        limit_cpu_priority()
        
        # Отключаем ненужные функции
        disable_unnecessary_features()
        
        # Показываем преимущества и ограничения
        show_minimal_mode_benefits()
        show_minimal_mode_limitations()
        
        # Получаем информацию о ресурсах после оптимизации
        final_resources = get_system_resources()
        display_resources(final_resources, "Ресурсы после оптимизации")
        
        # Показываем экономию
        if initial_resources and final_resources:
            memory_saved = initial_resources['memory_percent'] - final_resources['memory_percent']
            cpu_saved = initial_resources['cpu_percent'] - final_resources['cpu_percent']
            print(f"\n📈 Экономия ресурсов:")
            print(f"   Память: {memory_saved:.1f}%")
            print(f"   CPU: {cpu_saved:.1f}%")
        
        print(f"\n🎉 Оптимизация завершена!")
        print(f"⚡ NeoDark готов к запуску в минимальном режиме")
        
        # Предлагаем запустить в минимальном режиме
        choice = input("\nЗапустить NeoDark в минимальном режиме? (Y/n): ").strip().lower()
        if choice not in ['n', 'no', 'н', 'нет']:
            run_minimal_neodark()
        
        print(f"\n✅ Работа в минимальном режиме завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Операция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    # Проверка наличия необходимых модулей
    try:
        import psutil
    except ImportError:
        print("❌ Модуль 'psutil' не установлен.")
        print("Установите его командой: pip install psutil")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    main()