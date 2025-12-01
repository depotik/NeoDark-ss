import os
import sys
import platform
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

def print_header():
    """Выводит заголовок программы"""
    print("Планировщик задач NeoDark")
    print("=" * 40)

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

def show_scheduler_info():
    """Показывает информацию о планировщике задач"""
    print(" Планировщик задач NeoDark:")
    print("-" * 30)
    print("   Планировщик задач позволяет автоматизировать")
    print("   выполнение различных операций в заданное время.")
    print()
    print("   Возможности:")
    print("   • Запланировать выполнение скриптов")
    print("   • Настроить периодическое выполнение")
    print("   • Управление запланированными задачами")
    print("   • Логирование выполнения задач")
    print()

def get_system_scheduler():
    """Определяет системный планировщик задач"""
    system = platform.system()
    
    if system == "Windows":
        return "Task Scheduler"
    elif system == "Linux":
        return "cron"
    elif system == "Darwin":  # macOS
        return "launchd"
    else:
        return "unknown"

def schedule_task_windows():
    """Планирование задачи в Windows"""
    print("📅 Планирование задачи в Windows:")
    print("-" * 35)
    
    try:
        # Получаем информацию о задаче
        task_name = input("Название задачи: ").strip()
        if not task_name:
            print("❌ Название задачи не может быть пустым")
            return False
        
        # Путь к скрипту
        script_path = input("Путь к скрипту (или оставьте пустым для демонстрации): ").strip()
        if not script_path:
            script_path = os.path.abspath(__file__)
        
        # Время выполнения
        run_time = input("Время выполнения (ЧЧ:ММ, или оставьте пустым для 09:00): ").strip()
        if not run_time:
            run_time = "09:00"
        
        # Создаем bat-файл для задачи
        bat_content = f'''@echo off
REM Запланированная задача NeoDark: {task_name}
cd /d "{os.path.dirname(script_path)}"
python.exe "{script_path}"
'''
        
        # Сохраняем bat-файл
        bat_file = os.path.join(os.path.dirname(script_path), f"{task_name}.bat")
        with open(bat_file, 'w') as f:
            f.write(bat_content)
        
        print(f"   ✅ Создан файл задачи: {bat_file}")
        
        # Планируем задачу с помощью schtasks
        cmd = [
            'schtasks', '/create', 
            '/tn', task_name,
            '/tr', bat_file,
            '/sc', 'daily',
            '/st', run_time
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Задача '{task_name}' запланирована на {run_time} ежедневно")
            return True
        else:
            print(f"   ⚠️  Ошибка планирования задачи: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка планирования задачи: {e}")
        return False

def schedule_task_linux():
    """Планирование задачи в Linux (через cron)"""
    print("📅 Планирование задачи в Linux (cron):")
    print("-" * 40)
    
    try:
        # Получаем информацию о задаче
        task_name = input("Название задачи: ").strip()
        if not task_name:
            print("❌ Название задачи не может быть пустым")
            return False
        
        # Путь к скрипту
        script_path = input("Путь к скрипту (или оставьте пустым для демонстрации): ").strip()
        if not script_path:
            script_path = os.path.abspath(__file__)
        
        # Время выполнения
        print("   Формат времени: минуты часы день месяц день_недели")
        print("   Примеры:")
        print("   • 0 9 * * * - ежедневно в 09:00")
        print("   • 0 12 * * 1 - каждый понедельник в 12:00")
        print("   • 0 */6 * * * - каждые 6 часов")
        
        cron_time = input("Время выполнения (cron формат, или оставьте пустым для ежедневно в 09:00): ").strip()
        if not cron_time:
            cron_time = "0 9 * * *"
        
        # Создаем shell-скрипт для задачи
        script_content = f'''#!/bin/bash
# Запланированная задача NeoDark: {task_name}
cd "{os.path.dirname(script_path)}"
python3 "{script_path}"
'''
        
        # Сохраняем shell-скрипт
        sh_file = os.path.join(os.path.dirname(script_path), f"{task_name}.sh")
        with open(sh_file, 'w') as f:
            f.write(script_content)
        
        # Делаем исполняемым
        os.chmod(sh_file, 0o755)
        print(f"   ✅ Создан файл задачи: {sh_file}")
        
        # Добавляем задачу в crontab
        cron_entry = f"{cron_time} {sh_file} # NeoDark Task: {task_name}\n"
        
        # Получаем текущий crontab
        try:
            current_crontab = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            new_crontab = current_crontab.stdout + cron_entry
            
            # Записываем новый crontab
            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                print(f"   ✅ Задача '{task_name}' добавлена в crontab")
                print(f"   🕒 Расписание: {cron_time}")
                return True
            else:
                print("   ⚠️  Ошибка добавления задачи в crontab")
                return False
        except FileNotFoundError:
            print("   ⚠️  Команда crontab не найдена")
            print("   💡 Установите cron для использования планировщика")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка планирования задачи: {e}")
        return False

def schedule_task_macos():
    """Планирование задачи в macOS (через launchd)"""
    print("📅 Планирование задачи в macOS (launchd):")
    print("-" * 40)
    
    try:
        # Получаем информацию о задаче
        task_name = input("Название задачи: ").strip()
        if not task_name:
            print("❌ Название задачи не может быть пустым")
            return False
        
        # Путь к скрипту
        script_path = input("Путь к скрипту (или оставьте пустым для демонстрации): ").strip()
        if not script_path:
            script_path = os.path.abspath(__file__)
        
        # Создаем plist файл для launchd
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.neodark.{task_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{script_path}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>'''
        
        # Сохраняем plist файл
        plist_dir = Path.home() / "Library" / "LaunchAgents"
        plist_dir.mkdir(parents=True, exist_ok=True)
        plist_file = plist_dir / f"com.neodark.{task_name}.plist"
        
        with open(plist_file, 'w') as f:
            f.write(plist_content)
        
        print(f"   ✅ Создан файл задачи: {plist_file}")
        
        # Загружаем задачу
        result = subprocess.run(['launchctl', 'load', str(plist_file)], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Задача '{task_name}' загружена в launchd")
            return True
        else:
            print(f"   ⚠️  Ошибка загрузки задачи: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка планирования задачи: {e}")
        return False

def list_scheduled_tasks():
    """Показывает список запланированных задач"""
    print("\n📋 Список запланированных задач:")
    print("-" * 35)
    
    system = platform.system()
    
    try:
        if system == "Windows":
            # Показываем задачи из Task Scheduler
            result = subprocess.run(['schtasks', '/query', '/fo', 'TABLE'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                neodark_tasks = [line for line in lines if 'NeoDark' in line]
                if neodark_tasks:
                    print("   Задачи NeoDark:")
                    for task in neodark_tasks:
                        print(f"   {task}")
                else:
                    print("   Нет запланированных задач NeoDark")
            else:
                print("   ⚠️  Ошибка получения списка задач")
                
        elif system == "Linux":
            # Показываем задачи из crontab
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                neodark_tasks = [line for line in lines if 'NeoDark' in line]
                if neodark_tasks:
                    print("   Задачи NeoDark:")
                    for task in neodark_tasks:
                        print(f"   {task}")
                else:
                    print("   Нет запланированных задач NeoDark")
            else:
                print("   Нет задач в crontab или ошибка доступа")
                
        elif system == "Darwin":  # macOS
            # Показываем задачи из launchd
            launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
            if launch_agents_dir.exists():
                neodark_plists = list(launch_agents_dir.glob("com.neodark.*.plist"))
                if neodark_plists:
                    print("   Задачи NeoDark:")
                    for plist in neodark_plists:
                        print(f"   {plist.name}")
                else:
                    print("   Нет запланированных задач NeoDark")
            else:
                print("   Нет задач launchd")
                
    except Exception as e:
        print(f"   ❌ Ошибка получения списка задач: {e}")

def show_scheduling_examples():
    """Показывает примеры планирования задач"""
    print("\n📝 Примеры планирования задач:")
    print("-" * 35)
    
    examples = {
        "Windows": [
            "schtasks /create /tn \"NeoDark Backup\" /tr \"C:\\NeoDark\\backup.bat\" /sc daily /st 02:00",
            "schtasks /create /tn \"NeoDark Update\" /tr \"C:\\NeoDark\\update.bat\" /sc weekly /d MON /st 09:00"
        ],
        "Linux": [
            "0 2 * * * /home/user/NeoDark/backup.sh  # Ежедневно в 02:00",
            "0 9 * * 1 /home/user/NeoDark/update.sh  # Каждый понедельник в 09:00"
        ],
        "macOS": [
            "Используйте launchd plist файлы в ~/Library/LaunchAgents/",
            "Пример структуры plist с StartCalendarInterval"
        ]
    }
    
    system = platform.system()
    if system in examples:
        print(f"Для {system}:")
        for example in examples[system]:
            print(f"   {example}")

def main():
    """Главная функция планировщика задач"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Показываем информацию о планировщике
        show_scheduler_info()
        
        # Определяем системный планировщик
        scheduler = get_system_scheduler()
        print(f"💻 Обнаружен планировщик: {scheduler}")
        
        # Показываем меню
        print("\nВыберите действие:")
        print(" [1] Запланировать задачу")
        print(" [2] Просмотреть запланированные задачи")
        print(" [3] Примеры планирования")
        print(" [0] Выход")
        print()
        
        choice = input("Ваш выбор (0-3): ").strip()
        
        if choice == "1":
            # Планируем задачу
            system = platform.system()
            if system == "Windows":
                schedule_task_windows()
            elif system == "Linux":
                schedule_task_linux()
            elif system == "Darwin":  # macOS
                schedule_task_macos()
            else:
                print("❌ Неподдерживаемая система")
                
        elif choice == "2":
            # Показываем список задач
            list_scheduled_tasks()
            
        elif choice == "3":
            # Показываем примеры
            show_scheduling_examples()
            
        elif choice == "0":
            print("👋 Выход из планировщика задач...")
        else:
            print("❌ Неверный выбор")
        
        print(f"\n✅ Работа с планировщиком задач завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Работа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()