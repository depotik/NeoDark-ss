import os
import sys
import platform
import time
import threading
from datetime import datetime

try:
    import speedtest
    SPEEDTEST_AVAILABLE = True
except ImportError:
    SPEEDTEST_AVAILABLE = False

def print_header():
    """Выводит заголовок программы"""
    print("🚀 SpeedTest NeoDark")
    print("=" * 50)
    print("Проверка скорости интернет-соединения")
    print()

def show_requirements():
    """Показывает информацию о требованиях"""
    if not SPEEDTEST_AVAILABLE:
        print("❌ Модуль speedtest-cli не установлен!")
        print("Установите его командой: pip install speedtest-cli")
        print()
        return False
    return True

def format_speed(speed):
    """Форматирует скорость в читаемый вид"""
    if speed is None:
        return "N/A"
    
    if speed > 1000000000:  # > 1 Гбит/с
        return f"{speed/1000000000:.2f} Гбит/с"
    elif speed > 1000000:   # > 1 Мбит/с
        return f"{speed/1000000:.2f} Мбит/с"
    elif speed > 1000:      # > 1 Кбит/с
        return f"{speed/1000:.2f} Кбит/с"
    else:
        return f"{speed:.2f} бит/с"

def format_bytes(bytes_count):
    """Форматирует количество байт в читаемый вид"""
    if bytes_count is None:
        return "N/A"
    
    if bytes_count > 1000000000:  # > 1 ГБ
        return f"{bytes_count/1000000000:.2f} ГБ"
    elif bytes_count > 1000000:   # > 1 МБ
        return f"{bytes_count/1000000:.2f} МБ"
    elif bytes_count > 1000:      # > 1 КБ
        return f"{bytes_count/1000:.2f} КБ"
    else:
        return f"{bytes_count:.2f} Б"

def print_progress_dots(message, duration=5):
    """Показывает анимацию прогресса с точками"""
    end_time = time.time() + duration
    dots = 1
    
    while time.time() < end_time:
        dot_str = "." * dots
        print(f"\r{message}{dot_str}", end="", flush=True)
        dots = (dots % 3) + 1
        time.sleep(0.5)
    
    print()

def run_speedtest():
    """Выполняет тест скорости интернета"""
    try:
        print("🔍 Подготовка к тестированию...")
        print_progress_dots("Подключение к серверу", 3)
        
        # Создаем объект Speedtest
        st = speedtest.Speedtest()
        
        print("🌐 Поиск лучшего сервера...")
        print_progress_dots("Поиск", 2)
        
        # Находим лучший сервер
        st.get_best_server()
        best_server = st.results.server
        print(f"✅ Выбран сервер: {best_server['name']} ({best_server['country']})")
        print()
        
        # Тест на скачивание
        print("⬇️  Тестирование скорости скачивания...")
        print_progress_dots("Загрузка", 5)
        download_speed = st.download()
        print(f"✅ Скорость скачивания: {format_speed(download_speed)}")
        print()
        
        # Тест на загрузку
        print("⬆️  Тестирование скорости загрузки...")
        print_progress_dots("Отправка", 5)
        upload_speed = st.upload()
        print(f"✅ Скорость загрузки: {format_speed(upload_speed)}")
        print()
        
        # Получаем пинг
        ping = st.results.ping
        print(f"⏱️  Пинг: {ping:.2f} мс")
        print()
        
        # Выводим дополнительную информацию
        print("📊 Детальная информация:")
        print(f"   IP: {st.results.client['ip']}")
        print(f"   Провайдер: {st.results.client['isp']}")
        print(f"   Страна: {st.results.client['country']}")
        print(f"   Координаты: {st.results.client['lat']}, {st.results.client['lon']}")
        print(f"   Скачано: {format_bytes(st.results.bytes_received)}")
        print(f"   Отправлено: {format_bytes(st.results.bytes_sent)}")
        print()
        
        return {
            'download': download_speed,
            'upload': upload_speed,
            'ping': ping,
            'server': best_server,
            'client': st.results.client
        }
        
    except speedtest.ConfigRetrievalError:
        print("❌ Ошибка подключения к серверу SpeedTest")
        return None
    except speedtest.SpeedtestBestServerFailure:
        print("❌ Не удалось найти подходящий сервер")
        return None
    except Exception as e:
        print(f"❌ Ошибка при выполнении теста: {str(e)}")
        return None

def show_speed_recommendations(results):
    """Показывает рекомендации по скорости"""
    if not results:
        return
    
    download_mbps = results['download'] / 1000000
    upload_mbps = results['upload'] / 1000000
    
    print("💡 Рекомендации:")
    
    # Рекомендации по использованию интернета
    if download_mbps >= 100:
        print("   🎯 У вас отличная скорость интернета!")
        print("   Подходит для: 4K видео, онлайн-игр, видеоконференций")
    elif download_mbps >= 50:
        print("   ✅ У вас хорошая скорость интернета")
        print("   Подходит для: HD видео, музыки, веб-серфинга")
    elif download_mbps >= 25:
        print("   ⚠️  У вас средняя скорость интернета")
        print("   Подходит для: SD видео, электронной почты, веб-серфинга")
    else:
        print("   ⚠️  У вас низкая скорость интернета")
        print("   Рекомендуется: ограничиться текстовыми данными")
    
    print()
    
    # Рекомендации по пингу
    ping = results['ping']
    if ping <= 20:
        print("   ⚡ Отличный пинг - идеален для онлайн-игр")
    elif ping <= 50:
        print("   ✅ Хороший пинг - подходит для большинства задач")
    elif ping <= 100:
        print("   ⚠️ Средний пинг - возможны задержки в играх")
    else:
        print("   ⚠️ Высокий пинг - могут быть проблемы с реал-тайм приложениями")

def main():
    """Главная функция SpeedTest"""
    print_header()
    
    # Проверяем наличие необходимых модулей
    if not show_requirements():
        input("Нажмите Enter для выхода...")
        return
    
    print("Начинаем тестирование скорости интернета...")
    print("=" * 50)
    
    try:
        # Выполняем тест скорости
        start_time = datetime.now()
        results = run_speedtest()
        end_time = datetime.now()
        
        if results:
            # Показываем рекомендации
            show_speed_recommendations(results)
            
            # Выводим общее время тестирования
            duration = end_time - start_time
            print(f"⏱️  Общее время тестирования: {duration.total_seconds():.1f} секунд")
            
            print(f"\n✅ Тест завершен!")
        else:
            print("❌ Тест не удалось завершить")
            
        print(f"⏰ Завершено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Тест прерван пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()