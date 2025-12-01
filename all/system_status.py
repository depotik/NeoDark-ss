import os
import sys
import platform
import psutil
import time
from datetime import datetime

def get_neodark_banner():
    """Возвращает баннер NeoDark из banner.md"""
    return [
        "",
        "",
        "",
        "",
        "",
        "",
        "                                        ███╗   ██╗██████╗ ",
        "                                        ████╗  ██║██╔══██╗",
        "                                        ██╔██╗ ██║██║  ██║",
        "                                        ██║╚██╗██║██║  ██║",
        "                                         ██║ ╚████║██████╔╝",
        "                                         ╚═╝  ╚═══╝╚═════╝ "
    ]

def print_header():
    """Выводит заголовок программы"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Выводим баннер
    banner_lines = get_neodark_banner()
    for line in banner_lines:
        print(f"\033[96m{line}\033[0m")  # Голубой цвет
    
    print("=" * 70)
    print("  Статус системы NeoDark")
    print("=" * 70)

def get_system_info():
    """Получает информацию об операционной системе"""
    print(" Операционная система:")
    
    os_info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    
    print(f"   Название: {os_info['system']}")
    print(f"   Версия: {os_info['release']}")
    print(f"   Сборка: {os_info['version']}")
    print(f"   Компьютер: {os_info['node']}")
    print(f"   Архитектура: {os_info['machine']}")
    if os_info['processor']:
        print(f"   Процессор: {os_info['processor']}")
    print()
    
    return os_info

def get_cpu_info():
    """Получает информацию о процессоре"""
    print(" Процессор:")
    
    try:
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else None,
            "current_frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "cpu_usage": psutil.cpu_percent(interval=1)
        }
        
        print(f"   Физических ядер: {cpu_info['physical_cores']}")
        print(f"   Всего ядер: {cpu_info['total_cores']}")
        
        if cpu_info['max_frequency']:
            print(f"   Макс. частота: {cpu_info['max_frequency']:.2f} MHz")
        if cpu_info['current_frequency']:
            print(f"   Текущая частота: {cpu_info['current_frequency']:.2f} MHz")
            
        print(f"   Использование: {cpu_info['cpu_usage']}%")
        
        # Показать использование по ядрам
        print("   Использование по ядрам:")
        cpu_percents = psutil.cpu_percent(percpu=True, interval=1)
        for i, percent in enumerate(cpu_percents):
            print(f"     Ядро {i}: {percent}%")
            
    except Exception as e:
        print(f"    Ошибка получения информации о CPU: {e}")
    
    print()

def get_memory_info():
    """Получает информацию о памяти"""
    print(" Память:")
    
    try:
        # Физическая память
        svmem = psutil.virtual_memory()
        print(f"   Физическая память:")
        print(f"     Всего: {get_size(svmem.total)}")
        print(f"     Доступно: {get_size(svmem.available)}")
        print(f"     Использовано: {get_size(svmem.used)}")
        print(f"     Процент: {svmem.percent}%")
        
        # Swap память
        swap = psutil.swap_memory()
        print(f"   Swap память:")
        print(f"     Всего: {get_size(swap.total)}")
        print(f"     Свободно: {get_size(swap.free)}")
        print(f"     Использовано: {get_size(swap.used)}")
        print(f"     Процент: {swap.percent}%")
        
    except Exception as e:
        print(f"    Ошибка получения информации о памяти: {e}")
    
    print()

def get_disk_info():
    """Получает информацию о дисках"""
    print(" Диски:")
    
    try:
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"   Диск: {partition.device}")
            print(f"     Точка монтирования: {partition.mountpoint}")
            print(f"     Файловая система: {partition.fstype}")
            
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                print(f"     Всего: {get_size(partition_usage.total)}")
                print(f"     Использовано: {get_size(partition_usage.used)}")
                print(f"     Свободно: {get_size(partition_usage.free)}")
                print(f"     Процент: {partition_usage.percent}%")
            except PermissionError:
                print("      Нет доступа к информации о диске")
            print()
            
    except Exception as e:
        print(f"    Ошибка получения информации о дисках: {e}")
    
    print()

def get_network_info():
    """Получает информацию о сети"""
    print(" Сеть:")
    
    try:
        # Статистика сети
        net_io = psutil.net_io_counters()
        print(f"   Отправлено: {get_size(net_io.bytes_sent)}")
        print(f"   Получено: {get_size(net_io.bytes_recv)}")
        
        # Активные соединения
        connections = psutil.net_connections(kind='inet')
        print(f"   Активные соединения: {len(connections)}")
        
        # Сетевые интерфейсы
        if_addrs = psutil.net_if_addrs()
        print("   Сетевые интерфейсы:")
        for interface_name, interface_addresses in if_addrs.items():
            print(f"     {interface_name}:")
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"       IPv4: {address.address}")
                elif str(address.family) == 'AddressFamily.AF_INET6':
                    print(f"       IPv6: {address.address}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"       MAC: {address.address}")
                    
    except Exception as e:
        print(f"    Ошибка получения информации о сети: {e}")
    
    print()

def get_battery_info():
    """Получает информацию о батарее (для ноутбуков)"""
    if platform.system() == "Windows" or platform.system() == "Darwin":
        try:
            battery = psutil.sensors_battery()
            if battery:
                print(" Батарея:")
                print(f"   Процент заряда: {battery.percent}%")
                print(f"   Подключено к питанию: {'Да' if battery.power_plugged else 'Нет'}")
                if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
                    print(f"   Время работы: Неограниченно")
                elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
                    print(f"   Время работы: Неизвестно")
                else:
                    hours = battery.secsleft // 3600
                    minutes = (battery.secsleft % 3600) // 60
                    print(f"   Время работы: {hours} ч {minutes} мин")
                print()
        except Exception:
            # Батарея не обнаружена или ошибка
            pass

def get_sensors_info():
    """Получает информацию с датчиков системы"""
    try:
        print("  Температура:")
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                print(f"   {name}:")
                for entry in entries:
                    print(f"     {entry.label or name}: {entry.current}°C")
        else:
            print("   Информация о температуре недоступна")
        print()
    except Exception:
        print("  Температура: Информация недоступна")
        print()

def get_boot_time():
    """Получает время загрузки системы"""
    print("  Время работы системы:")
    
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        current_time = datetime.now()
        uptime = current_time - boot_time
        
        print(f"   Загрузка системы: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Время работы: {str(uptime).split('.')[0]}")
        
    except Exception as e:
        print(f"    Ошибка получения времени работы: {e}")
    
    print()

def get_running_processes():
    """Получает информацию о запущенных процессах"""
    print(" Процессы:")
    
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            processes.append(proc.info)
        
        print(f"   Всего процессов: {len(processes)}")
        
        # Самые ресурсоемкие процессы
        print("   Самые ресурсоемкие процессы:")
        processes_sorted = sorted(processes, key=lambda p: p['pid'])[:5]
        for process in processes_sorted:
            print(f"     PID: {process['pid']}, Name: {process['name']}")
            
    except Exception as e:
        print(f"    Ошибка получения информации о процессах: {e}")
    
    print()

def get_size(bytes, suffix="B"):
    """Масштабирует байты в удобочитаемый формат"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def print_system_status():
    """Выводит статус системы в улучшенном формате"""
    # Получаем баннер
    banner_lines = get_neodark_banner()
    
    # Получаем системную информацию
    sys_info = get_system_info()
    
    # Подготавливаем левую панель с информацией
    left_panel = [
        f" Хост: {platform.node()}",
        f"  ОС: {platform.system()} {platform.release()}",
        f" ЦП: {platform.processor() or 'Не определен'}",
        f" Ядра: {psutil.cpu_count(logical=False)} физ. / {psutil.cpu_count(logical=True)} лог.",
        f" Загрузка ЦП: {psutil.cpu_percent(interval=1)}%",
    ]
    
    # Добавляем информацию о памяти
    try:
        memory = psutil.virtual_memory()
        left_panel.append(f" Память: {get_size(memory.used)}/{get_size(memory.total)}")
        left_panel.append(f" Память %: {memory.percent}%")
    except:
        left_panel.append(" Память: Ошибка получения")
    
    # Добавляем информацию о диске
    try:
        disk = psutil.disk_usage('/')
        left_panel.append(f" Диск: {get_size(disk.used)}/{get_size(disk.total)}")
        left_panel.append(f" Диск %: {round(disk.percent, 1)}%")
    except:
        left_panel.append(" Диск: Ошибка получения")
    
    # Добавляем информацию о сети
    try:
        net_info = psutil.net_io_counters()
        left_panel.append(f" Сеть: ↑ {get_size(net_info.bytes_sent)} ↓ {get_size(net_info.bytes_recv)}")
    except:
        left_panel.append(" Сеть: Ошибка получения")
    
    # Добавляем информацию о времени работы
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        left_panel.append(f"  Аптайм: {str(uptime).split('.')[0]}")
    except:
        left_panel.append("  Аптайм: Ошибка получения")
    
    # Подготавливаем правую панель с логотипом
    right_panel = banner_lines
    
    # Подготавливаем нижний колонтитул
    footer = f"NeoDark System Status | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Определяем максимальную ширину для красивого отображения
    max_left_width = max(len(line) for line in left_panel) if left_panel else 0
    panel_separator = "  │  "
    
    # Выводим заголовок
    print("=" * 80)
    print(" " * 30 + "СТАТУС СИСТЕМЫ")
    print("=" * 80)
    
    # Выводим панели
    max_lines = max(len(left_panel), len(right_panel))
    
    for i in range(max_lines):
        left = left_panel[i] if i < len(left_panel) else ""
        right = right_panel[i] if i < len(right_panel) else ""
        
        # Форматируем строку с панелями
        if i < len(left_panel) and i < len(right_panel):
            print(f"{left:<35}{panel_separator}\033[96m{right}\033[0m")
        elif i < len(left_panel):
            print(f"{left:<35}{panel_separator}")
        elif i < len(right_panel):
            print(f"{' ':<35}{panel_separator}\033[96m{right}\033[0m")
    
    # Разделитель
    print("-" * 80)
    
    # Выводим нижний колонтитул
    print(footer.center(80))
    print("=" * 80)

def main():
    """Главная функция отображения статуса системы"""
    # Проверяем, какой режим использовать
    if len(sys.argv) > 1 and sys.argv[1] == "--simple":
        # Простой режим (как было раньше)
        print_header()
        
        try:
            # Получаем информацию о системе
            get_system_info()
            get_boot_time()
            get_cpu_info()
            get_memory_info()
            get_disk_info()
            get_network_info()
            get_battery_info()
            get_sensors_info()
            get_running_processes()
            
            print(" Получение статуса системы завершено!")
            print()
            print(f" Данные актуальны на: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except KeyboardInterrupt:
            print("\n\n  Получение статуса было прервано пользователем")
        except Exception as e:
            print(f"\n Произошла ошибка при получении статуса системы: {str(e)}")
    else:
        # Улучшенный режим (новый формат)
        # Очищаем экран
        os.system('cls' if os.name == 'nt' else 'clear')
        
        try:
            print_system_status()
        except KeyboardInterrupt:
            print("\n\n  Просмотр статуса был прерван пользователем")
        except Exception as e:
            print(f"\n Произошла ошибка: {str(e)}")
    
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