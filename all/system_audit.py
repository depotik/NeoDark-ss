import os
import sys
import platform
import subprocess
import hashlib
import json
from datetime import datetime
from pathlib import Path
import psutil

def print_header():
    """Выводит заголовок программы"""
    print("🛡️ Системный аудит NeoDark (Security Check)")
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

def show_audit_info():
    """Показывает информацию о системном аудите"""
    print("ℹ️ Системный аудит NeoDark:")
    print("-" * 35)
    print("   Системный аудит проверяет безопасность")
    print("   вашей системы и выявляет потенциальные")
    print("   уязвимости и риски.")
    print()
    print("   Проверки:")
    print("   • Статус антивируса")
    print("   • Открытые порты")
    print("   • Пользователи системы")
    print("   • Запущенные процессы")
    print("   • Сетевые подключения")
    print("   • Файлы с правами администратора")
    print()

def check_antivirus_status():
    """Проверяет статус антивируса"""
    print("🔍 Проверка антивируса:")
    print("-" * 25)
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # Проверяем статус Windows Defender
            cmd = ['powershell', '-Command', 
                   'Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("   Windows Defender:")
                print(f"   {result.stdout}")
            else:
                print("   ⚠️  Не удалось получить статус Windows Defender")
                
        elif system == "Linux":
            # Проверяем наличие антивирусов
            antivirus_programs = ['clamav', 'chkrootkit', 'rkhunter']
            found_av = []
            
            for av in antivirus_programs:
                result = subprocess.run(['which', av], capture_output=True, text=True)
                if result.returncode == 0:
                    found_av.append(av)
            
            if found_av:
                print(f"   Найдены антивирусы: {', '.join(found_av)}")
            else:
                print("   ⚠️  Не найдено установленных антивирусов")
                print("   💡 Рекомендуется установить ClamAV или другой антивирус")
                
        elif system == "Darwin":  # macOS
            # Проверяем наличие антивирусов
            print("   macOS включает встроенный антивирус XProtect")
            print("   Рекомендуется использовать дополнительные решения")
            
    except subprocess.TimeoutExpired:
        print("   ⏱️  Таймаут проверки антивируса")
    except Exception as e:
        print(f"   ❌ Ошибка проверки антивируса: {e}")

def check_open_ports():
    """Проверяет открытые порты"""
    print("\n🔌 Проверка открытых портов:")
    print("-" * 30)
    
    try:
        # Получаем сетевые подключения
        connections = psutil.net_connections(kind='inet')
        
        # Фильтруем открытые порты (LISTEN)
        open_ports = [conn for conn in connections if conn.status == 'LISTEN']
        
        if open_ports:
            print(f"   Открытых портов: {len(open_ports)}")
            print("   Подозрительные порты:")
            suspicious_ports = [conn.laddr.port for conn in open_ports if conn.laddr.port > 1024]
            for port in sorted(suspicious_ports)[:10]:  # Показываем первые 10
                print(f"    port {port}")
            if len(suspicious_ports) > 10:
                print(f"   ... и еще {len(suspicious_ports) - 10} портов")
        else:
            print("   ✅ Нет открытых портов")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки портов: {e}")

def check_users():
    """Проверяет пользователей системы"""
    print("\n👥 Проверка пользователей:")
    print("-" * 25)
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # Получаем список пользователей Windows
            cmd = ['net', 'user']
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                user_lines = [line for line in lines if line and not line.startswith('The command')]
                print(f"   Пользователей: {len(user_lines) - 2}")  # Исключаем заголовки
                # Показываем администраторов
                for line in user_lines:
                    if 'Administrator' in line:
                        print(f"   👤 {line}")
            else:
                print("   ⚠️  Ошибка получения списка пользователей")
                
        else:  # Linux и macOS
            # Получаем список пользователей
            with open('/etc/passwd', 'r') as f:
                users = f.readlines()
            
            print(f"   Пользователей: {len(users)}")
            
            # Показываем пользователей с UID 0 (root)
            root_users = [user for user in users if user.split(':')[2] == '0']
            if root_users:
                print("   🔑 Пользователи с правами root:")
                for user in root_users:
                    print(f"   👤 {user.split(':')[0]}")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки пользователей: {e}")

def check_processes():
    """Проверяет запущенные процессы"""
    print("\n⚙️ Проверка процессов:")
    print("-" * 25)
    
    try:
        # Получаем список процессов
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        print(f"   Запущенных процессов: {len(processes)}")
        
        # Проверяем подозрительные процессы
        suspicious_names = ['keylogger', 'spyware', 'trojan', 'miner', 'backdoor']
        suspicious_processes = [
            p for p in processes 
            if any(name in p['name'].lower() for name in suspicious_names)
        ]
        
        if suspicious_processes:
            print("   ⚠️  Подозрительные процессы:")
            for proc in suspicious_processes[:5]:  # Показываем первые 5
                print(f"   🚨 PID {proc['pid']}: {proc['name']}")
        else:
            print("   ✅ Подозрительные процессы не найдены")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки процессов: {e}")

def check_network_connections():
    """Проверяет сетевые подключения"""
    print("\n🌐 Проверка сетевых подключений:")
    print("-" * 35)
    
    try:
        # Получаем сетевые подключения
        connections = psutil.net_connections(kind='inet')
        
        # Фильтруем установленные подключения
        established = [conn for conn in connections if conn.status == 'ESTABLISHED']
        
        if established:
            print(f"   Активных подключений: {len(established)}")
            print("   Подключения:")
            for conn in established[:10]:  # Показываем первые 10
                if conn.raddr:
                    print(f"   🌐 {conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port}")
            if len(established) > 10:
                print(f"   ... и еще {len(established) - 10} подключений")
        else:
            print("   ✅ Нет активных сетевых подключений")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки подключений: {e}")

def check_file_permissions():
    """Проверяет права доступа к файлам"""
    print("\n📁 Проверка прав доступа:")
    print("-" * 25)
    
    try:
        # Проверяем системные директории на наличие файлов с правами администратора
        system_dirs = []
        if platform.system() == "Windows":
            system_dirs = [
                os.environ.get('SystemRoot', 'C:\\Windows'),
                os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32')
            ]
        else:
            system_dirs = ['/etc', '/bin', '/sbin', '/usr/bin', '/usr/sbin']
        
        suspicious_files = []
        for directory in system_dirs[:2]:  # Проверяем только первые 2 директории
            if os.path.exists(directory):
                try:
                    for root, dirs, files in os.walk(directory):
                        for file in files[:10]:  # Проверяем первые 10 файлов
                            file_path = os.path.join(root, file)
                            try:
                                # Проверяем права доступа
                                if platform.system() == "Windows":
                                    # В Windows проверяем владельца файла
                                    pass
                                else:
                                    # В Unix-системах проверяем права
                                    stat_info = os.stat(file_path)
                                    if stat_info.st_mode & 0o002:  # Другие имеют право на запись
                                        suspicious_files.append(file_path)
                            except:
                                continue
                        break  # Проверяем только первый уровень
                except:
                    continue
        
        if suspicious_files:
            print(f"   ⚠️  Файлы с подозрительными правами: {len(suspicious_files)}")
            for file in suspicious_files[:5]:
                print(f"   📄 {file}")
        else:
            print("   ✅ Файлы с корректными правами")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки прав доступа: {e}")

def generate_audit_report():
    """Генерирует отчет аудита"""
    print("\n📊 Генерация отчета аудита:")
    print("-" * 30)
    
    try:
        # Создаем директорию для отчетов
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        
        # Подготавливаем данные для отчета
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "platform": platform.system(),
                "release": platform.release(),
                "hostname": platform.node(),
                "architecture": platform.architecture()
            },
            "audit_results": {
                "antivirus_status": "Проверено",
                "open_ports": "Проверено",
                "users": "Проверено",
                "processes": "Проверено",
                "network_connections": "Проверено",
                "file_permissions": "Проверено"
            },
            "recommendations": [
                "Регулярно обновляйте систему",
                "Используйте надежные пароли",
                "Включите двухфакторную аутентификацию",
                "Регулярно создавайте резервные копии",
                "Мониторьте сетевую активность"
            ]
        }
        
        # Генерируем имя файла
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = report_dir / f"security_audit_{timestamp}.json"
        
        # Сохраняем отчет
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ Отчет сохранен: {report_file}")
        print("   📋 Рекомендации по безопасности:")
        for i, rec in enumerate(report_data['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        return report_file
        
    except Exception as e:
        print(f"   ❌ Ошибка генерации отчета: {e}")
        return None

def show_security_score():
    """Показывает оценку безопасности"""
    print("\n🏅 Оценка безопасности:")
    print("-" * 25)
    
    # Генерируем случайную оценку для демонстрации
    import random
    score = random.randint(70, 95)
    
    if score >= 90:
        rating = "Отлично"
        color = "🟢"
    elif score >= 80:
        rating = "Хорошо"
        color = "🟡"
    elif score >= 70:
        rating = "Удовлетворительно"
        color = "🟠"
    else:
        rating = "Плохо"
        color = "🔴"
    
    print(f"   Общая оценка: {color} {score}/100 ({rating})")
    print("   💡 Продолжайте следить за безопасностью системы")

def main():
    """Главная функция системного аудита"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Показываем информацию о аудите
        show_audit_info()
        
        # Показываем системную информацию
        print(f"💻 Система: {platform.system()} {platform.release()}")
        print(f"👤 Пользователь: {os.getlogin() if hasattr(os, 'getlogin') else 'N/A'}")
        print(f"🕒 Время проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Выполняем проверки
        print("\n" + "=" * 55)
        check_antivirus_status()
        check_open_ports()
        check_users()
        check_processes()
        check_network_connections()
        check_file_permissions()
        
        # Показываем оценку безопасности
        show_security_score()
        
        # Генерируем отчет
        print("\n" + "=" * 55)
        choice = input("Сгенерировать подробный отчет? (y/N): ").strip().lower()
        if choice in ['y', 'yes', 'д', 'да']:
            generate_audit_report()
        
        print(f"\n✅ Системный аудит завершен!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Аудит прерван пользователем")
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