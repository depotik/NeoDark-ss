import os
import sys
import platform
import subprocess
import time
from pathlib import Path

def print_header():
    """Выводит заголовок программы"""
    print("  Включение Zapret (Роскомнадзор блокировки)")
    print("=" * 55)

def check_platform():
    """Проверяет, поддерживается ли текущая платформа"""
    if platform.system() != "Windows":
        print(" Эта функция поддерживается только в Windows")
        return False
    return True

def find_zapret_directory():
    """Находит директорию zapret"""
    # Проверяем стандартные пути
    possible_paths = [
        Path("zapret"),
        Path("all/zapret"),
        Path("../zapret"),
        Path("all/zapret")
    ]
    
    for path in possible_paths:
        print(f"Проверяю путь: {path.absolute()}")  # Отладочная печать
        if path.exists() and (path / "general.bat").exists():
            print(f"Найден путь: {path.absolute()}")  # Отладочная печать
            return path
    
    # Если не найдено, проверяем текущую директорию
    current_dir = Path.cwd()
    print(f"Проверяю текущую директорию: {current_dir}")  # Отладочная печать
    if (current_dir / "general.bat").exists():
        return current_dir
        
    return None

def show_zapret_scripts(zapret_dir):
    """Показывает доступные скрипты zapret"""
    print("📂 Доступные конфигурации:")
    
    # Основные скрипты
    main_scripts = [
        ("general.bat", "Основная конфигурация"),
        ("general (МГТС).bat", "Для МГТС провайдеров"),
        ("general (FAKE TLS MOD).bat", "С фейковым TLS"),
        ("cloudflare_switch.bat", "Cloudflare переключатель")
    ]
    
    # Дополнительные скрипты
    alt_scripts = [
        ("general (ALT).bat", "Альтернативная конфигурация 1"),
        ("general (ALT2).bat", "Альтернативная конфигурация 2"),
        ("general (ALT3).bat", "Альтернативная конфигурация 3"),
        ("general (ALT4).bat", "Альтернативная конфигурация 4"),
        ("general (ALT5).bat", "Альтернативная конфигурация 5")
    ]
    
    print("\n🎯 Основные конфигурации:")
    for i, (script, description) in enumerate(main_scripts, 1):
        script_path = zapret_dir / script
        if script_path.exists():
            print(f"  [{i}] {description} ({script})")
        else:
            print(f"  [ ] {description} ({script}) - файл отсутствует")
    
    print("\n🔧 Альтернативные конфигурации:")
    for i, (script, description) in enumerate(alt_scripts, len(main_scripts) + 1):
        script_path = zapret_dir / script
        if script_path.exists():
            print(f"  [{i}] {description} ({script})")
        else:
            print(f"  [ ] {description} ({script}) - файл отсутствует")
    
    return main_scripts + alt_scripts

def run_zapret_script(zapret_dir, script_name):
    """Запускает выбранный скрипт zapret"""
    script_path = zapret_dir / script_name
    
    if not script_path.exists():
        print(f" Скрипт {script_name} не найден")
        return False
    
    try:
        print(f" Запуск скрипта: {script_name}")
        print(f" Полный путь: {script_path.absolute()}")  # Отладочная печать
        print("-" * 50)
        
        # Запуск скрипта
        if platform.system() == "Windows":
            # Используем абсолютный путь для рабочей директории
            absolute_cwd = zapret_dir.absolute()
            print(f" Рабочая директория: {absolute_cwd}")  # Отладочная печать
            result = subprocess.run(
                ["cmd", "/c", str(script_path.absolute())],  # Используем абсолютный путь к скрипту
                cwd=str(absolute_cwd),
                capture_output=False,
                text=True
            )
        else:
            # Для других систем
            result = subprocess.run(
                ["bash", str(script_path)],
                cwd=str(zapret_dir.absolute()),
                capture_output=False,
                text=True
            )
        
        if result.returncode == 0:
            print(" Скрипт выполнен успешно")
            return True
        else:
            print(f" Скрипт завершился с ошибкой (код: {result.returncode})")
            return False
            
    except Exception as e:
        print(f" Ошибка при запуске скрипта: {e}")

def show_service_options(zapret_dir):
    """Показывает опции управления службой"""
    print("\n  Управление службой Zapret:")
    
    service_scripts = [
        ("service_install.bat", "Установить службу"),
        ("service_remove.bat", "Удалить службу"),
        ("service_status.bat", "Проверить статус"),
        ("check_updates.bat", "Проверить обновления")
    ]
    
    for i, (script, description) in enumerate(service_scripts, 1):
        script_path = zapret_dir / script
        if script_path.exists():
            print(f"  [{i}] {description}")
        else:
            print(f"  [ ] {description} - файл отсутствует")
    
    return service_scripts

def run_service_script(zapret_dir, script_name):
    """Запускает скрипт управления службой"""
    script_path = zapret_dir / script_name
    
    if not script_path.exists():
        print(f" Скрипт {script_name} не найден")
        return False
    
    try:
        print(f" Выполнение: {script_name}")
        print("-" * 50)
        
        # Запуск скрипта
        result = subprocess.run(
            ["cmd", "/c", str(script_path)], 
            cwd=str(zapret_dir),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(" Операция выполнена успешно")
            return True
        else:
            print(f" Операция завершена с ошибкой (код: {result.returncode})")
            return False
            
    except Exception as e:
        print(f" Ошибка при выполнении операции: {e}")
        return False

def show_help():
    """Показывает справочную информацию"""
    print("\nℹ  Справка по Zapret:")
    print("   Zapret - это инструмент для обхода блокировок РКН с помощью DPI обфускации.")
    print("   Он работает на уровне сети и может помочь получить доступ к заблокированным сайтам.")
    print("\n     ВАЖНО:")
    print("   - Используйте только в законных целях")
    print("   - Убедитесь, что у вас есть права администратора")
    print("   - Некоторые конфигурации могут повлиять на скорость интернета")
    print("   - Регулярно проверяйте обновления списков")

def main():
    """Главная функция включения Zapret"""
    print_header()
    
    # Проверка платформы
    if not check_platform():
        input("\nНажмите Enter для выхода...")
        return
    
    # Поиск директории zapret
    zapret_dir = find_zapret_directory()
    if not zapret_dir:
        print(" Не удалось найти директорию zapret")
        print(" Убедитесь, что папка zapret находится в правильном месте")
        input("\nНажмите Enter для выхода...")
        return
    
    print(f" Найдена директория zapret: {zapret_dir}")
    
    while True:
        print("\n" + "=" * 55)
        print("Выберите действие:")
        print(" [1] Запустить конфигурацию Zapret")
        print(" [2] Управление службой")
        print(" [3] Справка")
        print(" [0] Выход")
        print("-" * 55)
        
        try:
            choice = input("Введите номер действия: ").strip()
            
            if choice == "0":
                print(" Выход из программы...")
                break
            elif choice == "1":
                # Показываем доступные скрипты
                scripts = show_zapret_scripts(zapret_dir)
                print("\n" + "-" * 55)
                script_choice = input("Выберите конфигурацию (0 для отмены): ").strip()
                
                if script_choice == "0":
                    continue
                    
                try:
                    script_index = int(script_choice) - 1
                    if 0 <= script_index < len(scripts):
                        script_name = scripts[script_index][0]
                        run_zapret_script(zapret_dir, script_name)
                    else:
                        print(" Неверный выбор")
                except ValueError:
                    print(" Неверный ввод")
                    
            elif choice == "2":
                # Показываем опции управления службой
                scripts = show_service_options(zapret_dir)
                print("\n" + "-" * 55)
                service_choice = input("Выберите действие (0 для отмены): ").strip()
                
                if service_choice == "0":
                    continue
                    
                try:
                    script_index = int(service_choice) - 1
                    if 0 <= script_index < len(scripts):
                        script_name = scripts[script_index][0]
                        run_service_script(zapret_dir, script_name)
                    else:
                        print(" Неверный выбор")
                except ValueError:
                    print(" Неверный ввод")
                    
            elif choice == "3":
                show_help()
            else:
                print(" Неверный выбор")
                
        except KeyboardInterrupt:
            print("\n\n  Программа прервана пользователем")
            break
        except Exception as e:
            print(f"\n Произошла ошибка: {str(e)}")
    
    print("\n Работа с Zapret завершена!")
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()