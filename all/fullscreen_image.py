import tkinter as tk
from PIL import Image, ImageTk
import time
import threading
import os

def create_fullscreen_window(image_path):
    """
    Создает полноэкранный просмотрщик изображений без рамок с блокировкой клавиш
    """
    root = tk.Tk()
    
    # Убираем рамки окна
    root.overrideredirect(True)
    
    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Устанавливаем размер окна на весь экран
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    
    # Поднимаем окно поверх всех других
    root.lift()
    root.attributes('-topmost', True)
    
    # Загружаем изображение
    try:
        image = Image.open(image_path)
        # Масштабируем изображение под размер экрана сохраняя пропорции
        image.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)
        
        # Центрируем изображение
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo, bg='black')
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Сохраняем ссылку на изображение чтобы оно не было удалено сборщиком мусора
        label.image = photo
        
    except Exception as e:
        # Если не можем загрузить изображение, показываем черный экран
        root.configure(bg='black')
    
    # Блокируем все события клавиатуры и мыши
    def block_events(event=None):
        return "break"
    
    # Привязываем все возможные события к функции блокировки
    root.bind("<Key>", block_events)
    root.bind("<Button>", block_events)
    root.bind("<Motion>", block_events)
    root.bind("<FocusIn>", block_events)
    root.bind("<FocusOut>", block_events)
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Блокируем закрытие окна
    
    return root

def auto_close(root, delay=10):
    """
    Автоматически закрывает окно через заданное время
    """
    def close():
        try:
            root.quit()
            root.destroy()
        except:
            pass
    
    # Запускаем таймер в отдельном потоке
    timer = threading.Timer(delay, close)
    timer.start()

if __name__ == "__main__":
    # Путь к изображению
    image_file = "i.webp"
    
    # Проверяем существует ли файл
    if not os.path.exists(image_file):
        print(f"Файл {image_file} не найден.")
        exit(1)
    
    # Создаем и запускаем окно в главном потоке
    root = create_fullscreen_window(image_file)
    
    # Запускаем автоматическое закрытие через 10 секунд
    auto_close(root, 10)
    
    # Запуск главного цикла событий
    root.mainloop()