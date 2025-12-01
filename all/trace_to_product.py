import os
import sys
import platform
import subprocess
import time
from datetime import datetime
import socket
import struct

def print_header():
    """Выводит заголовок программы"""
    print("🔍 Трассировка до продукта NeoDark")
    print("=" * 50)

def get_target_host():
    """Получает целевой хост для трассировки"""
    print("Выберите продукт для трассировки:")
    print(" [1] NeoDark Core Server (core.neodark.ru)")
    print(" [2] NeoDark Update Server (update.neodark.ru)")
    print(" [3] NeoDark Cloud Services (cloud.neodark.ru)")
    print(" [4] Ввести свой адрес")
    print()
    
    choice = input("Выберите опцию (1-4): ").strip()
    
    hosts = {
        '1': 'core.neodark.ru',
        '2': 'update.neodark.ru',
        '3': 'cloud.neodark.ru'
    }
    
    if choice in hosts:
        return hosts[choice]
    elif choice == '4':
        host = input("Введите адрес хоста: ").strip()
        if host:
            return host
        else:
            print("❌ Адрес хоста не может быть пустым")
            return None
    else:
        print("❌ Неверный выбор")
        return None

def trace_route_windows(host, max_hops=30):
    """Выполняет трассировку маршрута в Windows"""
    print(f"🔍 Трассировка маршрута к {host} (максимум {max_hops} прыжков):")
    print()
    
    try:
        # Используем встроенную команду tracert
        cmd = ["tracert", "-h", str(max_hops), host]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='cp866'  # Кодировка для Windows командной строки
        )
        
        # Читаем вывод построчно
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Проверяем код возврата
        rc = process.poll()
        if rc != 0:
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"❌ Ошибка: {stderr_output}")
                
        return rc == 0
        
    except FileNotFoundError:
        print("❌ Команда tracert не найдена")
        return False
    except Exception as e:
        print(f"❌ Ошибка при выполнении трассировки: {e}")
        return False

def trace_route_unix(host, max_hops=30):
    """Выполняет трассировку маршрута в Unix-системах"""
    print(f"🔍 Трассировка маршрута к {host} (максимум {max_hops} прыжков):")
    print()
    
    try:
        # Используем встроенную команду traceroute
        cmd = ["traceroute", "-m", str(max_hops), host]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Читаем вывод построчно
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Проверяем код возврата
        rc = process.poll()
        if rc != 0:
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"❌ Ошибка: {stderr_output}")
                
        return rc == 0
        
    except FileNotFoundError:
        print("❌ Команда traceroute не найдена")
        print("💡 Установите traceroute: sudo apt install traceroute (Debian/Ubuntu)")
        return False
    except Exception as e:
        print(f"❌ Ошибка при выполнении трассировки: {e}")
        return False

def trace_route_python(host, max_hops=30):
    """Выполняет трассировку маршрута с помощью Python (упрощенная версия)"""
    print(f"🔍 Трассировка маршрута к {host} (максимум {max_hops} прыжков):")
    print("(Имитация, так как прямая реализация требует привилегий root)")
    print()
    
    try:
        # Пытаемся получить IP-адрес хоста
        ip = socket.gethostbyname(host)
        print(f"✅ Хост {host} разрешен в IP: {ip}")
        print()
        
        # Имитируем трассировку
        print("_hop_   _ip_address___________   _hostname____________   _time_")
        for i in range(1, min(10, max_hops + 1)):
            # Имитируем задержки
            time.sleep(0.1)
            
            # Для демонстрации покажем разные IP
            fake_ip = f"192.168.{i}.{i*2}"
            fake_host = f"router{i}.isp.net" if i < 5 else f"core{i-4}.backbone.net"
            fake_time = f"{i*2}.{i:02d} ms"
            
            print(f"{i:2d}      {fake_ip:20s}   {fake_host:20s}   {fake_time}")
            
            # Если достигли целевого хоста
            if i == 8:
                print(f"✅ Достигнут целевой хост {host} ({ip})")
                break
                
        return True
        
    except socket.gaierror as e:
        print(f"❌ Ошибка разрешения имени хоста: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при выполнении трассировки: {e}")
        return False

def show_trace_info():
    """Показывает информацию о трассировке"""
    print("\nℹ️  Что такое трассировка маршрута:")
    print("   Трассировка маршрута (traceroute) - это сетевая диагностика,")
    print("   которая показывает путь, который проходят пакеты данных")
    print("   от вашего компьютера до целевого хоста.")
    print()
    print("📊 Как читать результаты:")
    print("   • Каждая строка представляет собой прыжок (hop) в сети")
    print("   • Показывается IP-адрес и имя хоста каждого узла")
    print("   • Время отклика в миллисекундах (обычно 3 попытки)")
    print("   • Звездочки (*) означают отсутствие ответа от узла")
    print()
    print("🛠️  Когда использовать:")
    print("   • Диагностика сетевых проблем")
    print("   • Определение местоположения задержек")
    print("   • Проверка доступности сервисов")
    print()

def main():
    """Главная функция трассировки"""
    print_header()
    
    try:
        # Получаем целевой хост
        target_host = get_target_host()
        if not target_host:
            input("\nНажмите Enter для выхода...")
            return
        
        print(f"\n🎯 Целевой хост: {target_host}")
        print("=" * 50)
        
        # Выполняем трассировку в зависимости от ОС
        system = platform.system()
        success = False
        
        if system == "Windows":
            print("🖥️  Обнаружена Windows система")
            success = trace_route_windows(target_host)
        elif system in ["Linux", "Darwin"]:
            print(f"🖥️  Обнаружена {system} система")
            success = trace_route_unix(target_host)
        else:
            print("⚠️  Неизвестная система, используем Python-реализацию")
            success = trace_route_python(target_host)
        
        if success:
            print(f"\n✅ Трассировка завершена!")
        else:
            print(f"\n⚠️  Трассировка завершена с ошибками")
        
        # Показываем информацию о трассировке
        show_trace_info()
        
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Трассировка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()