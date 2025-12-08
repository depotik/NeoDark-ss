#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import platform
import time
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Проверяем, запущен ли скрипт из main.py
CALLED_FROM_MAIN = len(sys.argv) > 1 and sys.argv[1] == '--from-main'

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 120

def print_center(text):
    width = get_terminal_width()
    lines = text.split('\n')
    for line in lines:
        # Удаляем цветовые коды для подсчета длины
        clean_line = line
        while '\033[' in clean_line and 'm' in clean_line:
            start = clean_line.find('\033[')
            end = clean_line.find('m', start)
            if end != -1:
                clean_line = clean_line[:start] + clean_line[end+1:]
        
        # Центрируем с сохранением цветов
        padding = max(0, (width - len(clean_line)) // 2)
        print(' ' * padding + line)

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f'''{Fore.CYAN}
███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ 
██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{Style.RESET_ALL}'''
    
    print_center(banner)
    print_center(f'{Fore.YELLOW}NeoDark-CLI | Creator: @weeaave{Style.RESET_ALL}')
    print_center(f'{Fore.LIGHTBLACK_EX}Special for NeoDark Ecosystem | Universal DNS Launcher{Style.RESET_ALL}')
    print()
    print_center(f'{Fore.MAGENTA}╔═══════════════════════════════════════════════════════╗{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}║         UNIVERSAL DNS CONFIGURATION LAUNCHER        ║{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}║     Auto-detection and manual Windows version       ║{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}')
    print()

def detect_windows_version():
    """Определение версии Windows"""
    system = platform.system()
    if system != "Windows":
        return "not_windows"
    
    version = platform.version()
    release = platform.release()
    win_ver = platform.win32_ver()
    
    print(f"{Fore.CYAN}[*] Определение системы...{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Система: {system} {release}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Версия: {version}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Сборка: {win_ver[2] if len(win_ver) > 2 else 'N/A'}{Style.RESET_ALL}")
    
    # Анализ версии Windows
    if release == "10":
        try:
            build = int(win_ver[2].split('.')[0]) if win_ver[2] else 0
            if build >= 22000:
                print(f"{Fore.GREEN}[✓] Определено: Windows 11 (Build {build}){Style.RESET_ALL}")
                return "windows11"
            else:
                print(f"{Fore.GREEN}[✓] Определено: Windows 10 (Build {build}){Style.RESET_ALL}")
                return "windows10"
        except:
            print(f"{Fore.YELLOW}[!] Не удалось определить точную версию{Style.RESET_ALL}")
            return "unknown"
    elif release == "11":
        print(f"{Fore.GREEN}[✓] Определено: Windows 11{Style.RESET_ALL}")
        return "windows11"
    else:
        print(f"{Fore.YELLOW}[!] Версия Windows: {release} (нестандартная){Style.RESET_ALL}")
        return "unknown"

def run_script(script_name):
    """Запуск внешнего скрипта"""
    if os.path.exists(script_name):
        print(f"{Fore.CYAN}[*] Запуск {script_name}...{Style.RESET_ALL}")
        time.sleep(1)
        
        # Запускаем скрипт
        result = subprocess.run([sys.executable, script_name], 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"{Fore.RED}[!] Ошибка запуска скрипта{Style.RESET_ALL}")
            print(f"{Fore.RED}Детали: {result.stderr}{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}[Нажмите Enter для возврата в меню...]{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] Скрипт {script_name} не найден!{Style.RESET_ALL}")
        time.sleep(2)

def show_menu(windows_version):
    """Отображение меню в зависимости от версии Windows"""
    
    # Определяем доступные опции
    if windows_version == "windows11":
        version_text = f"{Fore.GREEN}Windows 11{Style.RESET_ALL}"
        setup_script = "setdpiWin11.py"
        reset_script = "resetdpiWin11.py"
    elif windows_version == "windows10":
        version_text = f"{Fore.CYAN}Windows 10{Style.RESET_ALL}"
        setup_script = "setdpiWin10.py"
        reset_script = "resetdpiWin10.py"
    else:
        version_text = f"{Fore.YELLOW}Неизвестная версия{Style.RESET_ALL}"
        setup_script = None
        reset_script = None
    
    print(f"\n{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}ТЕКУЩАЯ СИСТЕМА: {version_text}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    
    exit_text = "Вернуться в главное меню" if CALLED_FROM_MAIN else "Выход из программы"
    menu = f'''
{Fore.CYAN}╔═══════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║                    ГЛАВНОЕ МЕНЮ                      ║{Style.RESET_ALL}
{Fore.CYAN}╠═══════════════════════════════════════════════════════╣{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.WHITE}1.{Fore.CYAN} │ Настройка DoH (ручные DNS + шифрование)      ║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.WHITE}2.{Fore.CYAN} │ Сброс к DHCP (сохраняя DoH шаблон)          ║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.WHITE}3.{Fore.CYAN} │ Сменить версию Windows вручную              ║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.WHITE}4.{Fore.CYAN} │ Проверить текущие настройки DNS             ║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.WHITE}5.{Fore.CYAN} │ Показать информацию о системе              ║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.WHITE}0.{Fore.CYAN} │ {exit_text:<47}║{Style.RESET_ALL}
{Fore.CYAN}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
'''
    
    print_center(menu)
    
    if windows_version == "unknown":
        print(f"{Fore.RED}[!] Внимание: Не удалось определить версию Windows{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Пожалуйста, выберите версию вручную (опция 3){Style.RESET_ALL}")
    
    return setup_script, reset_script

def check_dns_settings():
    """Проверка текущих DNS настроек"""
    print(f"\n{Fore.CYAN}[*] Проверка текущих DNS настроек...{Style.RESET_ALL}")
    
    check_cmd = '''
    # Получаем информацию о DNS
    Write-Output "═" * 60
    Write-Output "АКТИВНЫЕ СЕТЕВЫЕ АДАПТЕРЫ:"
    Write-Output "═" * 60
    
    Get-NetAdapter -Physical | Where-Object { $_.Status -eq 'Up' } | ForEach-Object {
        $adapter = $_
        Write-Output ""
        Write-Output "▶ Адаптер: $($adapter.Name)"
        Write-Output "  Описание: $($adapter.InterfaceDescription)"
        
        # Получаем DNS серверы
        $dnsServers = Get-DnsClientServerAddress -InterfaceAlias $adapter.Name -AddressFamily IPv4 -ErrorAction SilentlyContinue
        if ($dnsServers -and $dnsServers.ServerAddresses.Count -gt 0) {
            Write-Output "  DNS серверы: $($dnsServers.ServerAddresses -join ', ')"
        } else {
            Write-Output "  DNS серверы: Автоматически (DHCP)"
        }
        
        # Проверяем DoH настройки
        $interfaceDoh = Get-DnsClientDohServerAddress -InterfaceAlias $adapter.Name -ErrorAction SilentlyContinue
        if ($interfaceDoh) {
            Write-Output "  DoH: Включено"
            $interfaceDoh | ForEach-Object {
                Write-Output "    • $($_.ServerAddress): $($_.DohTemplate)"
            }
        } else {
            Write-Output "  DoH: Отключено"
        }
    }
    
    Write-Output ""
    Write-Output "═" * 60
    Write-Output "ГЛОБАЛЬНЫЕ DOH НАСТРОЙКИ:"
    Write-Output "═" * 60
    
    $globalDoh = Get-DnsClientDohServerAddress -ErrorAction SilentlyContinue
    if ($globalDoh) {
        $globalDoh | ForEach-Object {
            Write-Output "• $($_.ServerAddress): $($_.DohTemplate)"
        }
    } else {
        Write-Output "Нет зарегистрированных DoH серверов"
    }
    '''
    
    try:
        result = subprocess.run(["powershell", "-Command", check_cmd], 
                               capture_output=True, text=True, encoding='cp866')
        print(result.stdout)
    except Exception as e:
        print(f"{Fore.RED}[!] Ошибка проверки: {e}{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}[Нажмите Enter для продолжения...]{Style.RESET_ALL}")

def system_info():
    """Показать информацию о системе"""
    print(f"\n{Fore.CYAN}[*] Информация о системе...{Style.RESET_ALL}")
    
    info_cmd = '''
    # Системная информация
    Write-Output "═" * 60
    Write-Output "СИСТЕМНАЯ ИНФОРМАЦИЯ:"
    Write-Output "═" * 60
    
    $os = Get-CimInstance -ClassName Win32_OperatingSystem
    $computer = Get-CimInstance -ClassName Win32_ComputerSystem
    
    Write-Output "Операционная система: $($os.Caption)"
    Write-Output "Версия: $($os.Version)"
    Write-Output "Сборка: $($os.BuildNumber)"
    Write-Output "Архитектура: $($os.OSArchitecture)"
    Write-Output "Производитель: $($os.Manufacturer)"
    Write-Output ""
    Write-Output "Имя компьютера: $($computer.Name)"
    Write-Output "Пользователь: $($computer.UserName)"
    Write-Output "Модель: $($computer.Model)"
    Write-Output ""
    
    Write-Output "═" * 60
    Write-Output "СЕТЕВЫЕ ИНТЕРФЕЙСЫ:"
    Write-Output "═" * 60
    
    Get-NetAdapter -Physical | ForEach-Object {
        $statusIcon = if ($_.Status -eq 'Up') { '🟢' } else { '🔴' }
        Write-Output "$statusIcon $($_.Name): $($_.InterfaceDescription)"
        Write-Output "   MAC: $($_.MacAddress)"
        Write-Output "   Скорость: $($_.LinkSpeed)"
        Write-Output ""
    }
    '''
    
    try:
        result = subprocess.run(["powershell", "-Command", info_cmd], 
                               capture_output=True, text=True, encoding='cp866')
        print(result.stdout)
    except Exception as e:
        print(f"{Fore.RED}[!] Ошибка получения информации: {e}{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}[Нажмите Enter для продолжения...]{Style.RESET_ALL}")

def manual_version_select():
    """Ручной выбор версии Windows"""
    print(f"\n{Fore.CYAN}[*] Ручной выбор версии Windows{Style.RESET_ALL}")
    
    versions = [
        ("Windows 10", "windows10"),
        ("Windows 11", "windows11"),
        ("Не знаю / Другая", "unknown")
    ]
    
    print(f"\n{Fore.YELLOW}Выберите вашу версию Windows:{Style.RESET_ALL}")
    for i, (name, value) in enumerate(versions, 1):
        print(f"{Fore.WHITE}{i}.{Style.RESET_ALL} {name}")
    
    try:
        choice = int(input(f"\n{Fore.CYAN}Ваш выбор (1-{len(versions)}): {Style.RESET_ALL}"))
        if 1 <= choice <= len(versions):
            selected = versions[choice-1][1]
            print(f"{Fore.GREEN}[✓] Выбрана версия: {versions[choice-1][0]}{Style.RESET_ALL}")
            time.sleep(1)
            return selected
        else:
            print(f"{Fore.RED}[!] Неверный выбор{Style.RESET_ALL}")
            return "unknown"
    except ValueError:
        print(f"{Fore.RED}[!] Введите число{Style.RESET_ALL}")
        return "unknown"

def main():
    """Главная функция лаунчера"""
    current_version = None
    
    while True:
        print_banner()
        
        # Определяем версию Windows если еще не определена
        if current_version is None:
            current_version = detect_windows_version()
            if current_version == "not_windows":
                print(f"{Fore.RED}[!] Эта программа предназначена только для Windows!{Style.RESET_ALL}")
                input(f"{Fore.CYAN}[Нажмите Enter для выхода...]{Style.RESET_ALL}")
                sys.exit(1)
        
        # Показываем меню
        setup_script, reset_script = show_menu(current_version)
        
        # Получаем выбор пользователя
        try:
            choice = input(f"\n{Fore.CYAN}Выберите опцию (0-5): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                if setup_script:
                    run_script(setup_script)
                else:
                    print(f"{Fore.RED}[!] Скрипт настройки не доступен для этой версии{Style.RESET_ALL}")
                    time.sleep(2)
            
            elif choice == "2":
                if reset_script:
                    run_script(reset_script)
                else:
                    print(f"{Fore.RED}[!] Скрипт сброса не доступен для этой версии{Style.RESET_ALL}")
                    time.sleep(2)
            
            elif choice == "3":
                current_version = manual_version_select()
            
            elif choice == "4":
                check_dns_settings()
            
            elif choice == "5":
                system_info()
            
            elif choice == "0":
                if CALLED_FROM_MAIN:
                    # Возвращаемся в главное меню main.py
                    print(f"\n{Fore.YELLOW}[*] Возврат в главное меню...{Style.RESET_ALL}")
                    time.sleep(1)
                    sys.exit(0)
                else:
                    # Выходим из программы
                    print(f"\n{Fore.YELLOW}[*] Выход из программы...{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Спасибо за использование NeoDark-CLI!{Style.RESET_ALL}")
                    time.sleep(2)
                    break
            
            else:
                print(f"{Fore.RED}[!] Неверный выбор. Попробуйте снова.{Style.RESET_ALL}")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}[!] Программа прервана пользователем{Style.RESET_ALL}")
            if not CALLED_FROM_MAIN:
                print(f"{Fore.GREEN}До свидания!{Style.RESET_ALL}")
            time.sleep(1)
            sys.exit(0 if CALLED_FROM_MAIN else 1)
        
        except Exception as e:
            print(f"{Fore.RED}[!] Ошибка: {e}{Style.RESET_ALL}")
            time.sleep(2)

if __name__ == "__main__":
    # Проверяем, запущен ли скрипт на Windows
    if os.name != 'nt':
        print(f"{Fore.RED}Ошибка: Эта программа работает только на Windows!{Style.RESET_ALL}")
        sys.exit(1)
    
    main()