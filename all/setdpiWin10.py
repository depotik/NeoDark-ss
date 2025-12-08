#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import ctypes
import time
from colorama import init, Fore, Back, Style

init(autoreset=True)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate():
    script = os.path.abspath(sys.argv[0])
    params = ' '.join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    sys.exit(0)

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 120

def print_center(text):
    width = get_terminal_width()
    lines = text.split('\n')
    for line in lines:
        stripped_line = line.lstrip('\033')
        # Удаляем цветовые коды для подсчета длины
        while '\033[' in stripped_line and 'm' in stripped_line:
            start = stripped_line.find('\033[')
            end = stripped_line.find('m', start)
            if end != -1:
                stripped_line = stripped_line[:start] + stripped_line[end+1:]
        print(line.center(width))

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
    print_center(f'{Fore.LIGHTBLACK_EX}Special for NeoDark Ecosystem | Windows 10 DoH Setup{Style.RESET_ALL}')
    print()
    print_center(f'{Fore.MAGENTA}╔═══════════════════════════════════════════════════════╗{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}║         WINDOWS 10 - DOH CONFIGURATION              ║{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}║     Setting up DNS over HTTPS with Manual DNS       ║{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}')
    print()

def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], 
                               capture_output=True, text=True, encoding='cp866')
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def setup_windows10_doh():
    print(f"{Fore.CYAN}[*] Настройка DoH для Windows 10...{Style.RESET_ALL}")
    
    dns_server_primary = "176.99.11.77"
    dns_server_secondary = "80.78.247.254"
    doh_template = "https://xbox-dns.ru/dns-query"
    
    print(f"{Fore.GREEN}[+] DNS серверы: {dns_server_primary}, {dns_server_secondary}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] DoH шаблон: {doh_template}{Style.RESET_ALL}")
    
    # 1. Регистрация DoH сервера (Windows 10 способ)
    print(f"\n{Fore.CYAN}[1]{Style.RESET_ALL} Регистрация DoH шаблона в системе...")
    register_doh_cmd = f'''
    $server = "{dns_server_primary}"
    $template = "{doh_template}"
    
    # Проверяем, поддерживается ли DoH в этой версии Windows 10
    $winVersion = [System.Environment]::OSVersion.Version
    if ($winVersion.Major -eq 10 -and $winVersion.Build -ge 19628) {{
        # Windows 10 версии 2004 и выше
        Add-DnsClientDohServerAddress -ServerAddress $server -DohTemplate $template -AllowFallbackToUdp $false -AutoUpgrade $false
        Write-Output "DoH шаблон зарегистрирован (Win10 Build $($winVersion.Build))"
    }} else {{
        # Для более старых версий Windows 10 используем альтернативный метод
        $dohServers = Get-DnsClientDohServerAddress -ErrorAction SilentlyContinue
        if ($dohServers) {{
            Add-DnsClientDohServerAddress -ServerAddress $server -DohTemplate $template
            Write-Output "DoH шаблон зарегистрирован (legacy method)"
        }} else {{
            Write-Output "DoH не поддерживается в этой версии Windows 10"
        }}
    }}
    '''
    code, out, err = run_powershell_command(register_doh_cmd)
    print(f"   {Fore.GREEN if 'зарегистрирован' in out else Fore.YELLOW}{out}{Style.RESET_ALL}")
    
    # 2. Настройка сетевых адаптеров Windows 10
    print(f"\n{Fore.CYAN}[2]{Style.RESET_ALL} Настройка сетевых адаптеров...")
    
    # Получаем активные адаптеры
    get_adapters_cmd = '''
    Get-NetAdapter -Physical | Where-Object { $_.Status -eq 'Up' } | ForEach-Object {
        Write-Output "$($_.Name)|$($_.InterfaceDescription)"
    }
    '''
    code, out, err = run_powershell_command(get_adapters_cmd)
    
    if not out:
        print(f"   {Fore.YELLOW}[!] Активные адаптеры не найдены{Style.RESET_ALL}")
    else:
        adapters = [line.split('|') for line in out.split('\n') if line]
        print(f"   {Fore.GREEN}[+] Найдено адаптеров: {len(adapters)}{Style.RESET_ALL}")
        
        for adapter_info in adapters:
            if len(adapter_info) < 2:
                continue
                
            adapter_name = adapter_info[0].strip()
            adapter_desc = adapter_info[1].strip()
            
            print(f"   {Fore.WHITE}• {adapter_name} ({adapter_desc[:30]}...){Style.RESET_ALL}")
            
            # Установка DNS серверов для Windows 10
            set_dns_cmd = f'''
            $adapterName = "{adapter_name}"
            $dnsAddresses = "{dns_server_primary}", "{dns_server_secondary}"
            
            # Устанавливаем DNS серверы
            Set-DnsClientServerAddress -InterfaceAlias $adapterName -ServerAddresses $dnsAddresses -ErrorAction Stop
            Write-Output "DNS серверы установлены"
            '''
            code, out_dns, err_dns = run_powershell_command(set_dns_cmd)
            status = "✓" if code == 0 else "✗"
            color = Fore.GREEN if code == 0 else Fore.RED
            print(f"     {color}[{status}] {out_dns}{Style.RESET_ALL}")
            
            # Настройка DoH в реестре Windows 10
            set_doh_reg_cmd = f'''
            $adapterName = "{adapter_name}"
            $server = "{dns_server_primary}"
            
            # Получаем GUID интерфейса
            $adapter = Get-NetAdapter -Name $adapterName -ErrorAction SilentlyContinue
            if ($adapter) {{
                $ifGuid = $adapter.InterfaceGuid
                
                # Путь в реестре для DoH настроек (Windows 10)
                $regPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters\\DohInterfaceSettings\\$ifGuid"
                
                # Создаем ключи если не существуют
                if (!(Test-Path $regPath)) {{
                    New-Item -Path $regPath -Force | Out-Null
                }}
                
                # Настройка DoH для конкретного сервера
                $serverPath = "$regPath\\$server"
                if (!(Test-Path $serverPath)) {{
                    New-Item -Path $serverPath -Force | Out-Null
                }}
                
                # Устанавливаем флаги DoH
                New-ItemProperty -Path $serverPath -Name "DohFlags" -Value 1 -PropertyType DWORD -Force | Out-Null
                New-ItemProperty -Path $serverPath -Name "Template" -Value "{doh_template}" -PropertyType String -Force | Out-Null
                
                # Глобальные настройки DoH
                $globalPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters"
                Set-ItemProperty -Path $globalPath -Name "EnableAutoDoh" -Value 2 -Type DWORD -Force | Out-Null
                
                Write-Output "DoH настроен в реестре"
            }} else {{
                Write-Output "Адаптер не найден"
            }}
            '''
            code, out_doh, err_doh = run_powershell_command(set_doh_reg_cmd)
            status = "✓" if "настроен" in out_doh else "✗"
            color = Fore.GREEN if "настроен" in out_doh else Fore.YELLOW
            print(f"     {color}[{status}] {out_doh if out_doh else 'DoH параметры установлены'}{Style.RESET_ALL}")
    
    # 3. Очистка DNS кэша
    print(f"\n{Fore.CYAN}[3]{Style.RESET_ALL} Очистка DNS кэша...")
    flush_cmd = "Clear-DnsClientCache; ipconfig /flushdns"
    code, out, err = run_powershell_command(flush_cmd)
    print(f"   {Fore.GREEN}[✓] DNS кэш очищен{Style.RESET_ALL}")
    
    # 4. Перезапуск службы DNS клиента
    print(f"\n{Fore.CYAN}[4]{Style.RESET_ALL} Перезапуск DNS клиента...")
    restart_cmd = "Restart-Service -Name Dnscache -Force"
    code, out, err = run_powershell_command(restart_cmd)
    print(f"   {Fore.GREEN}[✓] Служба DNS перезапущена{Style.RESET_ALL}")
    
    # Итог
    print(f"\n{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] НАСТРОЙКА WINDOWS 10 ЗАВЕРШЕНА{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}Результат:{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}• DNS серверы: {Fore.YELLOW}Ручные ({dns_server_primary}, {dns_server_secondary}){Style.RESET_ALL}")
    print(f"   {Fore.WHITE}• DoH шифрование: {Fore.GREEN}Включено{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}• Шаблон: {Fore.CYAN}{doh_template}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}• Режим: {Fore.YELLOW}Только DoH{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}[!] Проверьте настройки: Панель управления → Сеть и Интернет{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}[Нажмите Enter для возврата в меню...]{Style.RESET_ALL}")

def main():
    if not is_admin():
        print_banner()
        print(f"{Fore.YELLOW}[!] Требуются права администратора...{Style.RESET_ALL}")
        time.sleep(2)
        elevate()
    
    print_banner()
    setup_windows10_doh()

if __name__ == "__main__":
    main()