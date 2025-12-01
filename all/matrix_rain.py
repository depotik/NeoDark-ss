import sys
import random
import time
import os
import threading
from datetime import datetime

# Попытка импортировать colorama для кроссплатформенной поддержки цветов
try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Определяем заглушки для цветов
    class Fore:
        GREEN = '\033[32m'
        LIGHTGREEN_EX = '\033[92m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
    
    class Back:
        RESET = '\033[0m'

class MatrixDrop:
    """Класс, представляющий одну падающую каплю матричного кода."""
    def __init__(self, x, max_y):
        self.x = x
        self.y = random.randint(-max_y, 0)  # Начинаем выше экрана
        self.speed = random.randint(1, 3)   # Случайная скорость падения
        self.characters = self._generate_characters()
        self.length = random.randint(5, 20)  # Случайная длина цепочки
        self.counter = 0
        self.max_y = max_y
        self.tail_color = Fore.GREEN
        self.head_color = Fore.LIGHTGREEN_EX
        self.white_color = Fore.WHITE

    def _generate_characters(self):
        """Генерирует случайные символы для капли."""
        # Комбинация латинских букв, цифр и специальных символов
        chars = []
        for _ in range(20):
            # ASCII символы от 33 до 126
            chars.append(chr(random.randint(33, 126)))
        return chars

    def move(self):
        """Перемещает каплю вниз с учетом ее скорости."""
        self.counter += 1
        if self.counter >= self.speed:
            self.y += 1
            self.counter = 0
            return True
        return False

    def draw(self, screen_buffer):
        """Отрисовывает каплю в буфере экрана."""
        for i in range(self.length):
            pos_y = self.y - i
            if 0 <= pos_y < self.max_y:
                # Выбираем символ
                char = self.characters[i % len(self.characters)]
                
                # Выбираем цвет в зависимости от позиции в цепочке
                if i == 0:  # Голова капли
                    color = self.head_color
                elif i < self.length // 3:  # Начало хвоста
                    color = self.white_color
                else:  # Основной хвост
                    color = self.tail_color
                
                # Добавляем символ в буфер экрана
                if 0 <= self.x < len(screen_buffer[pos_y]):
                    screen_buffer[pos_y][self.x] = f"{color}{char}{Fore.RESET}"

    def is_off_screen(self):
        """Проверяет, вышла ли капля за пределы экрана."""
        return self.y - self.length > self.max_y

class MatrixRain:
    """Основной класс для эффекта матричного дождя."""
    def __init__(self):
        self.drops = []
        self.running = False
        self.screen_width = 80
        self.screen_height = 25
        self.update_screen_size()
        
    def update_screen_size(self):
        """Обновляет размеры экрана."""
        try:
            # Получаем размер терминала
            self.screen_width = os.get_terminal_size().columns
            self.screen_height = os.get_terminal_size().lines - 1  # Минус одна строка для статуса
        except:
            # Если не удалось получить размер, используем значения по умолчанию
            pass
            
    def create_drop(self):
        """Создает новую каплю в случайной позиции."""
        x = random.randint(0, self.screen_width - 1)
        return MatrixDrop(x, self.screen_height)

    def initialize_drops(self):
        """Инициализирует начальный набор капель."""
        # Создаем начальный набор капель
        num_drops = self.screen_width // 3  # Примерно одна капля на каждые 3 колонки
        for _ in range(num_drops):
            self.drops.append(self.create_drop())

    def update_drops(self):
        """Обновляет позиции всех капель."""
        # Двигаем существующие капли
        for drop in self.drops[:]:  # Копия списка для безопасного удаления
            drop.move()
            # Удаляем капли, которые вышли за пределы экрана
            if drop.is_off_screen():
                self.drops.remove(drop)
        
        # Добавляем новые капли
        if len(self.drops) < self.screen_width // 2:  # Не более половины ширины экрана капель
            if random.random() < 0.3:  # 30% шанс создания новой капли
                self.drops.append(self.create_drop())

    def create_screen_buffer(self):
        """Создает буфер экрана для отрисовки."""
        return [[' ' for _ in range(self.screen_width)] for _ in range(self.screen_height)]

    def draw_status(self, start_time):
        """Отрисовывает статус в нижней части экрана."""
        elapsed = datetime.now() - start_time
        status_text = f"NeoDark Matrix Rain | Время: {str(elapsed).split('.')[0]} | Капель: {len(self.drops)}"
        
        # Центрируем текст статуса
        padding = (self.screen_width - len(status_text)) // 2
        if padding > 0:
            status_text = ' ' * padding + status_text
        
        # Обрезаем, если текст слишком длинный
        if len(status_text) > self.screen_width:
            status_text = status_text[:self.screen_width]
        
        return status_text

    def render_frame(self, start_time):
        """Отрисовывает один кадр эффекта."""
        # Создаем буфер экрана
        screen_buffer = self.create_screen_buffer()
        
        # Отрисовываем все капли в буфере
        for drop in self.drops:
            drop.draw(screen_buffer)
        
        # Преобразуем буфер в строки
        frame_lines = [''.join(row) for row in screen_buffer]
        
        # Добавляем статусную строку
        status_line = self.draw_status(start_time)
        frame_lines.append(status_line)
        
        # Очищаем экран и выводим кадр
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n'.join(frame_lines))

    def run(self, duration=15):
        """Запускает основной цикл эффекта."""
        self.running = True
        self.update_screen_size()
        self.initialize_drops()
        
        start_time = datetime.now()
        
        try:
            while self.running:
                # Проверяем, не истекло ли время
                elapsed = datetime.now() - start_time
                if duration and elapsed.total_seconds() >= duration:
                    break
                
                # Обновляем капли
                self.update_drops()
                
                # Отрисовываем кадр
                self.render_frame(start_time)
                
                # Небольшая задержка для контроля частоты кадров
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.RESET}⚠️  Эффект остановлен пользователем")
        finally:
            self.running = False
            # Сбрасываем цвета
            print(Fore.RESET + Back.RESET)

def show_intro():
    """Показывает вступительную информацию."""
    print("🌌 NeoDark Matrix Rain")
    print("=" * 50)
    print("Эффект матричного дождя в вашем терминале")
    print()
    print("✨ Особенности:")
    print("  • Реалистичный эффект падающих символов")
    print("  • Динамическое создание и удаление капель")
    print("  • Цветовая дифференциация головы и хвоста капли")
    print("  • Отслеживание времени работы")
    print()
    
    if not HAS_COLORAMA:
        print("⚠️  Модуль colorama не найден. Установите его для лучшего отображения цветов:")
        print("   pip install colorama")
        print()
    
    print("Нажмите Ctrl+C для остановки эффекта")
    print("Эффект автоматически остановится через 15 секунд")
    print()
    input("Нажмите Enter для запуска...")

def main():
    """Главная функция программы."""
    show_intro()
    
    try:
        # Создаем и запускаем эффект
        matrix = MatrixRain()
        matrix.run(duration=15)
        
        print(f"\n{Fore.RESET}✅ Эффект Matrix Rain завершен!")
        print("Спасибо за использование NeoDark!")
        
    except Exception as e:
        print(f"\n{Fore.RESET}❌ Произошла ошибка: {str(e)}")
    
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()