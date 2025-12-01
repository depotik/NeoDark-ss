import os
import time
import sys
import re
import subprocess
from internetspeedtest import SpeedTest

# Определяем color_code в начале файла
color_code = {
    "reset": "\033[0m",  
    "underline": "\033[04m", 
    "green": "\033[32m",     
    "yellow": "\033[93m",    
    "red": "\033[31m",       
    "cyan": "\033[36m",     
    "bold": "\033[01m",        
    "pink": "\033[95m",
    "url_l": "\033[36m",       
    "li_g": "\033[92m",      
    "f_cl": "\033[0m",
    "dark": "\033[90m",     
    "blue": "\033[94m",
    "orange": "\033[33m",
}

def center_text(text, width=80):
    """Функция для центрирования текста"""
    lines = text.split('\n')
    centered_lines = []
    for line in lines:
        clean_line = re.sub(r'\033\[[0-9;]*m', '', line)
        padding = (width - len(clean_line)) // 2
        centered_lines.append(' ' * padding + line)
    return '\n'.join(centered_lines)

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    """Создание прогресс-бара"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{color_code["cyan"]}{bar}{color_code["reset"]}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()

def format_speed(speed):
    """Форматирование скорости в читаемый вид"""
    if speed > 100:  # > 100 Мбит/с
        return f"{speed:.2f} Мбит/с"
    elif speed > 1:   # > 1 Мбит/с
        return f"{speed:.2f} Мбит/с"
    else:
        return f"{speed * 1000:.2f} Кбит/с"

def get_server_info(server):
    """Безопасное получение информации о сервере"""
    try:
        name = getattr(server, 'name', 'Неизвестно')
        # Пробуем разные возможные атрибуты для местоположения
        location = getattr(server, 'location', 
                  getattr(server, 'city', 
                  getattr(server, 'country', 'Неизвестно')))
        return name, location
    except Exception:
        return "Неизвестно", "Неизвестно"

def test_download_speed_internetspeedtest(st, server):
    """Тест скорости скачивания с прогресс-баром"""
    print(f"\n{color_code['yellow']}🠗 Тестирование скорости СКАЧИВАНИЯ...{color_code['reset']}")
    for i in range(101):
        time.sleep(0.03)
        print_progress_bar(i, 100, prefix='Прогресс:', suffix='Завершено', length=40)
    
    try:
        # Получаем результат и проверяем тип
        result = st.download(server)
        print(f"{color_code['dark']}🚀 Starting Download test...{color_code['reset']}")
        
        # Обрабатываем разные форматы возвращаемых данных
        if isinstance(result, tuple):
            # Если возвращается кортеж, берем первый элемент
            download_speed = result[0] / 1000000  # Конвертируем в Мбит/с
        else:
            # Если возвращается число
            download_speed = result / 1000000  # Конвертируем в Мбит/с
            
        print(f"{color_code['green']}✓ Скорость скачивания: {color_code['bold']}{download_speed:.2f} Мбит/с{color_code['reset']}")
        return download_speed
    except Exception as e:
        print(f"{color_code['red']}❌ Ошибка теста скачивания: {str(e)}{color_code['reset']}")
        print(f"{color_code['dark']}Тип результата: {type(result)}, Значение: {result}{color_code['reset']}")
        return 0

def test_upload_speed_internetspeedtest(st, server):
    """Тест скорости загрузки с прогресс-баром"""
    print(f"\n{color_code['yellow']}🠕 Тестирование скорости ЗАГРУЗКИ...{color_code['reset']}")
    for i in range(101):
        time.sleep(0.03)
        print_progress_bar(i, 100, prefix='Прогресс:', suffix='Завершено', length=40)
    
    try:
        # Получаем результат и проверяем тип
        result = st.upload(server)
        print(f"{color_code['dark']}🚀 Starting Upload test...{color_code['reset']}")
        
        # Обрабатываем разные форматы возвращаемых данных
        if isinstance(result, tuple):
            # Если возвращается кортеж, берем первый элемент
            upload_speed = result[0] / 1000000  # Конвертируем в Мбит/с
        else:
            # Если возвращается число
            upload_speed = result / 1000000  # Конвертируем в Мбит/с
            
        print(f"{color_code['green']}✓ Скорость загрузки: {color_code['bold']}{upload_speed:.2f} Мбит/с{color_code['reset']}")
        return upload_speed
    except Exception as e:
        print(f"{color_code['red']}❌ Ошибка теста загрузки: {str(e)}{color_code['reset']}")
        print(f"{color_code['dark']}Тип результата: {type(result)}, Значение: {result}{color_code['reset']}")
        return 0

def test_ping_internetspeedtest(st, server):
    """Тест пинга"""
    print(f"\n{color_code['yellow']}🔄 Тестирование ПИНГА...{color_code['reset']}")
    for i in range(101):
        time.sleep(0.02)
        print_progress_bar(i, 100, prefix='Прогресс:', suffix='Завершено', length=40)
    
    try:
        ping_result = st.ping(server)
        
        # Обрабатываем разные форматы возвращаемых данных для ping
        if isinstance(ping_result, tuple):
            # Если возвращается кортеж (ping, jitter)
            ping = ping_result[0]
            jitter = ping_result[1] if len(ping_result) > 1 else 0
        else:
            # Если возвращается только ping
            ping = ping_result
            jitter = 0
            
        print(f"{color_code['green']}✓ Пинг: {color_code['bold']}{ping:.2f} ms{color_code['reset']}")
        if jitter > 0:
            print(f"{color_code['green']}✓ Джиттер: {color_code['bold']}{jitter:.2f} ms{color_code['reset']}")
        return ping, jitter
    except Exception as e:
        print(f"{color_code['red']}❌ Ошибка теста пинга: {str(e)}{color_code['reset']}")
        return 0, 0

def debug_speedtest_methods():
    """Функция для отладки - показывает какие методы доступны и что они возвращают"""
    try:
        st = SpeedTest()
        servers = st.get_servers()
        if servers:
            best_server = st.find_best_server(servers)
            server_name, server_location = get_server_info(best_server)
            print(f"{color_code['cyan']}🔧 Отладочная информация:{color_code['reset']}")
            print(f"{color_code['dark']}Сервер: {server_name}{color_code['reset']}")
            
            # Тестируем методы
            print(f"{color_code['dark']}Тестируем ping...{color_code['reset']}")
            ping_result = st.ping(best_server)
            print(f"{color_code['dark']}Ping результат: {ping_result} (тип: {type(ping_result)}){color_code['reset']}")
            
            print(f"{color_code['dark']}Тестируем download...{color_code['reset']}")
            download_result = st.download(best_server)
            print(f"{color_code['dark']}Download результат: {download_result} (тип: {type(download_result)}){color_code['reset']}")
            
            print(f"{color_code['dark']}Тестируем upload...{color_code['reset']}")
            upload_result = st.upload(best_server)
            print(f"{color_code['dark']}Upload результат: {upload_result} (тип: {type(upload_result)}){color_code['reset']}")
            
        return True
    except Exception as e:
        print(f"{color_code['red']}❌ Ошибка отладки: {str(e)}{color_code['reset']}")
        return False

def full_speed_test():
    """Полный тест скорости (комбо)"""
    print(f"\n{color_code['cyan']}{color_code['bold']}🚀 Запуск полного теста скорости через LibreSpeed...{color_code['reset']}")
    
    try:
        # Инициализация SpeedTest
        st = SpeedTest()
        print(f"{color_code['dark']}⏳ Получение списка серверов...{color_code['reset']}")
        
        # Получаем серверы
        servers = st.get_servers()
        if not servers:
            print(f"{color_code['red']}❌ Не удалось получить список серверов{color_code['reset']}")
            return False
        
        print(f"{color_code['dark']}🔍 Поиск лучшего сервера...{color_code['reset']}")
        best_server = st.find_best_server(servers)
        
        # Безопасное получение информации о сервере
        server_name, server_location = get_server_info(best_server)
        
        print(f"{color_code['green']}✓ Выбран сервер: {color_code['bold']}{server_name}{color_code['reset']}")
        print(f"{color_code['dark']}📍 Местоположение: {server_location}{color_code['reset']}")
        
        # Тест пинга
        ping_result, jitter_result = test_ping_internetspeedtest(st, best_server)
        
        # Тест скачивания
        download_speed = test_download_speed_internetspeedtest(st, best_server)
        
        # Тест загрузки
        upload_speed = test_upload_speed_internetspeedtest(st, best_server)
        
        # Результаты
        print(f"\n{color_code['bold']}{color_code['cyan']}📊 РЕЗУЛЬТАТЫ ТЕСТА:{color_code['reset']}")
        print(f"{color_code['green']}┌{'─' * 50}┐{color_code['reset']}")
        print(f"{color_code['green']}│{color_code['reset']} 🠗 Скорость скачивания: {color_code['bold']}{download_speed:>7.2f} Мбит/с{color_code['reset']}{color_code['green']} │{color_code['reset']}")
        print(f"{color_code['green']}│{color_code['reset']} 🠕 Скорость загрузки:   {color_code['bold']}{upload_speed:>7.2f} Мбит/с{color_code['reset']}{color_code['green']} │{color_code['reset']}")
        print(f"{color_code['green']}│{color_code['reset']} 📍 Пинг:               {color_code['bold']}{ping_result:>7.2f} ms{color_code['reset']}{color_code['green']} │{color_code['reset']}")
        if jitter_result > 0:
            print(f"{color_code['green']}│{color_code['reset']} 📊 Джиттер:           {color_code['bold']}{jitter_result:>7.2f} ms{color_code['reset']}{color_code['green']} │{color_code['reset']}")
        print(f"{color_code['green']}└{'─' * 50}┘{color_code['reset']}")
        
        return True
        
    except Exception as e:
        print(f"\n{color_code['red']}❌ Ошибка теста скорости: {str(e)}{color_code['reset']}")
        print(f"{color_code['yellow']}💡 Советы по устранению:{color_code['reset']}")
        print(f"{color_code['dark']}• Проверьте подключение к интернету")
        print(f"• Убедитесь, что библиотека internetspeedtest установлена")
        print(f"• Попробуйте запустить тест позже{color_code['reset']}")
        
        # Предлагаем отладку
        print(f"\n{color_code['yellow']}🐛 Хотите запустить отладку? (y/n): {color_code['reset']}")
        if input().strip().lower() == 'y':
            debug_speedtest_methods()
        
        return False

def single_download_test():
    """Тест только скорости скачивания"""
    try:
        st = SpeedTest()
        servers = st.get_servers()
        best_server = st.find_best_server(servers)
        
        server_name, server_location = get_server_info(best_server)
        print(f"{color_code['green']}✓ Сервер: {server_name}{color_code['reset']}")
        download_speed = test_download_speed_internetspeedtest(st, best_server)
        return download_speed
    except Exception as e:
        print(f"{color_code['red']}❌ Ошибка: {str(e)}{color_code['reset']}")
        return 0

def single_upload_test():
    """Тест только скорости загрузки"""
    try:
        st = SpeedTest()
        servers = st.get_servers()
        best_server = st.find_best_server(servers)
        
        server_name, server_location = get_server_info(best_server)
        print(f"{color_code['green']}✓ Сервер: {server_name}{color_code['reset']}")
        upload_speed = test_upload_speed_internetspeedtest(st, best_server)
        return upload_speed
    except Exception as e:
        print(f"{color_code['red']}❌ Ошибка: {str(e)}{color_code['reset']}")
        return 0

def single_ping_test():
    """Тест только пинга"""
    try:
        st = SpeedTest()
        servers = st.get_servers()
        best_server = st.find_best_server(servers)
        
        server_name, server_location = get_server_info(best_server)
        print(f"{color_code['green']}✓ Сервер: {server_name}{color_code['reset']}")
        ping, jitter = test_ping_internetspeedtest(st, best_server)
        return ping, jitter
    except Exception as e:
        print(f"{color_code['red']}❌ Ошибка: {str(e)}{color_code['reset']}")
        return 0, 0

def display_menu():
    """Отображение меню"""
    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = 80

    # Баннер
    banner_content = f'''
{color_code['cyan']}
███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ 
██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
{color_code['reset']}
{color_code['yellow']}⚡ SpeedTest CLI | Creator: @weeaave
{color_code['dark']}Special for NeoDark Ecosystem | LibreSpeed{color_code['reset']}
'''
    
    banner = center_text(banner_content, terminal_width)
    print(banner)
    
    # Меню (не центрированное)
    menu = f'''
{color_code['bold']}{color_code['cyan']}🎯 ВЫБЕРИТЕ ТИП ТЕСТА:{color_code['reset']}

{color_code['yellow']}[1]{color_code['reset']} 🠗  Тест скорости СКАЧИВАНИЯ
{color_code['yellow']}[2]{color_code['reset']} 🠕  Тест скорости ЗАГРУЗКИ  
{color_code['yellow']}[3]{color_code['reset']} 📍  Тест ПИНГА
{color_code['yellow']}[4]{color_code['reset']} 🚀  ПОЛНЫЙ ТЕСТ (все параметры)
{color_code['yellow']}[5]{color_code['reset']} 🐛  ОТЛАДКА (показать типы данных)
{color_code['yellow']}[0]{color_code['reset']} ❌  ВЫХОД

{color_code['cyan']}Ваш выбор: {color_code['reset']}'''
    
    print(menu)

def exit_program():
    """Выход из программы с запуском main.py"""
    print(f"\n{color_code['green']}👋 До свидания!{color_code['reset']}")
    
    # Ожидание 4 секунды
    for i in range(4, 0, -1):
        print(f"{color_code['dark']}Возврат через {i} сек...{color_code['reset']}", end='\r')
        time.sleep(1)
    
    # Очистка консоли
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Запуск main.py
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_py_path = os.path.join(script_dir, '../main.py')
        
        if os.path.exists(main_py_path):
            subprocess.run([sys.executable, main_py_path])
        else:
            # Если ../main.py не найден, ищем в текущей директории
            main_py_current = os.path.join(script_dir, 'main.py')
            if os.path.exists(main_py_current):
                subprocess.run([sys.executable, main_py_current])
            else:
                print(f"{color_code['red']}Файл main.py не найден{color_code['reset']}")
    except Exception as e:
        print(f"{color_code['red']}Ошибка при запуске main.py: {e}{color_code['reset']}")
    
    sys.exit(0)

def main():
    """Основная функция"""
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            display_menu()
            choice = input().strip()
            
            if choice == '1':
                single_download_test()
                
            elif choice == '2':
                single_upload_test()
                
            elif choice == '3':
                single_ping_test()
                
            elif choice == '4':
                full_speed_test()
                
            elif choice == '5':
                debug_speedtest_methods()
                input(f"\n{color_code['dark']}Нажмите Enter для продолжения...{color_code['reset']}")
                continue
                
            elif choice == '0':
                exit_program()
                break
                
            else:
                print(f"\n{color_code['red']}❌ Ошибка: введите цифру от 0 до 5!{color_code['reset']}")
            
            # Пауза перед следующим выбором
            if choice != '0':
                input(f"\n{color_code['dark']}Нажмите Enter для продолжения...{color_code['reset']}")
                
        except KeyboardInterrupt:
            print(f"\n\n{color_code['red']}🚫 Программа прервана пользователем{color_code['reset']}")
            exit_program()
            break
        except Exception as e:
            print(f"\n{color_code['red']}❌ Критическая ошибка: {str(e)}{color_code['reset']}")
            input(f"{color_code['dark']}Нажмите Enter для продолжения...{color_code['reset']}")

if __name__ == "__main__":
    main()