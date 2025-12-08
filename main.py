import os
import sys
import time
import subprocess
import ctypes
import re  # ← ПЕРЕМЕСТИТЬ В НАЧАЛО!
from pathlib import Path

# Установка заголовка окна
try:
    ctypes.windll.kernel32.SetConsoleTitleW("NeoDark-CLI")
except:
    pass

# Цветовая схема NeoDark
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # Основные цвета
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Яркие цвета
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # NeoDark специальные
    NEO_BLUE = "\033[38;5;75m"
    NEO_PURPLE = "\033[38;5;99m"
    NEO_CYAN = "\033[38;5;51m"
    NEO_GREEN = "\033[38;5;118m"
    NEO_ORANGE = "\033[38;5;208m"
    NEO_PINK = "\033[38;5;205m"

# =============================================================================
# ПЕРЕМЕННЫЕ С ФАЙЛАМИ ДЛЯ КАЖДОЙ ФУНКЦИИ
# =============================================================================

# 🏠 Основные функции
FILES_MAIN = {
    "0": "exit_handler.py",
    "1": "switch_to_gui.py",
    "2": "sync_products.py",
    "3": "system_status.py",
    "4": "enable_autostart.py",
    "6": "check_updates_cli.py",
    "8": "minimal_resources.py"
}

# 🧹 Обслуживание и Утилиты
FILES_MAINTENANCE = {
    "10": "snoser.py",
    "11": "clear_cache.py",
    "12": "enable_zapret.py",
    "13": "join_neodark_edu.py",
    "14": "cpu_benchmark_light.py",
    "16": "sleep_mode_products.py",
    "17": "port_scanner.py",
    "18": "disable_telemetry.py"
}

# 💾 Конфигурация и Данные
FILES_CONFIG = {
    "20": "system_config_data.py",
    "21": "optimize_system.py",
    "23": "low_disk_mode.py",
    "24": "hide_console.py",
    "25": "desktop_setup.py",
    "26": "task_scheduler.py",
    "27": "firewall_management.py",
    "28": "system_audit.py"
}

# 🚀 Сетевые и Агентские функции
FILES_NETWORK = {
    "30": "matrix_rain.py",
    "31": "st.py",
    "32": "neoprai_agent.py",
    "33": "check_ip_reputation.py",
    "34": "show_ip_geolocation.py",
    "35": "trace_to_product.py",
    "39": "file_search_grep.py"

}

# 🔑 Аккаунты и Взаимодействие
FILES_ACCOUNTS = {
    "40": "login_account.py",
    "41": "change_password.py",
    "42": "create_guest_account.py",
    "43": "check_sessions.py",
    "44": "block_products.py",
    "46": "reset_profile.py",
    "47": "setup_backup.py",
    "48": "view_history.py",
    "49": "clear_cloud_config.py"
}

# 🧑‍💻 Инструменты разработчика
FILES_DEVELOPER = {
    "51": "add_custom_script.py",
    "52": "process_list_advanced.py",
    "53": "environment_variables.py",
    "56": "file_patch_demo.py",
    "67": "hotkey_manager.py",
    "68": "product_authenticity.py",
    "69": "launcherDPI.py"
}

# ✨ Развлечения и Визуализация
FILES_ENTERTAINMENT = {
    "60": "fake_bsod.py",
    "61": "logo_animation.py",
    "62": "keyboard_test.py",
    "63": "consPlayer/musicplayer.py",
    "66": "resource_monitor.py"
}

# Объединяем все файлы в один словарь для удобства
ALL_FILES = {}
ALL_FILES.update(FILES_MAIN)
ALL_FILES.update(FILES_MAINTENANCE)
ALL_FILES.update(FILES_CONFIG)
ALL_FILES.update(FILES_NETWORK)
ALL_FILES.update(FILES_ACCOUNTS)
ALL_FILES.update(FILES_DEVELOPER)
ALL_FILES.update(FILES_ENTERTAINMENT)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 120

def print_centered(text):
    width = get_terminal_width()
    clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
    padding = (width - len(clean_text)) // 2
    print(' ' * padding + text)

def print_header():
    """Выводит заголовок приложения в стиле из banner.md"""
    header_content = f'''
{Colors.NEO_CYAN}
███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ 
██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
{Colors.RESET}
{Colors.BRIGHT_YELLOW} NeoDark-CLI | Creator: @weeaave
{Colors.BRIGHT_BLACK}Special for NeoDark Ecosystem | NeoDark{Colors.RESET}
'''
    
    # Разбиваем заголовок на строки и печатаем центрированно
    for line in header_content.split('\n'):
        if line.strip():  # Печатаем только непустые строки
            print_centered(line)
    print()  # Пустая строка после заголовка

def format_menu_line(left_num, left_desc, right_num, right_desc, box_width):
    """Форматирует строку для двух колонок без рамок"""
    left_part = f"{Colors.NEO_CYAN}[{left_num:>2}]{Colors.RESET} {left_desc}" if left_num else ""
    right_part = f"{Colors.NEO_CYAN}[{right_num:>2}]{Colors.RESET} {right_desc}" if right_num else ""
    
    if left_part and right_part:
        # Обе колонки заполнены
        line = f"{left_part:<35} {right_part}"
    elif left_part:
        # Только левая колонка
        line = f"{left_part}"
    elif right_part:
        # Только правая колонка
        line = f"{' ' * 35} {right_part}"
    else:
        # Пустая строка
        line = ""
    
    return line

def print_two_columns(items, section_color, section_title):
    """Вывод двух колонок меню без рамок"""
    # Печатаем заголовок секции без рамки
    print_centered(f"{section_color}{Colors.BOLD}{section_title}{Colors.RESET}")
    print_centered(f"{section_color}{'─' * 50}{Colors.RESET}")
    
    # Разделяем элементы на две колонки
    mid_point = (len(items) + 1) // 2  # Округляем вверх
    left_column = items[:mid_point]
    right_column = items[mid_point:]
    
    max_lines = max(len(left_column), len(right_column))
    
    # Печатаем элементы меню без рамок
    for i in range(max_lines):
        left_item = left_column[i] if i < len(left_column) else ("", "")
        right_item = right_column[i] if i < len(right_column) else ("", "")
        
        left_num, left_desc = left_item
        right_num, right_desc = right_item
        
        line = format_menu_line(left_num, left_desc, right_num, right_desc, 0)
        if line:
            print_centered(f"{section_color}{line}{Colors.RESET}")
    
    print()  # Пустая строка после секции

def execute_script(script_number):
    """Выполнение скрипта из папки all с использованием переменных файлов"""
    # Получаем имя файла из переменных
    filename = ALL_FILES.get(script_number)
    
    if not filename:
        print_centered(f"{Colors.RED}❌ Функция {script_number} не найдена в конфигурации{Colors.RESET}")
        input(f"\n{Colors.BRIGHT_BLACK}Нажмите Enter для возврата в главное меню...{Colors.RESET}")
        return
    
    # Определяем путь к скрипту в зависимости от контекста (исходный код или exe)
    if getattr(sys, 'frozen', False):
        # Если запущено как скомпилированное приложение (.exe)
        application_path = Path(sys._MEIPASS)
        script_path = application_path / "all" / filename
    else:
        # Если запущено как обычный скрипт (.py)
        script_path = Path("all") / filename
    
    if script_path.exists():
        try:
            clear_screen()
            print_centered(f"{Colors.NEO_GREEN}🚀 Запуск функции {script_number} - {filename}{Colors.RESET}")
            print_centered(f"{Colors.BRIGHT_BLACK}📁 Файл: {script_path}{Colors.RESET}\n")
            
            # Сохраняем текущий каталог
            old_cwd = os.getcwd()
            
            # Получаем корневую папку проекта (где находится main.py)
            if getattr(sys, 'frozen', False):
                project_root = Path(sys._MEIPASS)
            else:
                project_root = Path.cwd()
            
            # Определяем каталог для запуска скрипта
            # Если скрипт находится в подкаталоге (например, consPlayer/), используем его родительскую папку
            if 'consPlayer' in filename or any(sep in str(filename) for sep in ['/', '\\']):
                # Для скриптов в подкаталогах используем корневую папку проекта
                script_cwd = project_root
                script_to_run = script_path
            else:
                # Для обычных скриптов используем папку 'all'
                script_cwd = project_root / "all"
                script_to_run = Path(filename)
            
            # Меняем текущий каталог для выполнения скрипта
            os.chdir(script_cwd)
            
            print_centered(f"{Colors.BRIGHT_BLACK}📂 Рабочая директория: {script_cwd}{Colors.RESET}")
            print_centered(f"{Colors.BRIGHT_BLACK}▶️  Запускаемый файл: {script_to_run}{Colors.RESET}\n")
            
            # Для .py файлов запускаем их через subprocess
            if filename.endswith('.py'):
                try:
                    # Запускаем скрипт
                    result = subprocess.run(
                        [sys.executable, str(script_to_run)],
                        check=False,
                        cwd=str(script_cwd),
                        text=True,
                        encoding='utf-8'
                    )
                    
                    if result.returncode == 0:
                        print(f"\n{Colors.NEO_GREEN}✅ Скрипт завершен успешно{Colors.RESET}")
                    elif result.returncode == 1:
                        print(f"\n{Colors.YELLOW}⚠️  Скрипт завершился с кодом 1 (возможно, ожидаемое завершение){Colors.RESET}")
                    else:
                        print(f"\n{Colors.YELLOW}⚠️  Скрипт завершился с кодом: {result.returncode}{Colors.RESET}")
                        
                except KeyboardInterrupt:
                    print(f"\n{Colors.RED}⏹️  Выполнение прервано пользователем{Colors.RESET}")
                except Exception as e:
                    print(f"\n{Colors.RED}❌ Ошибка выполнения: {str(e)}{Colors.RESET}")
            else:
                # Для других файлов (например, .bat) используем subprocess
                try:
                    subprocess.run([str(script_to_run)], shell=True, check=True, cwd=str(script_cwd))
                    print(f"\n{Colors.NEO_GREEN}✅ Выполнение завершено{Colors.RESET}")
                except subprocess.CalledProcessError as e:
                    print(f"\n{Colors.RED}❌ Ошибка выполнения (код {e.returncode}){Colors.RESET}")
                except KeyboardInterrupt:
                    print(f"\n{Colors.RED}⏹️  Выполнение прервано пользователем{Colors.RESET}")
            
            # Возвращаем исходный каталог
            os.chdir(old_cwd)
            
            print()  # Пустая строка для читаемости
            
        except Exception as e:
            print_centered(f"{Colors.RED}❌ Неожиданная ошибка: {str(e)}{Colors.RESET}")
            import traceback
            traceback.print_exc()  # Для отладки
    else:
        print_centered(f"{Colors.RED}❌ Файл {script_path} не найден{Colors.RESET}")
        print_centered(f"{Colors.YELLOW}💡 Ожидаемый файл: {filename}{Colors.RESET}")
        if not getattr(sys, 'frozen', False):
            print_centered(f"{Colors.BRIGHT_BLACK}📁 Создайте файл в папке 'all'{Colors.RESET}")
    
    input(f"\n{Colors.BRIGHT_BLACK}Нажмите Enter для возврата в главное меню...{Colors.RESET}")
def show_file_info():
    """Показывает информацию о файлах конфигурации"""
    clear_screen()
    print_header()  
    
    print_centered(f"{Colors.NEO_CYAN} КОНФИГУРАЦИЯ ФАЙЛОВ NeoDark-CLI{Colors.RESET}")
    print()
    
    sections = [
        ("Основные функции", FILES_MAIN, Colors.NEO_BLUE),
        ("Обслуживание и Утилиты", FILES_MAINTENANCE, Colors.NEO_GREEN),
        ("Конфигурация и Данные", FILES_CONFIG, Colors.NEO_PURPLE),
        ("Сетевые и Агентские функции", FILES_NETWORK, Colors.NEO_ORANGE),
        ("Аккаунты и Взаимодействие", FILES_ACCOUNTS, Colors.NEO_PINK),
        ("Инструменты разработчика", FILES_DEVELOPER, Colors.BRIGHT_CYAN),
        ("Развлечения и Визуализация", FILES_ENTERTAINMENT, Colors.BRIGHT_MAGENTA)
    ]
    
    for section_name, files_dict, color in sections:
        print_centered(f"{color}{Colors.BOLD}╔{'═' * 80}╗{Colors.RESET}")
        print_centered(f"{color}{Colors.BOLD}║ {section_name:<78} ║{Colors.RESET}")
        print_centered(f"{color}{Colors.BOLD}╠{'═' * 80}╣{Colors.RESET}")
        
        for num, filename in files_dict.items():
            line = f"║ {Colors.NEO_CYAN}[{num:>2}]{Colors.RESET} → {filename:<65} ║"
            print_centered(f"{color}{line}{Colors.RESET}")
        
        print_centered(f"{color}{Colors.BOLD}╚{'═' * 80}╝{Colors.RESET}")
        print()
    
    input(f"\n{Colors.BRIGHT_BLACK}Нажмите Enter для возврата в главное меню...{Colors.RESET}")

def show_startup_warning():
    """Показывает предупреждение при запуске"""
    # Очищаем экран
    clear_screen()
    
    # Показываем красное предупреждение по центру
    warning_text = f"{Colors.RED}ВНИМАНИЕ{Colors.RESET}"
    print_centered(warning_text)
    print()  # Пустая строка
    
    # Показываем информационное сообщение
    info_lines = [
        "Вы используете trial версию продукта - это значит, что продукт доступен",
        "очень узкому кругу лиц и бета-тестерам. Четверть продуктов сделана в",
        "DEMO-версиях, не используйте в коммерческих целях!"
    ]
    
    for line in info_lines:
        print_centered(line)
    
    print()  # Пустая строка
    
    # Ждем 2 секунды перед добавлением серой надписи
    time.sleep(2)  # Убрал import time, так как он уже в начале файла
    
    # Серая надпись с инструкцией
    instruction = f"{Colors.BRIGHT_BLACK}Нажмите Enter для продолжения...{Colors.RESET}"
    print_centered(instruction)
    
    # Ждем еще 3 секунды (всего 5 секунд с начала отображения)
    time.sleep(3)
    
    # Очищаем экран и переходим к главному меню
    clear_screen()

def main_menu():
    menu_sections = [
        {
            "title": "1. ОСНОВНЫЕ ФУНКЦИИ",
            "color": Colors.NEO_BLUE,
            "items": [
                ("0", "Выход"),
                ("1", "Переключиться на GUI"),
                ("2", "Синхронизировать продукты"),
                ("3", "Статус системы"),
                ("4", "Включить автозапуск"),
                ("6", "Проверить обновления (CLI)"),
                ("8", "Запуск с минимальными ресурсами")
            ]
        },
        {
            "title": "2. ОБСЛУЖИВАНИЕ И УТИЛИТЫ",
            "color": Colors.NEO_GREEN,
            "items": [
                ("10", "Сносер TG (demo)"),
                ("11", "Очистить кэш"),
                ("12", "Включить Zapret"),
                ("13", "Вступить в NeoDark (edu)"),
                ("14", "Бенчмарк процессора (Light)"),
                ("16", "Спящий режим для продуктов"),
                ("17", "Проверка портов"),
                ("18", "Отключить телеметрию")
            ]
        },
        {
            "title": "3. КОНФИГУРАЦИЯ И ДАННЫЕ", 
            "color": Colors.NEO_PURPLE,
            "items": [
                ("20", "Данные системы и конфигурации"),
                ("21", "Оптимизировать систему"),
                ("23", "Режим low-disk"),
                ("24", "Скрыть окно консоли"),
                ("25", "Установка рабочего стола"),
                ("26", "Планировщик задач"),
                ("27", "Управление брандмауэром"),
                ("28", "Системный аудит")
            ]
        },
        {
            "title": "4. СЕТЕВЫЕ И АГЕНТСКИЕ ФУНКЦИИ",
            "color": Colors.NEO_ORANGE, 
            "items": [
                ("30", "Matrix-rain 15с"),
                ("31", "SpeedTest"),
                ("32", "Запустить NeoPRAI-Agent"),
                ("33", "Проверить IP-репутацию"),
                ("34", "IP-адрес и Геолокация"),
                ("35", "Трассировка до продукта"),
                ("39", "Поиск по файлам (Grep-like)")
            ]
        },
        {
            "title": "5. АККАУНТЫ И ВЗАИМОДЕЙСТВИЕ",
            "color": Colors.NEO_PINK,
            "items": [
                ("40", "Войти в аккаунт"),
                ("41", "Сменить пароль (локально)"),
                ("42", "Создать гостевой аккаунт"),
                ("43", "Проверить активность сессий"),
                ("44", "Блокировка продуктов"),
                ("46", "Сброс настроек профиля"),
                ("47", "Настроить резервное копирование"),
                ("48", "Просмотр истории действий"),
                ("49", "Очистить облачную конфигурацию")
            ]
        },
        {
            "title": "6. ИНСТРУМЕНТЫ РАЗРАБОТЧИКА",
            "color": Colors.BRIGHT_CYAN,
            "items": [
                ("51", "Добавить свой скрипт"),
                ("52", "Список процессов (Advanced)"),
                ("53", "Просмотр переменных среды"),
                ("56", "Патч файла (Demo)"),
                ("67", "Управление горячими клавишами"),
                ("68", "Проверка подлинности продукта"),
                ("69", "Настройка DPI (Universal Launcher)")
            ]
        },
        {
            "title": "7. РАЗВЛЕЧЕНИЯ И ВИЗУАЛИЗАЦИЯ",
            "color": Colors.BRIGHT_MAGENTA,
            "items": [
                ("60", "Синий экран смерти (Fake)"),
                ("61", "Консольная анимация логотипа"),
                ("62", "Тест клавиатуры (CLI)"),
                ("63", "Консольный плеер (Demo)"),
                ("66", "Мониторинг ресурсов (график)")
            ]
        }
    ]
    
    while True:
        clear_screen()
        print_header()
        
        # Вывод всех секций меню без рамок
        for section in menu_sections:
            print_two_columns(section["items"], section["color"], section["title"])
        
        # Дополнительные команды
        print_centered(f"{Colors.BRIGHT_BLACK}{'─' * 50}{Colors.RESET}")
        print_centered(f"{Colors.BRIGHT_BLACK}💡 Введите {Colors.NEO_CYAN}info{Colors.BRIGHT_BLACK} для просмотра конфигурации файлов{Colors.RESET}")
        print_centered(f"{Colors.BRIGHT_BLACK}💡 Введите {Colors.NEO_CYAN}0 или 99{Colors.BRIGHT_BLACK} для выхода{Colors.RESET}")
        
        # Центрированный ввод
        print()
        choice_prompt = f"{Colors.NEO_CYAN}Выберите пункт меню {Colors.BRIGHT_WHITE}[0-69]{Colors.NEO_CYAN}: {Colors.RESET}"
        print_centered(choice_prompt)
        
        try:
            width = get_terminal_width()
            clean_prompt = re.sub(r'\033\[[0-9;]*m', '', choice_prompt)
            cursor_pos = (width - len(clean_prompt)) // 2
            print(" " * cursor_pos, end="")
            
            choice = input().strip().lower()
            
            if choice == "0" or choice == "99":
                print_centered(f"\n{Colors.NEO_GREEN}До свидания! Спасибо за использование NeoDark-CLI!{Colors.RESET}")
                time.sleep(2)
                clear_screen()
                break
            elif choice == "info":
                show_file_info()
                continue
            elif choice.isdigit() and 1 <= int(choice) <= 69:
                execute_script(choice)
            else:
                print_centered(f"\n{Colors.RED}Неверный выбор! Введите число от 0 до 69.{Colors.RESET}")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print_centered(f"\n{Colors.RED}Программа прервана пользователем{Colors.RESET}")
            time.sleep(2)
            break
        except Exception as e:
            print_centered(f"\n{Colors.RED}Ошибка: {str(e)}{Colors.RESET}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        # Показываем предупреждение при запуске
        show_startup_warning()
        
        # Запускаем главное меню
        main_menu()
    except Exception as e:
        print(f"{Colors.RED}Критическая ошибка: {str(e)}{Colors.RESET}")
        input("Нажмите Enter для выхода...")