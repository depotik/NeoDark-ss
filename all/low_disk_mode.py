import json
import os
import sys
import platform
import shutil
import psutil
from datetime import datetime
from pathlib import Path

def print_header():
    """Выводит заголовок программы"""
    print("💾 Режим Low-Disk NeoDark")
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

def check_disk_space():
    """Проверяет доступное место на диске"""
    print("🔍 Проверка дискового пространства:")
    print("-" * 35)
    
    try:
        # Получаем информацию о диске
        if platform.system() == "Windows":
            disk = psutil.disk_usage('C:\\')
        else:
            disk = psutil.disk_usage('/')
        
        total = disk.total
        used = disk.used
        free = disk.free
        percent = disk.percent
        
        print(f"   Всего места: {format_bytes(total)}")
        print(f"   Использовано: {format_bytes(used)}")
        print(f"   Свободно: {format_bytes(free)}")
        print(f"   Процент использования: {percent}%")
        
        # Определяем состояние диска
        if percent > 90:
            print("   🚨 Критически мало свободного места!")
            status = "critical"
        elif percent > 80:
            print("   ⚠️ Мало свободного места")
            status = "low"
        else:
            print("   ✅ Достаточно свободного места")
            status = "ok"
        
        return {
            "total": total,
            "used": used,
            "free": free,
            "percent": percent,
            "status": status
        }
    except Exception as e:
        print(f"   ❌ Ошибка проверки дискового пространства: {e}")
        return None

def format_bytes(bytes_value):
    """Форматирует байты в удобочитаемый формат"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def identify_large_files_and_dirs():
    """Определяет большие файлы и директории"""
    print("\n🔍 Поиск больших файлов и директорий:")
    print("-" * 40)
    
    try:
        # Определяем директории для проверки
        dirs_to_check = []
        
        if platform.system() == "Windows":
            dirs_to_check = [
                os.path.expanduser('~\\Desktop'),
                os.path.expanduser('~\\Downloads'),
                os.path.expanduser('~\\Documents'),
                os.environ.get('TEMP', 'C:\\Windows\\Temp')
            ]
        else:
            dirs_to_check = [
                os.path.expanduser('~/Desktop'),
                os.path.expanduser('~/Downloads'),
                os.path.expanduser('~/Documents'),
                '/tmp'
            ]
        
        large_items = []
        
        for directory in dirs_to_check:
            if os.path.exists(directory):
                try:
                    # Проверяем директорию
                    total_size = get_directory_size(directory)
                    if total_size > 100 * 1024 * 1024:  # Больше 100MB
                        large_items.append({
                            'path': directory,
                            'size': total_size,
                            'type': 'directory'
                        })
                    
                    # Проверяем отдельные большие файлы
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                file_size = os.path.getsize(file_path)
                                if file_size > 50 * 1024 * 1024:  # Больше 50MB
                                    large_items.append({
                                        'path': file_path,
                                        'size': file_size,
                                        'type': 'file'
                                    })
                            except (OSError, FileNotFoundError):
                                continue
                except Exception:
                    continue
        
        # Сортируем по размеру
        large_items.sort(key=lambda x: x['size'], reverse=True)
        
        # Показываем топ-10 больших элементов
        print("   Топ больших файлов и директорий:")
        for i, item in enumerate(large_items[:10], 1):
            icon = "📁" if item['type'] == 'directory' else "📄"
            print(f"   {icon} {format_bytes(item['size'])} - {item['path']}")
        
        return large_items
    except Exception as e:
        print(f"   ❌ Ошибка поиска больших файлов: {e}")
        return []

def get_directory_size(path):
    """Получает размер директории"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    continue
    except Exception:
        pass
    return total_size

def clean_temp_files():
    """Очищает временные файлы"""
    print("\n🧹 Очистка временных файлов:")
    print("-" * 30)
    
    cleaned_size = 0
    files_deleted = 0
    
    try:
        # Определяем директории временных файлов
        temp_dirs = []
        
        if platform.system() == "Windows":
            temp_dirs = [
                os.environ.get('TEMP', 'C:\\Windows\\Temp'),
                os.path.expanduser('~\\AppData\\Local\\Temp')
            ]
        else:
            temp_dirs = ['/tmp']
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path):
                                file_size = os.path.getsize(item_path)
                                os.remove(item_path)
                                cleaned_size += file_size
                                files_deleted += 1
                            elif os.path.isdir(item_path):
                                dir_size = get_directory_size(item_path)
                                shutil.rmtree(item_path)
                                cleaned_size += dir_size
                                files_deleted += 1
                        except (OSError, PermissionError):
                            continue
                except Exception:
                    continue
        
        print(f"   ✅ Очищено {files_deleted} элементов")
        print(f"   🗑️ Освобождено: {format_bytes(cleaned_size)}")
        return cleaned_size
    except Exception as e:
        print(f"   ❌ Ошибка очистки временных файлов: {e}")
        return 0

def clean_cache_files():
    """Очищает файлы кэша"""
    print("\n🗑️ Очистка файлов кэша:")
    print("-" * 25)
    
    cleaned_size = 0
    files_deleted = 0
    
    try:
        # Определяем директории кэша
        cache_dirs = []
        
        if platform.system() == "Windows":
            cache_dirs = [
                os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\INetCache'),
                os.path.expanduser('~\\AppData\\Local\\Temp')
            ]
        else:
            cache_dirs = [
                os.path.expanduser('~/.cache'),
                '/var/cache'
            ]
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    dir_size = get_directory_size(cache_dir)
                    shutil.rmtree(cache_dir)
                    os.makedirs(cache_dir, exist_ok=True)  # Создаем пустую директорию
                    cleaned_size += dir_size
                    files_deleted += 1
                except (OSError, PermissionError) as e:
                    print(f"   ⚠️ Ошибка очистки {cache_dir}: {e}")
                    continue
        
        print(f"   ✅ Очищено {files_deleted} кэш-директорий")
        print(f"   🗑️ Освобождено: {format_bytes(cleaned_size)}")
        return cleaned_size
    except Exception as e:
        print(f"   ❌ Ошибка очистки кэша: {e}")
        return 0

def enable_low_disk_mode():
    """Включает режим экономии дискового пространства"""
    print("\n⚡ Включение режима Low-Disk:")
    print("-" * 30)
    
    try:
        # Создаем файл конфигурации режима
        config_dir = Path.home() / ".neodark"
        config_dir.mkdir(exist_ok=True)
        
        mode_file = config_dir / "low_disk_mode.json"
        
        config = {
            "enabled": True,
            "timestamp": datetime.now().isoformat(),
            "auto_cleanup": True,
            "warning_threshold": 80,
            "critical_threshold": 90
        }
        
        with open(mode_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("   ✅ Режим Low-Disk включен")
        print("   ⚙️ Автоматическая очистка активирована")
        print(f"   📁 Конфигурация сохранена: {mode_file}")
        return True
    except Exception as e:
        print(f"   ❌ Ошибка включения режима: {e}")
        return False

def show_saving_tips():
    """Показывает советы по экономии места"""
    print("\n💡 Советы по экономии дискового пространства:")
    print("-" * 50)
    print("   1. Регулярно очищайте временную память")
    print("   2. Удаляйте ненужные загрузки")
    print("   3. Используйте облачные хранилища")
    print("   4. Архивируйте старые файлы")
    print("   5. Удаляйте дубликаты файлов")
    print("   6. Очищайте корзину")
    print("   7. Удаляйте ненужные программы")
    print("   8. Используйте режим Low-Disk в NeoDark")

def main():
    """Главная функция режима Low-Disk"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Проверяем дисковое пространство
        disk_info = check_disk_space()
        
        if not disk_info:
            print("❌ Не удалось получить информацию о диске")
            input("\nНажмите Enter для выхода...")
            return
        
        # Если место критически мало, предлагаем действия
        if disk_info['status'] in ['critical', 'low']:
            print("\n⚠️ Обнаружено малое количество свободного места!")
            
            # Ищем большие файлы
            large_items = identify_large_files_and_dirs()
            
            # Предлагаем очистку
            print("\n" + "=" * 50)
            choice = input("Выполнить автоматическую очистку? (y/N): ").strip().lower()
            if choice in ['y', 'yes', 'д', 'да']:
                # Очищаем временные файлы
                temp_cleaned = clean_temp_files()
                
                # Очищаем кэш
                cache_cleaned = clean_cache_files()
                
                # Показываем результаты
                total_cleaned = temp_cleaned + cache_cleaned
                print(f"\n📊 Итого освобождено: {format_bytes(total_cleaned)}")
        else:
            print("\n✅ С дисковым пространством всё в порядке")
            
            # Показываем большие файлы для информации
            large_items = identify_large_files_and_dirs()
        
        # Предлагаем включить режим экономии места
        print("\n" + "=" * 50)
        choice = input("Включить постоянный режим Low-Disk? (y/N): ").strip().lower()
        if choice in ['y', 'yes', 'д', 'да']:
            enable_low_disk_mode()
        
        # Показываем советы
        show_saving_tips()
        
        print(f"\n✅ Работа в режиме Low-Disk завершена!")
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