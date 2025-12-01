import os
import sys
import platform
from pathlib import Path
import subprocess

def print_header():
    """Выводит заголовок программы"""
    print("🚀 Включение автозапуска NeoDark")
    print("=" * 50)

def get_system_info():
    """Получает информацию о системе"""
    system = platform.system()
    print(f"💻 Обнаружена система: {system}")
    return system

def enable_autostart_windows():
    """Включает автозапуск для Windows"""
    try:
        import winreg
        
        # Получаем путь к текущему скрипту
        script_path = os.path.abspath(sys.argv[0])
        app_path = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(app_path, "..", "main.py")
        if os.path.exists(main_script):
            script_path = os.path.abspath(main_script)
        
        # Создаем команду для запуска
        python_path = sys.executable
        command = f'"{python_path}" "{script_path}"'
        
        # Открываем ключ реестра для автозапуска
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Добавляем запись в автозапуск
        winreg.SetValueEx(key, "NeoDark", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        print("✅ Автозапуск включен для Windows")
        print(f"   Путь: {script_path}")
        return True
        
    except ImportError:
        print("❌ Модуль winreg не доступен")
        return False
    except Exception as e:
        print(f"❌ Ошибка включения автозапуска в Windows: {e}")
        return False

def enable_autostart_linux():
    """Включает автозапуск для Linux"""
    try:
        # Создаем директорию для автозапуска если её нет
        autostart_dir = Path.home() / ".config" / "autostart"
        autostart_dir.mkdir(parents=True, exist_ok=True)
        
        # Получаем путь к текущему скрипту
        script_path = os.path.abspath(sys.argv[0])
        app_path = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(app_path, "..", "main.py")
        if os.path.exists(main_script):
            script_path = os.path.abspath(main_script)
        
        # Создаем .desktop файл
        desktop_file = autostart_dir / "neodark.desktop"
        python_path = sys.executable
        
        desktop_content = f"""[Desktop Entry]
Type=Application
Name=NeoDark
Comment=NeoDark System Utility
Exec={python_path} {script_path}
Icon=utilities-terminal
Terminal=false
Categories=Utility;
"""
        
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
        
        print("✅ Автозапуск включен для Linux")
        print(f"   Файл: {desktop_file}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка включения автозапуска в Linux: {e}")
        return False

def enable_autostart_macos():
    """Включает автозапуск для macOS"""
    try:
        # Получаем путь к текущему скрипту
        script_path = os.path.abspath(sys.argv[0])
        app_path = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(app_path, "..", "main.py")
        if os.path.exists(main_script):
            script_path = os.path.abspath(main_script)
        
        # Создаем директорию для автозапуска если её нет
        autostart_dir = Path.home() / "Library" / "LaunchAgents"
        autostart_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем plist файл
        plist_file = autostart_dir / "com.neodark.autostart.plist"
        python_path = sys.executable
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.neodark.autostart</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
        
        with open(plist_file, 'w') as f:
            f.write(plist_content)
        
        print("✅ Автозапуск включен для macOS")
        print(f"   Файл: {plist_file}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка включения автозапуска в macOS: {e}")
        return False

def show_autostart_info():
    """Показывает информацию об автозапуске"""
    print("\nℹ️  Информация об автозапуске:")
    print("   Автозапуск позволяет программе запускаться автоматически")
    print("   при входе пользователя в систему.")
    print()
    print("💡 Преимущества:")
    print("   • Удобство использования")
    print("   • Автоматическое выполнение задач")
    print("   • Быстрый доступ к функциям")
    print()
    print("⚠️  Важно:")
    print("   • Может потребоваться перезагрузка для активации")
    print("   • Некоторые антивирусы могут блокировать автозапуск")
    print("   • Убедитесь, что путь к программе не изменится")

def main():
    """Главная функция включения автозапуска"""
    print_header()
    
    try:
        # Получаем информацию о системе
        system = get_system_info()
        
        # Включаем автозапуск в зависимости от системы
        success = False
        if system == "Windows":
            success = enable_autostart_windows()
        elif system == "Linux":
            success = enable_autostart_linux()
        elif system == "Darwin":  # macOS
            success = enable_autostart_macos()
        else:
            print("❌ Неподдерживаемая система")
            input("\nНажмите Enter для выхода...")
            return
        
        if success:
            print(f"\n🎉 Автозапуск успешно включен!")
        else:
            print(f"\n⚠️  Не удалось включить автозапуск")
        
        # Показываем информацию
        show_autostart_info()
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Операция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()