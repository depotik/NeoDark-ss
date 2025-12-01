# matrix.py
import sys
import random
import time
import subprocess
import os
import msvcrt

try:
    import colorama
except ImportError:
    print('Для запуска программы нужен модуль colorama.')
    print('Установите его: pip install colorama')
    sys.exit()

# Инициализация colorama для работы с цветами в Windows
colorama.init()

class Капля:
    """Класс, представляющий одну падающую каплю матричного кода."""
    def __init__(self, ширина, высота):
        self.x = random.randint(0, ширина - 1)
        self.y = random.randint(-высота, 0)  # Начинаем выше экрана
        self.скорость = random.randint(1, 3)  # Случайная скорость падения
        self.символы = [str(random.randint(0, 9)) for _ in range(10)]  # Случайные цифры
        self.длина = random.randint(5, 15)  # Случайная длина цепочки
        self.счетчик = 0
        self.ширина = ширина
        self.высота = высота

    def двигать(self):
        """Перемещает каплю вниз с учетом ее скорости."""
        self.счетчик += 1
        if self.счетчик >= self.скорость:
            self.y += 1
            self.счетчик = 0
            return True
        return False

    def рисовать(self):
        """Отрисовывает каплю на экране."""
        for i in range(self.длина):
            позиция_y = self.y - i
            if 0 <= позиция_y < self.высота:
                # Более яркий символ в начале цепочки
                цвет = colorama.Fore.LIGHTGREEN_EX if i == 0 else colorama.Fore.GREEN
                символ = self.символы[i % len(self.символы)]
                # Перемещаем курсор и выводим символ
                print(f"\033[{позиция_y + 1};{self.x + 1}H{цвет}{символ}", end='')
    
    def очистить(self):
        """Стирает каплю с экрана."""
        for i in range(self.длина):
            позиция_y = self.y - i
            if 0 <= позиция_y < self.высота:
                # Перемещаем курсор и стираем символ
                print(f"\033[{позиция_y + 1};{self.x + 1}H ", end='')

    def за_пределами_экрана(self):
        """Проверяет, вышла ли капля за пределы экрана."""
        return self.y - self.длина > self.высота

    def обновить(self):
        """Обновляет каплю, когда она выходит за пределы экрана."""
        self.__init__(self.ширина, self.высота)

def проверить_нажатие_esc():
    """Проверяет, была ли нажата клавиша ESC."""
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'\x1b':  # ESC
            return True
    return False

def получить_размеры_консоли():
    """Получает размеры консоли."""
    try:
        import shutil
        размеры = shutil.get_terminal_size()
        return размеры.columns, размеры.lines
    except:
        return 80, 160  # Размеры по умолчанию

def очистить_экран():
    """Очищает экран консоли."""
    os.system('cls' if os.name == 'nt' else 'clear')

def установить_заголовок(заголовок):
    """Устанавливает заголовок окна консоли."""
    if os.name == 'nt':
        os.system(f'title {заголовок}')

def запустить_main_py():
    """Запускает файл main.py из родительской директории."""
    try:
        путь_к_файлу = os.path.join(os.path.dirname(__file__), '..', 'main.py')
        путь_к_файлу = os.path.abspath(путь_к_файлу)
        
        print(f"\nЗапускаем {путь_к_файлу}...")
        
        # Проверяем существование файла
        if not os.path.exists(путь_к_файлу):
            print(f"Файл {путь_к_файлу} не найден!")
            return False
        
        # Запускаем файл с помощью Python
        subprocess.run([sys.executable, путь_к_файлу])
        return True
        
    except Exception as ошибка:
        print(f"Ошибка при запуске main.py: {ошибка}")
        return False

def основной():
    # Настройка консоли
    установить_заголовок('Матричный Дождь')
    очистить_экран()
    
    # Скрываем курсор с помощью ANSI кода
    print('\033[?25l', end='')
    
    # Получаем размеры консоли
    ширина, высота = получить_размеры_консоли()
    
    # Создаем массив капель
    количество_капель = ширина // 2  # Количество капель (~50% ширины экрана)
    капли = [Капля(ширина, высота) for _ in range(количество_капель)]
    
    # Выводим инструкцию в верхней части экрана
    print("\033[1;1HНажмите ESC для выхода...")
    
    try:
        while True:
            # Очищаем и перерисовываем капли
            for капля in капли:
                капля.очистить()
                if капля.двигать():
                    капля.рисовать()
                
                # Если капля ушла за нижнюю границу, обновляем ее
                if капля.за_пределами_экрана():
                    капля.обновить()
                    капля.рисовать()
            
            # Проверяем нажатие клавиши ESC
            if проверить_нажатие_esc():
                print("\nВыход из матричного дождя...")
                break
            
            # Задержка для контроля скорости анимации
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\nПрервано пользователем...")
    
    finally:
        # Восстанавливаем настройки консоли
        print('\033[?25h', end='')  # Показываем курсор
        очистить_экран()
        print(colorama.Fore.RESET + "Матричный дождь завершен.")
        
        # Запускаем main.py после выхода
        запустить_main_py()

if __name__ == "__main__":
    основной()