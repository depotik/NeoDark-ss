import os
import sys
from datetime import datetime

def print_header():
    """Выводит заголовок программы"""
    print("⌨️ Управление горячими клавишами")
    print("=" * 45)

def get_neodark_banner():
    """Возвращает баннер NeoDark"""
    return '''\033[96m███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ 
██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝\033[0m'''

def show_neodark_logo():
    """Показывает логотип NeoDark"""
    print(get_neodark_banner())
    print()

def show_hotkey_info():
    """Показывает информацию о горячих клавишах"""
    print("ℹ️ Горячие клавиши NeoDark:")
    print("-" * 35)
    print("   Горячие клавиши позволяют быстро")
    print("   выполнять часто используемые функции.")
    print()
    print("   Преимущества:")
    print("   • Повышение производительности")
    print("   • Удобство использования")
    print("   • Быстрый доступ к функциям")
    print("   • Индивидуальная настройка")

def list_current_hotkeys():
    """Показывает текущие горячие клавиши"""
    print("\n⌨️ Текущие горячие клавиши:")
    print("-" * 40)
    
    # Демонстрационные горячие клавиши
    hotkeys = [
        ("Ctrl+Shift+S", "Статус системы"),
        ("Ctrl+Shift+C", "Очистить кэш"),
        ("Ctrl+Shift+Z", "Включить Zapret"),
        ("Ctrl+Shift+M", "Matrix-rain"),
        ("Ctrl+Shift+T", "Проверка портов"),
        ("Ctrl+Shift+P", "Синхронизация продуктов"),
        ("Ctrl+Shift+U", "Проверить обновления"),
        ("Ctrl+Shift+R", "Перезапустить NeoDark"),
        ("Ctrl+Shift+Q", "Выход"),
        ("F1", "Помощь"),
        ("F5", "Обновить"),
        ("F12", "Открыть консоль")
    ]
    
    print(f"{'Комбинация':<20} {'Функция':<30}")
    print("-" * 55)
    
    for combo, function in hotkeys:
        print(f"{combo:<20} {function:<30}")

def configure_hotkey_demo():
    """Демонстрация настройки горячих клавиш"""
    print("\n⚙️ Настройка горячих клавиш (демо):")
    print("-" * 40)
    
    try:
        # Получаем информацию о новой горячей клавише
        print("Добавление новой горячей клавиши:")
        key_combo = input("Комбинация клавиш (например, Ctrl+Shift+K): ").strip()
        if not key_combo:
            key_combo = "Ctrl+Shift+K"
            print(f"Используется комбинация: {key_combo}")
        
        print("\nДоступные функции:")
        functions = [
            "Статус системы",
            "Очистить кэш",
            "Включить Zapret",
            "Matrix-rain",
            "Проверка портов",
            "Синхронизация продуктов",
            "Проверить обновления",
            "Открыть консоль"
        ]
        
        for i, func in enumerate(functions, 1):
            print(f"   [{i}] {func}")
        
        func_choice = input("\nВыберите функцию (1-8): ").strip()
        if not func_choice or not func_choice.isdigit() or not (1 <= int(func_choice) <= len(functions)):
            func_choice = "1"
        
        selected_function = functions[int(func_choice) - 1]
        
        # Имитация настройки
        print("\n🔄 Настройка горячей клавиши...")
        
        import time
        steps = [
            "Проверка доступности комбинации",
            "Создание обработчика события",
            "Регистрация горячей клавиши",
            "Тестирование комбинации",
            "Сохранение конфигурации"
        ]
        
        for i, step in enumerate(steps, 1):
            print(f"   [{i}/{len(steps)}] {step}...")
            time.sleep(0.7)
        
        print("✅ Горячая клавиша успешно настроена!")
        print(f"⌨️  {key_combo} → {selected_function}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка настройки горячей клавиши: {e}")
        return False

def show_hotkey_tips():
    """Показывает советы по горячим клавишам"""
    print("\n💡 Советы по горячим клавишам:")
    print("-" * 35)
    print("   • Используйте интуитивные комбинации")
    print("   • Избегайте конфликтов с системными")
    print("   • Группируйте по функциональности")
    print("   • Документируйте свои комбинации")
    print("   • Используйте стандартные сочетания")
    print("   • Регулярно пересматривайте настройки")

def show_hotkey_management():
    """Показывает управление горячими клавишами"""
    print("\n🔧 Управление горячими клавишами:")
    print("-" * 35)
    print("   [1] Добавить горячую клавишу")
    print("   [2] Удалить горячую клавишу")
    print("   [3] Изменить горячую клавишу")
    print("   [4] Сбросить к стандартным")
    print("   [5] Экспорт конфигурации")
    print("   [6] Импорт конфигурации")

def main():
    """Главная функция управления горячими клавишами"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Показываем информацию
        show_hotkey_info()
        
        # Показываем текущие горячие клавиши
        list_current_hotkeys()
        
        # Показываем советы
        show_hotkey_tips()
        
        # Показываем управление
        show_hotkey_management()
        
        # Демонстрация настройки
        print("\n" + "=" * 45)
        if configure_hotkey_demo():
            print("\n🎉 Горячая клавиша успешно настроена!")
        else:
            print("\n⚠️  Настройка горячей клавиши не выполнена")
        
        print(f"\n✅ Работа завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Операция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()