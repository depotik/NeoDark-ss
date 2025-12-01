import os
import sys
import platform
import time
import threading
from datetime import datetime
import math

def print_header():
    """Выводит заголовок программы"""
    print("⚡ Бенчмарк процессора (Light) NeoDark")
    print("=" * 50)

def cpu_benchmark_test(duration=10):
    """Выполняет легкий бенчмарк CPU"""
    print(f"🚀 Запуск теста производительности CPU ({duration} секунд)...")
    print("   Выполняются математические вычисления...")
    print()
    
    # Переменные для теста
    start_time = time.time()
    end_time = start_time + duration
    operations = 0
    score = 0
    
    # Выполняем вычисления в течение заданного времени
    while time.time() < end_time:
        # Математические операции для нагрузки на CPU
        for _ in range(1000):
            # Различные математические операции
            x = math.sqrt(operations % 1000 + 1)
            y = math.sin(operations % 360)
            z = math.cos(operations % 360)
            result = x * y + z
            
            # Инкрементируем счетчики
            operations += 1
            
            # Проверяем, не пора ли завершить тест
            if time.time() >= end_time:
                break
    
    # Вычисляем итоговый результат
    elapsed_time = time.time() - start_time
    score = int(operations / elapsed_time * 1000)  # Нормализованный счет
    
    return {
        'operations': operations,
        'elapsed_time': elapsed_time,
        'score': score
    }

def multi_thread_benchmark(duration=10):
    """Выполняет многопоточный бенчмарк"""
    print(f"🚀 Запуск многопоточного теста ({duration} секунд)...")
    print("   Используются все доступные ядра CPU...")
    print()
    
    # Определяем количество ядер
    num_cores = os.cpu_count()
    if not num_cores:
        num_cores = 1
    
    print(f"   Доступно ядер: {num_cores}")
    
    # Создаем потоки
    threads = []
    results = []
    
    # Функция для выполнения в потоке
    def thread_worker(thread_id, results_list):
        start_time = time.time()
        end_time = start_time + duration
        operations = 0
        
        while time.time() < end_time:
            # Математические операции для нагрузки на CPU
            for _ in range(500):
                x = math.sqrt(operations % 1000 + 1)
                y = math.sin(operations % 360)
                z = math.cos(operations % 360)
                result = x * y + z
                operations += 1
                
                if time.time() >= end_time:
                    break
        
        results_list.append({
            'thread_id': thread_id,
            'operations': operations,
            'elapsed_time': time.time() - start_time
        })
    
    # Запускаем потоки
    for i in range(num_cores):
        thread = threading.Thread(target=thread_worker, args=(i, results))
        threads.append(thread)
        thread.start()
    
    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()
    
    # Считаем общие результаты
    total_operations = sum(r['operations'] for r in results)
    avg_elapsed_time = sum(r['elapsed_time'] for r in results) / len(results)
    score = int(total_operations / avg_elapsed_time * 1000)
    
    return {
        'threads': len(results),
        'total_operations': total_operations,
        'avg_elapsed_time': avg_elapsed_time,
        'score': score,
        'per_thread': results
    }

def memory_benchmark():
    """Выполняет тест памяти"""
    print("🧠 Запуск теста памяти...")
    print()
    
    start_time = time.time()
    
    # Создаем и обрабатываем большие массивы данных
    data_size = 1000000  # 1 миллион элементов
    test_data = []
    
    # Заполняем массив
    for i in range(data_size):
        test_data.append(i * 2.5)
    
    # Выполняем операции с массивом
    sum_value = 0
    for i in range(0, len(test_data), 10):
        sum_value += test_data[i]
    
    # Модифицируем данные
    for i in range(len(test_data)):
        test_data[i] = test_data[i] * 1.1
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Очищаем память
    del test_data
    
    return {
        'data_size': data_size,
        'elapsed_time': elapsed_time,
        'memory_score': int(data_size / elapsed_time * 100)
    }

def display_system_info():
    """Отображает информацию о системе"""
    print("💻 Информация о системе:")
    print("-" * 30)
    
    print(f"ОС: {platform.system()} {platform.release()}")
    print(f"Архитектура: {platform.machine()}")
    print(f"Процессор: {platform.processor()}")
    
    # Количество ядер
    physical_cores = os.cpu_count()
    if physical_cores:
        print(f"Ядер CPU: {physical_cores}")
    
    print()

def display_single_thread_results(results):
    """Отображает результаты однопоточного теста"""
    print("📈 Результаты однопоточного теста:")
    print("-" * 30)
    print(f"Выполнено операций: {results['operations']:,}")
    print(f"Время теста: {results['elapsed_time']:.2f} секунд")
    print(f"Производительность: {results['score']:,} ops/sec")
    print()

def display_multi_thread_results(results):
    """Отображает результаты многопоточного теста"""
    print("📈 Результаты многопоточного теста:")
    print("-" * 30)
    print(f"Потоков: {results['threads']}")
    print(f"Всего операций: {results['total_operations']:,}")
    print(f"Среднее время: {results['avg_elapsed_time']:.2f} секунд")
    print(f"Производительность: {results['score']:,} ops/sec")
    print()

def display_memory_results(results):
    """Отображает результаты теста памяти"""
    print("📈 Результаты теста памяти:")
    print("-" * 30)
    print(f"Размер данных: {results['data_size']:,} элементов")
    print(f"Время обработки: {results['elapsed_time']:.3f} секунд")
    print(f"Оценка памяти: {results['memory_score']:,} ops/sec")
    print()

def compare_with_benchmarks(score):
    """Сравнивает результаты с известными бенчмарками"""
    print("📊 Сравнение с другими системами:")
    print("-" * 30)
    
    # Примерные значения для сравнения (условные)
    benchmarks = {
        "Raspberry Pi 4": 500000,
        "Intel i3 (старый)": 2000000,
        "Intel i5 (средний)": 4000000,
        "Intel i7 (новый)": 7000000,
        "Intel i9 (высокий)": 10000000,
        "AMD Ryzen 7": 8000000
    }
    
    print("Ваш результат:", f"{score:,} ops/sec")
    print()
    
    closest_system = None
    closest_score = float('inf')
    
    for system, system_score in benchmarks.items():
        print(f"{system}: {system_score:,} ops/sec")
        # Находим ближайшую систему по производительности
        diff = abs(score - system_score)
        if diff < closest_score:
            closest_score = diff
            closest_system = system
    
    if closest_system:
        print(f"\nБлиже всего к: {closest_system}")
    print()

def show_benchmark_tips():
    """Показывает советы по бенчмарку"""
    print("💡 Советы по повышению производительности:")
    print("-" * 40)
    print("• Закройте ненужные приложения перед тестированием")
    print("• Убедитесь, что система охлаждается должным образом")
    print("• Проверьте, не ограничивает ли питание производительность")
    print("• Для точных результатов проведите тест несколько раз")
    print("• Сравнивайте результаты только на одинаковых конфигурациях")
    print()

def main():
    """Главная функция бенчмарка процессора"""
    print_header()
    
    try:
        # Отображаем информацию о системе
        display_system_info()
        
        # Запрашиваем у пользователя тип теста
        print("Выберите тип теста:")
        print(" [1] Однопоточный бенчмарк (10 секунд)")
        print(" [2] Многопоточный бенчмарк (10 секунд)")
        print(" [3] Тест памяти")
        print(" [4] Полный тест (все вышеперечисленное)")
        print()
        
        choice = input("Введите номер теста (1-4): ").strip()
        
        start_time = datetime.now()
        
        if choice == "1":
            # Однопоточный тест
            results = cpu_benchmark_test(10)
            display_single_thread_results(results)
            compare_with_benchmarks(results['score'])
            
        elif choice == "2":
            # Многопоточный тест
            results = multi_thread_benchmark(10)
            display_multi_thread_results(results)
            compare_with_benchmarks(results['score'])
            
        elif choice == "3":
            # Тест памяти
            results = memory_benchmark()
            display_memory_results(results)
            
        elif choice == "4":
            # Полный тест
            print("🔄 Выполняем полный тест...")
            print()
            
            # Однопоточный тест
            single_results = cpu_benchmark_test(10)
            display_single_thread_results(single_results)
            
            # Многопоточный тест
            multi_results = multi_thread_benchmark(10)
            display_multi_thread_results(multi_results)
            
            # Тест памяти
            memory_results = memory_benchmark()
            display_memory_results(memory_results)
            
            # Сравнение с бенчмарками (по многопоточному результату)
            compare_with_benchmarks(multi_results['score'])
        else:
            print("❌ Неверный выбор")
            input("\nНажмите Enter для выхода...")
            return
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Показываем советы
        show_benchmark_tips()
        
        print(f"✅ Тест завершен!")
        print(f"⏱️  Общее время тестирования: {duration.total_seconds():.1f} секунд")
        print(f"⏰ Завершено: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Тест прерван пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()