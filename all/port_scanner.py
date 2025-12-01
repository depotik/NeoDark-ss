import sys
import socket
import threading
import time
from datetime import datetime
import ipaddress

def print_header():
    """Выводит заголовок программы"""
    print("🔍 Сканер портов NeoDark")
    print("=" * 50)

def get_target():
    """Получает цель сканирования от пользователя"""
    print("Введите IP-адрес или доменное имя для сканирования:")
    target = input(">>> ").strip()
    
    if not target:
        print("❌ Цель не указана")
        return None
    
    try:
        # Проверяем, является ли ввод IP-адресом
        ipaddress.ip_address(target)
        return target
    except ValueError:
        try:
            # Пытаемся преобразовать доменное имя в IP
            ip = socket.gethostbyname(target)
            print(f"✅ Домен {target} преобразован в IP: {ip}")
            return ip
        except socket.gaierror:
            print("❌ Неверный IP-адрес или доменное имя")
            return None

def get_port_range():
    """Получает диапазон портов для сканирования"""
    print("\nВыберите диапазон портов:")
    print(" [1] Стандартные порты (1-1024)")
    print(" [2] Зарегистрированные порты (1024-49151)")
    print(" [3] Все порты (1-65535)")
    print(" [4] Пользовательский диапазон")
    
    choice = input("Выберите опцию (1-4): ").strip()
    
    if choice == "1":
        return 1, 1024
    elif choice == "2":
        return 1024, 49151
    elif choice == "3":
        return 1, 65535
    elif choice == "4":
        try:
            start_port = int(input("Начальный порт: "))
            end_port = int(input("Конечный порт: "))
            if 1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port:
                return start_port, end_port
            else:
                print("❌ Неверный диапазон портов")
                return None, None
        except ValueError:
            print("❌ Неверный формат портов")
            return None, None
    else:
        print("❌ Неверный выбор")
        return None, None

def scan_port(target, port, open_ports, lock):
    """Сканирует один порт"""
    try:
        # Создаем сокет
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Таймаут 500 мс
        
        # Пытаемся подключиться
        result = sock.connect_ex((target, port))
        
        # Если результат 0, порт открыт
        if result == 0:
            with lock:
                open_ports.append(port)
                print(f"   🟢 Порт {port} открыт")
        
        sock.close()
    except Exception:
        pass  # Игнорируем ошибки для отдельных портов

def scan_ports(target, start_port, end_port):
    """Сканирует диапазон портов"""
    print(f"\n🚀 Начинаем сканирование {target}:{start_port}-{end_port}")
    print("-" * 50)
    
    open_ports = []
    lock = threading.Lock()
    threads = []
    
    # Получаем информацию о сервисах
    common_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S"
    }
    
    start_time = datetime.now()
    
    # Сканируем порты
    for port in range(start_port, end_port + 1):
        # Создаем поток для сканирования порта
        thread = threading.Thread(target=scan_port, args=(target, port, open_ports, lock))
        threads.append(thread)
        thread.start()
        
        # Ограничиваем количество одновременных потоков
        if len(threads) >= 1000:
            for t in threads:
                t.join()
            threads = []
    
    # Ждем завершения оставшихся потоков
    for thread in threads:
        thread.join()
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Выводим результаты
    print("\n" + "=" * 50)
    print("📊 Результаты сканирования:")
    print(f"   Цель: {target}")
    print(f"   Диапазон: {start_port}-{end_port}")
    print(f"   Открытых портов: {len(open_ports)}")
    print(f"   Время сканирования: {duration.total_seconds():.2f} секунд")
    print("-" * 50)
    
    if open_ports:
        open_ports.sort()
        print("🟢 Открытые порты:")
        for port in open_ports:
            service = common_ports.get(port, "Неизвестно")
            print(f"   Порт {port}: {service}")
    else:
        print("🟡 Открытые порты не найдены")
    
    return open_ports

def show_port_info():
    """Показывает информацию о портах"""
    print("\nℹ️  Информация о портах:")
    print("   Порты делятся на три диапазона:")
    print("   • Системные (0-1023) - требуют привилегий администратора")
    print("   • Зарегистрированные (1024-49151) - пользовательские порты")
    print("   • Динамические (49152-65535) - эфемерные порты")
    print()
    print("   Стандартные сервисы:")
    print("   • 21 - FTP (передача файлов)")
    print("   • 22 - SSH (безопасный шелл)")
    print("   • 23 - Telnet (небезопасный шелл)")
    print("   • 25 - SMTP (почта)")
    print("   • 53 - DNS (доменные имена)")
    print("   • 80 - HTTP (веб)")
    print("   • 443 - HTTPS (безопасный веб)")

def main():
    """Главная функция сканера портов"""
    print_header()
    
    try:
        # Получаем цель сканирования
        target = get_target()
        if not target:
            input("\nНажмите Enter для выхода...")
            return
        
        # Получаем диапазон портов
        start_port, end_port = get_port_range()
        if start_port is None or end_port is None:
            input("\nНажмите Enter для выхода...")
            return
        
        # Сканируем порты
        open_ports = scan_ports(target, start_port, end_port)
        
        # Показываем информацию о портах
        show_port_info()
        
        print(f"\n✅ Сканирование завершено!")
        print(f"⏰ Завершено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Сканирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()