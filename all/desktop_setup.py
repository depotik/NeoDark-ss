import os
import sys
import platform
import shutil
import json
from datetime import datetime
from pathlib import Path

def print_header():
    """Выводит заголовок программы"""
    print("🖥️ Установка рабочего стола NeoDark")
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

def get_desktop_path():
    """Получает путь к рабочему столу"""
    try:
        if platform.system() == "Windows":
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        elif platform.system() == "Darwin":  # macOS
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        else:  # Linux и другие Unix-системы
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            # Если Desktop не существует, пробуем другие варианты
            if not os.path.exists(desktop):
                desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Рабочий стол')
        
        return desktop
    except Exception as e:
        print(f"❌ Ошибка определения пути к рабочему столу: {e}")
        return None

def create_neodark_shortcut():
    """Создает ярлык NeoDark на рабочем столе"""
    print("🔗 Создание ярлыка NeoDark:")
    print("-" * 30)
    
    try:
        desktop_path = get_desktop_path()
        if not desktop_path:
            return False
        
        # Проверяем существование рабочего стола
        if not os.path.exists(desktop_path):
            print(f"   ⚠️  Путь к рабочему столу не найден: {desktop_path}")
            # Пытаемся создать директорию
            try:
                os.makedirs(desktop_path, exist_ok=True)
                print(f"   ✅ Создана директория рабочего стола")
            except Exception as e:
                print(f"   ❌ Ошибка создания директории: {e}")
                return False
        
        # Определяем путь к основному скрипту
        main_script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
        if not os.path.exists(main_script):
            print("   ⚠️  Основной скрипт не найден")
            main_script = os.path.abspath(__file__)
        
        system = platform.system()
        
        if system == "Windows":
            # Создаем .bat файл для Windows
            shortcut_content = f'''@echo off
REM Ярлык NeoDark
cd /d "{os.path.dirname(main_script)}"
python.exe "{main_script}"
pause
'''
            shortcut_path = os.path.join(desktop_path, "NeoDark.bat")
            
        elif system == "Darwin":  # macOS
            # Создаем shell-скрипт для macOS
            shortcut_content = f'''#!/bin/bash
# Ярлык NeoDark
cd "{os.path.dirname(main_script)}"
python3 "{main_script}"
echo "Нажмите Enter для выхода..."
read
'''
            shortcut_path = os.path.join(desktop_path, "NeoDark.sh")
            
        else:  # Linux и другие Unix-системы
            # Создаем shell-скрипт для Linux
            shortcut_content = f'''#!/bin/bash
# Ярлык NeoDark
cd "{os.path.dirname(main_script)}"
python3 "{main_script}"
echo "Нажмите Enter для выхода..."
read
'''
            shortcut_path = os.path.join(desktop_path, "NeoDark.sh")
        
        # Создаем файл ярлыка
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(shortcut_content)
        
        # Для Unix-систем делаем файл исполняемым
        if system in ["Linux", "Darwin"]:
            os.chmod(shortcut_path, 0o755)
        
        print(f"   ✅ Ярлык создан: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка создания ярлыка: {e}")
        return False

def create_desktop_config():
    """Создает конфигурацию рабочего стола"""
    print("\n🔧 Создание конфигурации рабочего стола:")
    print("-" * 40)
    
    try:
        # Создаем директорию конфигурации
        config_dir = Path.home() / ".neodark" / "desktop"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем конфигурационный файл
        config_file = config_dir / "setup.json"
        
        config = {
            "timestamp": datetime.now().isoformat(),
            "desktop_path": get_desktop_path(),
            "shortcuts": ["NeoDark"],
            "wallpaper": "default",
            "icons": {
                "size": "medium",
                "arrangement": "auto"
            },
            "version": "1.0"
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ Конфигурация создана: {config_file}")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка создания конфигурации: {e}")
        return False

def setup_neodark_folders():
    """Создает папки NeoDark на рабочем столе"""
    print("\n📁 Создание папок NeoDark:")
    print("-" * 30)
    
    try:
        desktop_path = get_desktop_path()
        if not desktop_path:
            return False
        
        # Создаем основную папку NeoDark
        neodark_folder = os.path.join(desktop_path, "NeoDark")
        os.makedirs(neodark_folder, exist_ok=True)
        print(f"   ✅ Основная папка: {neodark_folder}")
        
        # Создаем подпапки
        subfolders = ["Projects", "Tools", "Logs", "Configs", "Backups"]
        for folder in subfolders:
            folder_path = os.path.join(neodark_folder, folder)
            os.makedirs(folder_path, exist_ok=True)
            print(f"   📁 Подпапка: {folder}")
        
        print("   ✅ Все папки успешно созданы")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка создания папок: {e}")
        return False

def setup_desktop_wallpaper():
    """Настраивает обои рабочего стола (демо)"""
    print("\n🖼️ Настройка обоев рабочего стола:")
    print("-" * 35)
    
    print("   🖼️ Доступные темы обоев:")
    wallpapers = [
        "1. NeoDark Dark Theme",
        "2. NeoDark Light Theme", 
        "3. NeoDark Matrix Theme",
        "4. NeoDark Cyberpunk Theme"
    ]
    
    for wallpaper in wallpapers:
        print(f"   {wallpaper}")
    
    print("\n   ⚠️  Применение обоев требует дополнительных прав")
    print("   и доступно в полной версии NeoDark.")
    
    choice = input("\nВыберите обои (1-4) или пропустите (Enter): ").strip()
    if choice in ['1', '2', '3', '4']:
        print(f"   📝 Выбраны обои: {wallpapers[int(choice)-1]}")
        print("   💡 Для применения скачайте полную версии NeoDark")
    
    return True

def show_desktop_tips():
    """Показывает советы по организации рабочего стола"""
    print("\n💡 Советы по организации рабочего стола:")
    print("-" * 45)
    print("   1. Используйте папки для группировки файлов")
    print("   2. Регулярно очищайте рабочий стол")
    print("   3. Используйте ярлыки вместо копий программ")
    print("   4. Настройте удобное расположение иконок")
    print("   5. Используйте обои, которые не отвлекают")
    print("   6. Создайте отдельные папки для проектов")
    print("   7. Используйте сортировку по типу файлов")
    print("   8. Регулярно архивируйте старые файлы")

def show_neodark_desktop_features():
    """Показывает особенности рабочего стола NeoDark"""
    print("\n✨ Особенности рабочего стола NeoDark:")
    print("-" * 45)
    print("   • Автоматическая организация файлов")
    print("   • Интеграция с облачными сервисами")
    print("   • Синхронизация настроек между устройствами")
    print("   • Темы оформления")
    print("   • Уведомления о важных событиях")
    print("   • Быстрый доступ к инструментам")
    print("   • Защита конфиденциальных данных")
    print("   • Автоматическое резервное копирование")

def main():
    """Главная функция установки рабочего стола"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Показываем информацию о рабочем столе
        desktop_path = get_desktop_path()
        if desktop_path:
            print(f"📂 Путь к рабочему столу: {desktop_path}")
        else:
            print("❌ Не удалось определить путь к рабочему столу")
            input("\nНажмите Enter для выхода...")
            return
        
        # Создаем ярлык NeoDark
        print("\n" + "=" * 50)
        if create_neodark_shortcut():
            print("✅ Ярлык NeoDark успешно создан")
        else:
            print("⚠️ Ошибка создания ярлыка")
        
        # Создаем конфигурацию
        if create_desktop_config():
            print("✅ Конфигурация рабочего стола создана")
        else:
            print("⚠️ Ошибка создания конфигурации")
        
        # Создаем папки
        if setup_neodark_folders():
            print("✅ Папки NeoDark созданы")
        else:
            print("⚠️ Ошибка создания папок")
        
        # Настраиваем обои (демо)
        setup_desktop_wallpaper()
        
        # Показываем советы
        show_desktop_tips()
        
        # Показываем особенности
        show_neodark_desktop_features()
        
        print(f"\n🎉 Установка рабочего стола завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Установка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()