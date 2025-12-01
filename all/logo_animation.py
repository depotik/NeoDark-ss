import os
import sys
import time
import random
from datetime import datetime

def print_header():
    """Выводит заголовок программы"""
    print("🎨 Консольная анимация логотипа")
    print("=" * 40)

def get_neodark_banner():
    """Возвращает баннер NeoDark"""
    return [
        "███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗",
        "████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝",
        "██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ ",
        "██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ ",
        "██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗",
        "╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝"
    ]

def show_neodark_logo():
    """Показывает логотип NeoDark"""
    banner = get_neodark_banner()
    for line in banner:
        print(f"\033[96m{line}\033[0m")
    print()

def show_animation_info():
    """Показывает информацию об анимации логотипа"""
    print("ℹ️ Анимация логотипа NeoDark:")
    print("-" * 35)
    print("   Консольная анимация логотипа")
    print("   демонстрирует возможности")
    print("   текстовой графики в терминале.")
    print()
    print("   Включает эффекты:")
    print("   • Построчная прорисовка")
    print("   • Цветовые переходы")
    print("   • Анимация символов")
    print("   • Плавное появление")

def animate_logo():
    """Анимирует логотип NeoDark"""
    print("\n🎨 Анимация логотипа:")
    print("-" * 30)
    
    try:
        # Получаем логотип
        banner = get_neodark_banner()
        
        print("🔄 Запуск анимации...")
        time.sleep(1)
        
        # Очищаем экран
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Построчная анимация
        for i, line in enumerate(banner):
            # Постепенно показываем строку
            for j in range(len(line) + 1):
                # Очищаем экран
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Показываем уже полностью отрисованные строки
                for k in range(i):
                    print(f"\033[96m{banner[k]}\033[0m")
                
                # Показываем частично отрисованную текущую строку
                if j > 0:
                    current_part = line[:j]
                    print(f"\033[96m{current_part}\033[0m")
                
                time.sleep(0.02)  # Задержка для анимации
        
        # Добавляем пустую строку
        print()
        
        # Анимация цвета
        colors = [
            "\033[91m",  # Красный
            "\033[92m",  # Зеленый
            "\033[93m",  # Желтый
            "\033[94m",  # Синий
            "\033[95m",  # Фиолетовый
            "\033[96m",  # Голубой
        ]
        
        # Цикл цветовой анимации
        for cycle in range(10):
            # Очищаем экран
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Показываем логотип с текущим цветом
            color = colors[cycle % len(colors)]
            for line in banner:
                print(f"{color}{line}\033[0m")
            
            print()
            print("🎨 Цветовая анимация...")
            time.sleep(0.3)
        
        # Возвращаем исходный цвет
        os.system('cls' if os.name == 'nt' else 'clear')
        show_neodark_logo()
        print("✅ Анимация завершена!")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️ Анимация прервана пользователем")
        return True
    except Exception as e:
        print(f"❌ Ошибка анимации: {e}")
        return False

def show_animation_types():
    """Показывает типы анимаций"""
    print("\n🎭 Типы анимаций:")
    print("-" * 20)
    print("   [1] Построчная")
    print("   [2] Побуквенная")
    print("   [3] Цветовая")
    print("   [4] Матричная")
    print("   [5] Пульсация")

def show_animation_settings():
    """Показывает настройки анимации"""
    print("\n⚙️ Настройки анимации:")
    print("-" * 25)
    print("   Скорость: Средняя")
    print("   Цвет: Голубой/Цветная")
    print("   Эффекты: Включены")
    print("   Длительность: 5 секунд")
    print("   Циклы: 3")

def main():
    """Главная функция анимации логотипа"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Показываем информацию
        show_animation_info()
        
        # Показываем типы анимаций
        show_animation_types()
        
        # Показываем настройки
        show_animation_settings()
        
        # Анимация логотипа
        print("\n" + "=" * 40)
        input("Нажмите Enter для запуска анимации...")
        
        if animate_logo():
            print("\n🎉 Анимация успешно завершена!")
        else:
            print("\n⚠️  Анимация не завершена")
        
        print(f"\n✅ Работа завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Анимация прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()
import os
import sys
import time
import random
import threading

# Импортируем общие компоненты
try:
    from banner import print_neodark_banner, color_code
except ImportError:
    # Если не удается импортировать, создаем минимальные компоненты
    color_code = {
        "reset": "\033[0m",
        "green": "\033[32m",
        "yellow": "\033[93m",
        "red": "\033[31m",
        "cyan": "\033[36m",
        "bold": "\033[01m",
        "dark": "\033[90m",
        "neon_blue": "\033[38;5;75m",
        "neon_purple": "\033[38;5;99m",
        "neon_cyan": "\033[38;5;51m",
        "neon_green": "\033[38;5;118m",
        "neon_orange": "\033[38;5;208m",
        "neon_pink": "\033[38;5;205m",
    }
    
    def print_neodark_banner(title="", subtitle=""):
        """Минимальная реализация баннера"""
        print(f"{color_code['cyan']}")
        print("Logo Animation")
        print(f"{color_code['reset']}")
        if title:
            print(f"{color_code['yellow']}{title}{color_code['reset']}")
        print()

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_size():
    """Получение размеров терминала"""
    try:
        return os.get_terminal_size().columns, os.get_terminal_size().lines
    except:
        return 80, 24

def center_text(text, width=None):
    """Функция для центрирования текста"""
    if width is None:
        width, _ = get_terminal_size()
    
    lines = text.split('\n')
    centered_lines = []
    for line in lines:
        # Удаление цветовых кодов для правильного расчета длины
        clean_line = ''.join(re.split(r'\033\[[0-9;]*m', line))
        padding = (width - len(clean_line)) // 2
        centered_lines.append(' ' * padding + line)
    return '\n'.join(centered_lines)

def print_neodark_logo(colors=None):
    """Вывод логотипа NeoDark с возможностью изменения цветов"""
    if colors is None:
        colors = [color_code["neon_cyan"], color_code["neon_blue"]]
    
    logo_lines = [
        f"{colors[0]}███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗",
        f"{colors[1]}████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝",
        f"{colors[0]}██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ ",
        f"{colors[1]}██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ ",
        f"{colors[0]}██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗",
        f"{colors[1]}╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝",
        f"{color_code['reset']}"
    ]
    
    # Центрируем логотип
    width, _ = get_terminal_size()
    for line in logo_lines:
        clean_line = ''.join(re.split(r'\033\[[0-9;]*m', line))
        padding = (width - len(clean_line)) // 2
        print(' ' * padding + line)

def matrix_rain_effect():
    """Эффект дождя из матрицы на заднем плане"""
    width, height = get_terminal_size()
    
    # Создаем массив для отслеживания позиций символов
    columns = [0] * width
    
    # Символы для эффекта
    chars = "01"
    
    try:
        while True:
            # Создаем строку для вывода
            line = ""
            for i in range(width):
                if columns[i] > 0:
                    # Выводим символ
                    line += random.choice(chars)
                    columns[i] -= 1
                else:
                    # Пустое место или начать новый "дождь"
                    line += " "
                    if random.random() < 0.05:  # 5% шанс начать новый дождь
                        columns[i] = random.randint(5, 20)
            
            print(line)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

def animated_logo():
    """Анимация логотипа с плавным изменением цветов"""
    neon_colors = [
        color_code["neon_cyan"],
        color_code["neon_blue"],
        color_code["neon_purple"],
        color_code["neon_pink"],
        color_code["neon_green"],
        color_code["neon_orange"]
    ]
    
    try:
        for _ in range(20):  # 20 циклов анимации
            clear_screen()
            
            # Выбираем два случайных цвета для логотипа
            color1 = random.choice(neon_colors)
            color2 = random.choice(neon_colors)
            
            # Выводим логотип
            print_neodark_logo([color1, color2])
            
            # Центрируем дополнительный текст
            width, _ = get_terminal_size()
            subtitle = f"{color_code['yellow']}🚀 Advanced System Management Interface{color_code['reset']}"
            creator = f"{color_code['dark']}Creator: @weeaave | Special for NeoDark{color_code['reset']}"
            
            print()
            print(center_text(subtitle, width))
            print(center_text(creator, width))
            
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass

def pulsing_logo():
    """Пульсирующий логотип"""
    try:
        for _ in range(15):  # 15 циклов пульсации
            # Увеличение
            for scale in range(10, 20):
                clear_screen()
                print("\n" * (scale - 10))  # Смещение для центрирования по вертикали
                print_neodark_logo()
                time.sleep(0.05)
            
            # Уменьшение
            for scale in range(19, 9, -1):
                clear_screen()
                print("\n" * (scale - 10))
                print_neodark_logo()
                time.sleep(0.05)
    except KeyboardInterrupt:
        pass

def color_wave_logo():
    """Волновой эффект цвета по логотипу"""
    neon_colors = [
        color_code["neon_cyan"],
        color_code["neon_blue"],
        color_code["neon_purple"],
        color_code["neon_pink"],
        color_code["neon_green"],
        color_code["neon_orange"]
    ]
    
    logo_lines = [
        "███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗",
        "████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝",
        "██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ ",
        "██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ ",
        "██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗",
        "╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝",
    ]
    
    try:
        for cycle in range(30):  # 30 циклов волны
            clear_screen()
            
            offset = cycle % len(neon_colors)
            
            for i, line in enumerate(logo_lines):
                color_index = (i + offset) % len(neon_colors)
                colored_line = f"{neon_colors[color_index]}{line}{color_code['reset']}"
                print(center_text(colored_line))
            
            # Дополнительный текст
            width, _ = get_terminal_size()
            subtitle = f"{color_code['yellow']}🚀 Advanced System Management Interface{color_code['reset']}"
            creator = f"{color_code['dark']}Creator: @weeaave | Special for NeoDark{color_code['reset']}"
            
            print()
            print(center_text(subtitle, width))
            print(center_text(creator, width))
            
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass

def main():
    """Основная функция"""
    try:
        while True:
            clear_screen()
            print_neodark_banner("Анимация логотипа", "NeoDark Visual Effects")
            
            print(f"{color_code['cyan']}Выберите тип анимации логотипа:{color_code['reset']}")
            print(f"{color_code['yellow']}[1]{color_code['reset']} Цветная анимация")
            print(f"{color_code['yellow']}[2]{color_code['reset']} Пульсация")
            print(f"{color_code['yellow']}[3]{color_code['reset']} Цветная волна")
            print(f"{color_code['yellow']}[0]{color_code['reset']} Назад")
            
            choice = input(f"\n{color_code['cyan']}Ваш выбор: {color_code['reset']}").strip()
            
            if choice == "1":
                animated_logo()
            elif choice == "2":
                pulsing_logo()
            elif choice == "3":
                color_wave_logo()
            elif choice == "0":
                break
            else:
                print(f"\n{color_code['red']}❌ Неверный выбор{color_code['reset']}")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n\n{color_code['red']}🚫 Анимация прервана пользователем{color_code['reset']}")
    except Exception as e:
        print(f"\n{color_code['red']}❌ Ошибка: {str(e)}{color_code['reset']}")
    
    input(f"\n{color_code['dark']}Нажмите Enter для возврата в главное меню...{color_code['reset']}")

if __name__ == "__main__":
    import re
    main()