import os
import sys
import platform
import subprocess
import time
from datetime import datetime

def print_header():
    """Выводит заголовок программы"""
    print("🛡️  Отключение телеметрии NeoDark")
    print("=" * 50)

def check_platform():
    """Проверяет, поддерживается ли текущая платформа"""
    system = platform.system()
    if system not in ["Windows", "Linux", "Darwin"]:
        print(f"❌ Платформа {system} не поддерживается")
        return False
    return True

def disable_windows_telemetry():
    """Отключает телеметрию Windows"""
    print("🔧 Отключение телеметрии Windows...")
    
    if platform.system() != "Windows":
        print("   ⚠️  Эта функция доступна только в Windows")
        return False
    
    try:
        # Список служб для отключения
        services_to_disable = [
            "DiagTrack",           # Connected User Experiences and Telemetry
            "dmwappushservice",    # WAP Push Message Routing Service
            "WerSvc"              # Windows Error Reporting Service
        ]
        
        # Список задач планировщика для отключения
        tasks_to_disable = [
            "\\Microsoft\\Windows\\Application Experience\\Microsoft Compatibility Appraiser",
            "\\Microsoft\\Windows\\Application Experience\\ProgramDataUpdater",
            "\\Microsoft\\Windows\\Auto Update\\AUOptionsNotify",
            "\\Microsoft\\Windows\\Customer Experience Improvement Program\\BthSQM",
            "\\Microsoft\\Windows\\Customer Experience Improvement Program\\Consolidator",
            "\\Microsoft\\Windows\\Customer Experience Improvement Program\\KernelCeipTask",
            "\\Microsoft\\Windows\\Customer Experience Improvement Program\\UsbCeip",
            "\\Microsoft\\Windows\\DiskDiagnostic\\Microsoft-Windows-DiskDiagnosticDataCollector"
        ]
        
        # Отключение служб
        print("   🚫 Отключение служб телеметрии...")
        for service in services_to_disable:
            try:
                subprocess.run(
                    ["sc", "config", service, "start=", "disabled"], 
                    capture_output=True, 
                    text=True, 
                    shell=True
                )
                subprocess.run(
                    ["sc", "stop", service], 
                    capture_output=True, 
                    text=True, 
                    shell=True
                )
                print(f"     ✅ Служба {service} отключена")
            except Exception as e:
                print(f"     ⚠️  Ошибка отключения службы {service}: {e}")
        
        # Отключение задач планировщика
        print("   🚫 Отключение задач планировщика...")
        for task in tasks_to_disable:
            try:
                subprocess.run(
                    ["schtasks", "/change", "/tn", task, "/disable"], 
                    capture_output=True, 
                    text=True, 
                    shell=True
                )
                print(f"     ✅ Задача {task} отключена")
            except Exception as e:
                print(f"     ⚠️  Ошибка отключения задачи {task}: {e}")
        
        # Отключение через реестр (основные параметры)
        print("   🚫 Настройка параметров реестра...")
        registry_commands = [
            # Отключение telemetry
            ["reg", "add", "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection", 
             "/v", "AllowTelemetry", "/t", "REG_DWORD", "/d", "0", "/f"],
            
            # Отключение CEIP
            ["reg", "add", "HKLM\\SOFTWARE\\Microsoft\\SQMClient\\Windows", 
             "/v", "CEIPEnable", "/t", "REG_DWORD", "/d", "0", "/f"],
            
            # Отключение веб-поиска в меню Пуск
            ["reg", "add", "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search", 
             "/v", "BingSearchEnabled", "/t", "REG_DWORD", "/d", "0", "/f"],
        ]
        
        for cmd in registry_commands:
            try:
                subprocess.run(cmd, capture_output=True, text=True, shell=True)
                print(f"     ✅ Параметр реестра установлен")
            except Exception as e:
                print(f"     ⚠️  Ошибка установки параметра реестра: {e}")
        
        print("   ✅ Телеметрия Windows отключена")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка отключения телеметрии Windows: {e}")
        return False

def disable_linux_telemetry():
    """Отключение телеметрии Linux (Ubuntu и другие)"""
    print("🔧 Отключение телеметрии Linux...")
    
    try:
        # Отключение Ubuntu telemetry если доступно
        if os.path.exists("/usr/bin/ubuntu-report"):
            try:
                subprocess.run(["sudo", "ubuntu-report", "off"], capture_output=True, text=True)
                print("   ✅ Ubuntu telemetry отключен")
            except Exception as e:
                print(f"   ⚠️  Ошибка отключения Ubuntu telemetry: {e}")
        
        # Отключение apport (система отчетов об ошибках)
        try:
            subprocess.run(["sudo", "systemctl", "stop", "apport"], capture_output=True, text=True)
            subprocess.run(["sudo", "systemctl", "disable", "apport"], capture_output=True, text=True)
            print("   ✅ Система отчетов об ошибках отключена")
        except Exception as e:
            print(f"   ⚠️  Ошибка отключения apport: {e}")
        
        # Отключение whoopsie (еще одна система отчетов об ошибках)
        try:
            subprocess.run(["sudo", "systemctl", "stop", "whoopsie"], capture_output=True, text=True)
            subprocess.run(["sudo", "systemctl", "disable", "whoopsie"], capture_output=True, text=True)
            print("   ✅ Whoopsie отключен")
        except Exception as e:
            print(f"   ⚠️  Ошибка отключения whoopsie: {e}")
        
        print("   ✅ Телеметрия Linux отключена")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка отключения телеметрии Linux: {e}")
        return False

def disable_macos_telemetry():
    """Отключение телеметрии macOS"""
    print("🔧 Отключение телеметрии macOS...")
    
    if platform.system() != "Darwin":
        print("   ⚠️  Эта функция доступна только в macOS")
        return False
    
    try:
        # Отключение аналитики и телеметрии
        analytics_commands = [
            ["sudo", "launchctl", "unload", "-w", 
             "/System/Library/LaunchDaemons/com.apple.apsd.plist"],
            ["sudo", "launchctl", "unload", "-w", 
             "/System/Library/LaunchDaemons/com.apple.analyticsd.plist"],
            ["sudo", "launchctl", "unload", "-w", 
             "/System/Library/LaunchDaemons/com.apple.diagnosticd.plist"]
        ]
        
        for cmd in analytics_commands:
            try:
                subprocess.run(cmd, capture_output=True, text=True)
                print("   ✅ Компоненты аналитики отключены")
            except Exception as e:
                print(f"   ⚠️  Ошибка отключения компонентов: {e}")
        
        print("   ✅ Телеметрия macOS отключена")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка отключения телеметрии macOS: {e}")
        return False

def show_telemetry_info():
    """Показывает информацию о телеметрии"""
    print("\nℹ️  Что такое телеметрия и зачем её отключать:")
    print("   Телеметрия - это сбор данных об использовании системы и приложений.")
    print("   Компании используют эти данные для улучшения своих продуктов,")
    print("   но это может затрагивать вашу конфиденциальность.")
    print()
    print("   Отключение телеметрии может:")
    print("   ✅ Повысить приватность")
    print("   ✅ Уменьшить сетевой трафик")
    print("   ✅ Потенциально улучшить производительность")
    print()
    print("   ⚠️  ВАЖНО:")
    print("   Некоторые функции могут перестать работать корректно")
    print("   Разработчики теряют возможность получать данные об ошибках")

def main():
    """Главная функция отключения телеметрии"""
    print_header()
    
    # Проверка платформы
    if not check_platform():
        input("\nНажмите Enter для выхода...")
        return
    
    system = platform.system()
    
    print(f"💻 Обнаружена система: {system}")
    
    # Подтверждение действия
    print("\n⚠️  ВНИМАНИЕ!")
    print("   Отключение телеметрии может повлиять на работу некоторых функций системы.")
    print("   Для внесения изменений в системные настройки могут потребоваться права администратора.")
    
    confirm = input("\nПродолжить? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'д', 'да']:
        print("❌ Операция отменена пользователем")
        input("\nНажмите Enter для выхода...")
        return
    
    try:
        success = False
        
        if system == "Windows":
            success = disable_windows_telemetry()
        elif system == "Linux":
            success = disable_linux_telemetry()
        elif system == "Darwin":  # macOS
            success = disable_macos_telemetry()
        
        if success:
            print(f"\n🎉 Телеметрия успешно отключена!")
            print("💡 Рекомендуется перезагрузить систему для применения всех изменений")
        else:
            print(f"\n⚠️  Некоторые компоненты телеметрии не удалось отключить")
        
        print(f"\n✅ Операция завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Операция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    # Показываем информацию
    show_telemetry_info()
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()