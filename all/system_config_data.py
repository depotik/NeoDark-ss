import os
import sys
import platform
import json
import hashlib
from datetime import datetime
from pathlib import Path
import psutil

def print_header():
    """Выводит заголовок программы"""
    print("⚙️ Данные системы и конфигурации NeoDark")
    print("=" * 50)

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

def get_system_info():
    """Получает информацию о системе"""
    print("💻 Информация о системе:")
    print("-" * 30)
    
    try:
        system_info = {
            "hostname": platform.node(),
            "os": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": platform.architecture(),
            "python_version": platform.python_version(),
            "neodark_version": "1.2.5"
        }
        
        for key, value in system_info.items():
            print(f"   {key.capitalize()}: {value}")
        
        return system_info
    except Exception as e:
        print(f"   ❌ Ошибка получения информации о системе: {e}")
        return {}

def get_hardware_info():
    """Получает информацию о железе"""
    print("\n🖥️ Информация о железе:")
    print("-" * 30)
    
    try:
        hardware_info = {}
        
        # Информация о CPU
        hardware_info['cpu_count_logical'] = psutil.cpu_count(logical=True)
        hardware_info['cpu_count_physical'] = psutil.cpu_count(logical=False)
        hardware_info['cpu_freq'] = psutil.cpu_freq().current if psutil.cpu_freq() else "N/A"
        
        # Информация о памяти
        memory = psutil.virtual_memory()
        hardware_info['memory_total'] = memory.total
        hardware_info['memory_available'] = memory.available
        
        # Информация о дисках
        disk = psutil.disk_usage('/')
        hardware_info['disk_total'] = disk.total
        hardware_info['disk_free'] = disk.free
        
        # Выводим информацию
        print(f"   Логических ядер CPU: {hardware_info['cpu_count_logical']}")
        print(f"   Физических ядер CPU: {hardware_info['cpu_count_physical']}")
        print(f"   Частота CPU: {hardware_info['cpu_freq']} MHz")
        print(f"   Всего памяти: {format_bytes(hardware_info['memory_total'])}")
        print(f"   Доступно памяти: {format_bytes(hardware_info['memory_available'])}")
        print(f"   Всего места на диске: {format_bytes(hardware_info['disk_total'])}")
        print(f"   Свободно на диске: {format_bytes(hardware_info['disk_free'])}")
        
        return hardware_info
    except Exception as e:
        print(f"   ❌ Ошибка получения информации о железе: {e}")
        return {}

def get_neodark_config():
    """Получает конфигурацию NeoDark"""
    print("\n🔧 Конфигурация NeoDark:")
    print("-" * 30)
    
    try:
        # Создаем директорию конфигурации если её нет
        config_dir = Path.home() / ".neodark"
        config_dir.mkdir(exist_ok=True)
        
        # Путь к файлу конфигурации
        config_file = config_dir / "config.json"
        
        # Если файл конфигурации существует, читаем его
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            # Создаем базовую конфигурацию
            config = {
                "language": "ru",
                "theme": "dark",
                "autostart": False,
                "minimize_on_startup": False,
                "check_updates": True,
                "enable_logging": True,
                "log_level": "INFO"
            }
            
            # Сохраняем конфигурацию
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        
        # Выводим конфигурацию
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        print(f"\n   📁 Файл конфигурации: {config_file}")
        return config
    except Exception as e:
        print(f"   ❌ Ошибка работы с конфигурацией: {e}")
        return {}

def get_installed_products():
    """Получает список установленных продуктов"""
    print("\n📦 Установленные продукты:")
    print("-" * 30)
    
    # Симуляция списка установленных продуктов
    products = [
        {
            "id": "neodark-core",
            "name": "NeoDark Core",
            "version": "1.2.5",
            "status": "installed",
            "install_date": "2023-10-15"
        },
        {
            "id": "neodark-security",
            "name": "NeoDark Security Suite",
            "version": "3.0.1",
            "status": "installed",
            "install_date": "2023-11-20"
        },
        {
            "id": "neodark-media",
            "name": "NeoDark Media Pack",
            "version": "2.4.0",
            "status": "installed",
            "install_date": "2023-09-05"
        }
    ]
    
    for product in products:
        status_icon = "✅" if product['status'] == 'installed' else "🔄"
        print(f"   {status_icon} {product['name']} (v{product['version']})")
        print(f"     ID: {product['id']}")
        print(f"     Установлен: {product['install_date']}")
        print()
    
    return products

def get_environment_info():
    """Получает информацию о переменных окружения"""
    print("\n🌍 Переменные окружения:")
    print("-" * 30)
    
    # Основные переменные окружения
    important_vars = [
        'PATH', 'HOME', 'USER', 'USERNAME', 'SHELL', 
        'LANG', 'PYTHONPATH', 'VIRTUAL_ENV'
    ]
    
    for var in important_vars:
        value = os.environ.get(var, 'Не задано')
        # Обрезаем длинные значения
        if len(value) > 50:
            value = value[:47] + "..."
        print(f"   {var}: {value}")

def format_bytes(bytes_value):
    """Форматирует байты в удобочитаемый формат"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def export_system_info():
    """Экспортирует информацию о системе в файл"""
    print("\n💾 Экспорт информации:")
    print("-" * 30)
    
    try:
        # Создаем директорию для экспорта если её нет
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        # Подготавливаем данные для экспорта
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "system_info": get_system_info(),
            "hardware_info": get_hardware_info(),
            "neodark_config": get_neodark_config(),
            "installed_products": get_installed_products()
        }
        
        # Генерируем имя файла
        filename = f"system_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = export_dir / filename
        
        # Экспортируем данные
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ Информация экспортирована в: {filepath}")
        return filepath
    except Exception as e:
        print(f"   ❌ Ошибка экспорта: {e}")
        return None

def show_system_summary():
    """Показывает сводку по системе"""
    print("\n📊 Сводка по системе:")
    print("-" * 30)
    
    try:
        # Получаем информацию о системе
        uname = platform.uname()
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        current_time = datetime.now()
        uptime = current_time - boot_time
        
        print(f"   Система: {uname.system} {uname.release}")
        print(f"   Версия: {uname.version}")
        print(f"   Машина: {uname.machine}")
        print(f"   Процессор: {uname.processor}")
        print(f"   Время работы: {str(uptime).split('.')[0]}")
        print(f"   Имя хоста: {uname.node}")
    except Exception as e:
        print(f"   ❌ Ошибка получения сводки: {e}")

def main():
    """Главная функция данных системы и конфигурации"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Получаем информацию о системе
        system_info = get_system_info()
        
        # Получаем информацию о железе
        hardware_info = get_hardware_info()
        
        # Получаем конфигурацию NeoDark
        neodark_config = get_neodark_config()
        
        # Получаем список установленных продуктов
        installed_products = get_installed_products()
        
        # Получаем информацию о переменных окружения
        get_environment_info()
        
        # Показываем сводку по системе
        show_system_summary()
        
        # Предлагаем экспортировать информацию
        print("\n" + "=" * 50)
        choice = input("Экспортировать информацию в файл? (y/N): ").strip().lower()
        if choice in ['y', 'yes', 'д', 'да']:
            export_system_info()
        
        print(f"\n✅ Получение данных системы завершено!")
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