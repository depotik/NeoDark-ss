import os
import sys
import platform
import re
import time
from datetime import datetime
from pathlib import Path

def print_header():
    """Выводит заголовок программы"""
    print("🔍 Поиск по файлам (Grep-like) NeoDark")
    print("=" * 50)

def get_search_parameters():
    """Получает параметры поиска от пользователя"""
    print("Настройка поиска:")
    
    # Получаем директорию для поиска
    print("\nДиректория для поиска:")
    print(" [1] Текущая директория")
    print(" [2] Указать путь")
    print(" [3] Домашняя директория")
    
    dir_choice = input("Выберите опцию (1-3): ").strip()
    
    if dir_choice == "1":
        search_dir = os.getcwd()
    elif dir_choice == "2":
        search_dir = input("Введите путь к директории: ").strip()
        if not os.path.exists(search_dir):
            print("❌ Директория не найдена")
            return None, None, None, None
    elif dir_choice == "3":
        search_dir = Path.home()
    else:
        print("❌ Неверный выбор")
        return None, None, None, None
    
    print(f"\nВыбранная директория: {search_dir}")
    
    # Получаем шаблон поиска
    search_pattern = input("\nВведите шаблон поиска (регулярное выражение или текст): ").strip()
    if not search_pattern:
        print("❌ Шаблон поиска не может быть пустым")
        return None, None, None, None
    
    # Получаем фильтры файлов
    print("\nФильтр файлов (оставьте пустым для всех файлов):")
    print("Примеры: *.py, *.txt, *.log, config.*")
    file_filter = input("Фильтр файлов: ").strip()
    
    # Получаем опции поиска
    print("\nОпции поиска:")
    case_sensitive = input("Учитывать регистр? (y/N): ").strip().lower() in ['y', 'yes', 'д', 'да']
    recursive = input("Рекурсивный поиск? (Y/n): ").strip().lower() not in ['n', 'no', 'н', 'нет']
    
    return search_dir, search_pattern, file_filter, {
        'case_sensitive': case_sensitive,
        'recursive': recursive
    }

def matches_file_filter(filename, file_filter):
    """Проверяет, соответствует ли файл фильтру"""
    if not file_filter:
        return True
    
    # Простая реализация фильтра файлов
    if '*' in file_filter:
        # Преобразуем в регулярное выражение
        pattern = file_filter.replace('.', '\\.').replace('*', '.*')
        return re.match(pattern, filename, re.IGNORECASE)
    else:
        # Простое сравнение
        return file_filter.lower() in filename.lower()

def search_in_file(file_path, pattern, case_sensitive):
    """Ищет шаблон в файле"""
    results = []
    
    try:
        # Определяем режим открытия файла в зависимости от регистра
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # Читаем файл
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line_num, line in enumerate(file, 1):
                # Ищем совпадения
                if re.search(pattern, line, flags):
                    results.append({
                        'line_number': line_num,
                        'line_content': line.rstrip('\n\r'),
                        'file_path': file_path
                    })
    except Exception as e:
        # Игнорируем ошибки чтения файлов
        pass
    
    return results

def search_files(search_dir, pattern, file_filter, options):
    """Выполняет поиск по файлам"""
    print(f"\n🚀 Начинаем поиск в директории: {search_dir}")
    print(f"Шаблон поиска: {pattern}")
    if file_filter:
        print(f"Фильтр файлов: {file_filter}")
    print(f"Учитывать регистр: {'Да' if options['case_sensitive'] else 'Нет'}")
    print(f"Рекурсивный поиск: {'Да' if options['recursive'] else 'Нет'}")
    print("\n" + "=" * 50)
    
    start_time = time.time()
    found_results = []
    files_checked = 0
    
    try:
        # Проходим по файлам
        if options['recursive']:
            # Рекурсивный поиск
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    # Проверяем фильтр файлов
                    if matches_file_filter(file, file_filter):
                        file_path = os.path.join(root, file)
                        try:
                            results = search_in_file(file_path, pattern, options['case_sensitive'])
                            if results:
                                found_results.extend(results)
                            files_checked += 1
                            
                            # Показываем прогресс
                            if files_checked % 100 == 0:
                                print(f"Проверено файлов: {files_checked}")
                        except Exception:
                            continue
        else:
            # Нерекурсивный поиск только в указанной директории
            try:
                for item in os.listdir(search_dir):
                    item_path = os.path.join(search_dir, item)
                    if os.path.isfile(item_path):
                        # Проверяем фильтр файлов
                        if matches_file_filter(item, file_filter):
                            try:
                                results = search_in_file(item_path, pattern, options['case_sensitive'])
                                if results:
                                    found_results.extend(results)
                                files_checked += 1
                            except Exception:
                                continue
            except PermissionError:
                print("❌ Нет доступа к директории")
                return []
        
        end_time = time.time()
        search_time = end_time - start_time
        
        # Выводим результаты
        print("\n" + "=" * 50)
        print("📊 Результаты поиска:")
        print(f"Проверено файлов: {files_checked}")
        print(f"Найдено совпадений: {len(found_results)}")
        print(f"Время поиска: {search_time:.2f} секунд")
        print("=" * 50)
        
        if found_results:
            print("\n📋 Найденные совпадения:")
            # Группируем результаты по файлам
            files_with_matches = {}
            for result in found_results:
                file_path = result['file_path']
                if file_path not in files_with_matches:
                    files_with_matches[file_path] = []
                files_with_matches[file_path].append(result)
            
            # Выводим результаты
            for file_path, matches in files_with_matches.items():
                print(f"\n📄 {file_path}:")
                for match in matches[:10]:  # Показываем максимум 10 совпадений на файл
                    line_num = match['line_number']
                    line_content = match['line_content']
                    # Подсвечиваем совпадения
                    try:
                        flags = 0 if options['case_sensitive'] else re.IGNORECASE
                        highlighted = re.sub(
                            f'({re.escape(pattern)})', 
                            r'🌟\033[91m\1\033[0m🌟', 
                            line_content, 
                            flags=flags
                        )
                        print(f"   {line_num:4d}: {highlighted}")
                    except:
                        print(f"   {line_num:4d}: {line_content}")
                
                if len(matches) > 10:
                    print(f"   ... и еще {len(matches) - 10} совпадений")
        else:
            print("\n❌ Совпадений не найдено")
            
        return found_results
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Поиск прерван пользователем")
        return []
    except Exception as e:
        print(f"\n❌ Ошибка при поиске: {str(e)}")
        return []

def show_search_tips():
    """Показывает советы по поиску"""
    print("\n💡 Советы по использованию:")
    print("   • Используйте . для поиска во всех файлах")
    print("   • Используйте регулярные выражения для сложных шаблонов")
    print("   • Примеры фильтров: *.py, *.txt, config.*")
    print("   • Для поиска слов используйте \\bword\\b")
    print("   • Для игнорирования регистра не включайте опцию")
    print()

def main():
    """Главная функция поиска по файлам"""
    print_header()
    
    try:
        # Получаем параметры поиска
        search_dir, pattern, file_filter, options = get_search_parameters()
        if not search_dir:
            input("\nНажмите Enter для выхода...")
            return
        
        # Выполняем поиск
        results = search_files(search_dir, pattern, file_filter, options)
        
        # Показываем советы
        show_search_tips()
        
        print(f"\n✅ Поиск завершен!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Поиск прерван пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()