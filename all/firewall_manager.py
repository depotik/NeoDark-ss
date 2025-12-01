import os
import sys
import platform
import subprocess
import json
from datetime import datetime
from pathlib import Path

def print_header():
    """Выводит заголовок программы"""
    print("🛡️ Управление брандмауэром NeoDark")
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

def show_firewall_info():
    """Показывает информацию о брандмауэре"""
    print("ℹ️ Управление брандмауэром NeoDark:")
    print("-" * 40)
    print("   Брандмауэр защищает вашу систему от")
    print("   несанкционированного доступа из сети.")
    print()
    print("   Возможности:")
    print("   • Просмотр правил брандмауэра")
    print("   • Добавление/удаление правил")
    print("   • Блокировка/разблокировка портов")
    print("   • Управление приложениями")
    print("   • Логирование сетевой активности")
    print()

def get_firewall_status():
    """Получает статус брандмауэра"""
    print("🔍 Статус брандмауэра:")
    print("-" * 30)
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # Проверяем статус брандмауэра Windows
            cmd = ['netsh', 'advfirewall', 'show', 'allprofiles']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   Статус профилей:")
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'State' in line or 'Состояние' in line:
                        print(f"   {line}")
                return True
            else:
                print(f"   ⚠️  Ошибка получения статуса: {result.stderr}")
                return False
                
        elif system == "Linux":
            # Проверяем различные брандмауэры в Linux
            firewalls = [
                {'name': 'ufw', 'status_cmd': ['ufw', 'status']},
                {'name': 'firewalld', 'status_cmd': ['systemctl', 'status', 'firewalld']},
                {'name': 'iptables', 'status_cmd': ['iptables', '-L', '-n']}
            ]
            
            found_firewall = False
            for fw in firewalls:
                try:
                    result = subprocess.run(fw['status_cmd'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print(f"   ✅ Найден {fw['name']}")
                        found_firewall = True
                        # Показываем краткий статус
                        lines = result.stdout.strip().split('\n')
                        for i, line in enumerate(lines[:5]):  # Показываем первые 5 строк
                            print(f"   {line}")
                        if len(lines) > 5:
                            print("   ...")
                        break
                except subprocess.TimeoutExpired:
                    print(f"   ⏱️  Таймаут проверки {fw['name']}")
                except FileNotFoundError:
                    continue
                except Exception as e:
                    print(f"   ⚠️  Ошибка проверки {fw['name']}: {e}")
            
            if not found_firewall:
                print("   ⚠️  Не найдено активных брандмауэров")
                print("   💡 Установите ufw, firewalld или настройте iptables")
            
            return found_firewall
            
        elif system == "Darwin":  # macOS
            # Проверяем статус через systemsetup
            result = subprocess.run(['systemsetup', '-getfirewall'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   {result.stdout.strip()}")
                return True
            else:
                print(f"   ⚠️  Ошибка получения статуса: {result.stderr}")
                return False
        else:
            print("❌ Неподдерживаемая система")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def show_firewall_rules():
    """Показывает правила брандмауэра"""
    print("\n📋 Правила брандмауэра:")
    print("-" * 30)
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # Показываем правила брандмауэра Windows
            cmd = ['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all']
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                print(f"   Найдено правил: {len([l for l in lines if 'Rule Name:' in l or 'Имя правила:' in l])}")
                # Показываем первые 10 правил
                for line in lines[:20]:
                    if 'Rule Name:' in line or 'Имя правила:' in line:
                        print(f"   🔥 {line}")
            else:
                print(f"   ⚠️  Ошибка получения правил: {result.stderr}")
                
        elif system == "Linux":
            # Показываем правила iptables
            result = subprocess.run(['iptables', '-L', '-n', '-v'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                print("   Активные цепочки:")
                for line in lines[:15]:  # Показываем первые 15 строк
                    print(f"   {line}")
            else:
                print("   ⚠️  Ошибка получения правил iptables")
                
        elif system == "Darwin":  # macOS
            # Показываем правила pf (Packet Filter)
            result = subprocess.run(['pfctl', '-sr'], capture_output=True, text=True)
            if result.returncode == 0:
                if result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    print("   Активные правила:")
                    for line in lines[:10]:  # Показываем первые 10 строк
                        print(f"   {line}")
                else:
                    print("   Нет активных правил")
            else:
                print("   ⚠️  Ошибка получения правил pf")
                
    except Exception as e:
        print(f"   ❌ Ошибка получения правил: {e}")

def show_firewall_tips():
    """Показывает советы по настройке брандмауэра"""
    print("\n💡 Советы по настройке брандмауэра:")
    print("-" * 40)
    print("   1. Всегда включайте брандмауэр")
    print("   2. Блокируйте неиспользуемые порты")
    print("   3. Разрешайте только необходимые соединения")
    print("   4. Регулярно проверяйте правила")
    print("   5. Используйте логирование для мониторинга")
    print("   6. Обновляйте правила при изменении конфигурации")
    print("   7. Тестируйте изменения в безопасной среде")
    print("   8. Делайте резервные копии конфигураций")

def main():
    """Главная функция управления брандмауэром"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Показываем информацию о брандмауэре
        show_firewall_info()
        
        # Определяем систему
        system = platform.system()
        print(f"💻 Обнаружена система: {system}")
        
        # Получаем статус брандмауэра
        get_firewall_status()
        
        # Показываем правила
        show_firewall_rules()
        
        # Показываем советы
        show_firewall_tips()
        
        print(f"\n✅ Работа с брандмауэром завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Работа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()