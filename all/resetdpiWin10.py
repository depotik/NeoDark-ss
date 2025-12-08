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
    print_center(f'{Fore.LIGHTBLACK_EX}Special for NeoDark Ecosystem | Windows 10 DHCP Reset{Style.RESET_ALL}')
    print()
    print_center(f'{Fore.MAGENTA}╔═══════════════════════════════════════════════════════╗{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}║         WINDOWS 10 - DHCP RESET                      ║{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}║     Resetting DNS to DHCP with DoH Template          ║{Style.RESET_ALL}')
    print_center(f'{Fore.MAGENTA}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}')
    print()

def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], 
                               capture_output=True, text=True, encoding='cp866')
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def reset_windows10_dhcp():
    print(f"{Fore.CYAN}[*] Сброс DNS настроек к DHCP для Windows 10...{Style.RESET_ALL}")
    
    doh_template = "https://xbox-dns.ru/dns-query"
    doh_server = "176.99.11.77"
    
    print(f"{Fore.YELLOW}[!] DoH шаблон останется активным: {doh_template}{Style.RESET_ALL}")
    
    # 1. Регистрация/проверка DoH шаблона
    print(f"\n{Fore.CYAN}[1]{Style.RESET_ALL} Проверка DoH шаблона...")
    check_doh_cmd = f'''
    $server = "{doh_server}"
    $template = "{doh_template}"
    
    # Проверяем, зарегистрирован ли шаблон
    $existing = Get-DnsClientDohServerAddress -ErrorAction SilentlyContinue | Where-Object {{ $_.ServerAddress -eq $server }}
    
    if (-not $existing) {{
        # Регистрируем если нет
        Add-DnsClientDohServerAddress -ServerAddress $server -DohTemplate $template -AllowFallbackToUdp $false -AutoUpgrade $false
        Write-Output "DoH шаблон зарегистрирован"
    }} else {{
        Write-Output "DoH шаблон уже активен"
    }}
    '''
    code, out, err = run_powershell_command(check_doh_cmd)
    print(f"   {Fore.GREEN}{out}{Style.RESET_ALL}")
    
    # 2. Получаем все сетевые адаптеры
    print(f"\n{Fore.CYAN}[2]{Style.RESET_ALL} Поиск сетевых адаптеров...")
    get_adapters_cmd = '''
    Get-NetAdapter -Physical | ForEach-Object {
        $statusIcon = if ($_.Status -eq 'Up') { '▲' } else { '▼' }
        Write-Output "$($_.Name)|$($_.Status)|$statusIcon|$($_.InterfaceDescription)"
    }
    '''
    code, out, err = run_powershell_command(get_adapters_cmd)
    
    if not out:
        print(f"   {Fore.YELLOW}[!] Адаптеры не найдены{Style.RESET_ALL}")
        return
    
    adapters = [line.split('|') for line in out.split('\n') if line]
    print(f"   {Fore.GREEN}[+] Найдено адаптеров: {len(adapters)}{Style.RESET_ALL}")
    
    # 3. Сброс DNS к DHCP для каждого адаптера
    print(f"\n{Fore.CYAN}[3]{Style.RESET_ALL} Сброс DNS к DHCP...")
    
    reset_count = 0
    for adapter_info in adapters:
        if len(adapter_info) < 4:
            continue
            
        adapter_name = adapter_info[0].strip()
        adapter_status = adapter_info[1].strip()
        status_icon = adapter_info[2].strip()
        adapter_desc = adapter_info[3].strip()[:30]
        
        status_color = Fore.GREEN if adapter_status == "Up" else Fore.RED
        print(f"   {status_color}{status_icon}{Style.RESET_ALL} {Fore.WHITE}{adapter_name} ({adapter_desc}...){Style.RESET_ALL}")
        
        # Сброс DNS серверов (возврат к DHCP) - Windows 10 метод
        reset_dns_cmd = f'''
        $adapterName = "{adapter_name}"
        
        # Способ 1: Удаляем статические DNS (предпочтительный для Windows 10)
        try {{
            Remove-DnsClientServerAddress -InterfaceAlias $adapterName -Confirm:$false -ErrorAction Stop
            $result = "DNS сброшены к DHCP"
        }} catch {{
            # Способ 2: Устанавливаем пустые серверы
            try {{
                Set-DnsClientServerAddress -InterfaceAlias $adapterName -ResetServerAddresses -ErrorAction Stop
                $result = "DNS сброшены (reset method)"
            }} catch {{
                # Способ 3: Через netsh (самый надежный для старых Win10)
                netsh interface ipv4 set dnsservers name="$adapterName" source=dhcp
                $result = "DNS сброшены (netsh)"
            }}
        }}
        
        # Проверяем результат
        $currentDNS = Get-DnsClientServerAddress -InterfaceAlias $adapterName -AddressFamily IPv4 -ErrorAction SilentlyContinue
        if ($currentDNS -and $currentDNS.ServerAddresses.Count -gt 0) {{
            Write-Output "Ошибка: DNS не сброшены"
        }} else {{
            Write-Output $result
        }}
        '''
        code, out_reset, err_reset = run_powershell_command(reset_dns_cmd)
        
        if "сброшены" in out_reset or "DHCP" in out_reset:
            reset_count += 1
            print(f"     {Fore.GREEN}[✓] {out_reset}{Style.RESET_ALL}")
        else:
            print(f"     {Fore.YELLOW}[!] {out_reset}{Style.RESET_ALL}")
        
        # 4. Настройка DoH в реестре Windows 10 для ручного шаблона
        print(f"     {Fore.WHITE}Настройка DoH шаблона...{Style.RESET_ALL}")
        
        set_doh_cmd = f'''
        $adapterName = "{adapter_name}"
        $server = "{doh_server}"
        
        $adapter = Get-NetAdapter -Name $adapterName -ErrorAction SilentlyContinue
        if ($adapter) {{
            $ifGuid = $adapter.InterfaceGuid
            
            # Windows 10 путь для DoH настроек
            $regBase = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Dnscache"
            
            # 1. Настройки для конкретного интерфейса
            $ifPath = "$regBase\\InterfaceSpecificParameters\\$ifGuid\\DohInterfaceSettings"
            if (!(Test-Path $ifPath)) {{
                New-Item -Path $ifPath -Force | Out-Null
            }}
            
            # 2. Настройки DoH для сервера
            $serverPath = "$ifPath\\Doh\\$server"
            if (!(Test-Path $serverPath)) {{
                New-Item -Path $serverPath -Force | Out-Null
            }}
            
            # Устанавливаем флаг для ручного шаблона (значение 1 = только ручной шаблон)
            New-ItemProperty -Path $serverPath -Name "DohFlags" -Value 1 -PropertyType DWORD -Force | Out-Null
            
            # 3. Глобальные настройки DoH
            $globalPath = "$regBase\\Parameters"
            Set-ItemProperty -Path $globalPath -Name "EnableAutoDoh" -Value 2 -Type DWORD -Force | Out-Null
            
            # 4. Указываем шаблон URL
            $templatePath = "$regBase\\Parameters\\DohInterfaceSettings"
            if (!(Test-Path $templatePath)) {{
                New-Item -Path $templatePath -Force | Out-Null
            }}
            New-ItemProperty -Path $templatePath -Name "$server" -Value "{doh_template}" -PropertyType String -Force | Out-Null
            
            Write-Output "DoH: Включено (ручной шаблон)"
        }}
        '''
        code, out_doh, err_doh = run_powershell_command(set_doh_cmd)
        
        if "Включено" in out_doh:
            print(f"     {Fore.GREEN}[✓] {out_doh}{Style.RESET_ALL}")
        else:
            print(f"     {Fore.YELLOW}[!] {out_doh if out_doh else 'DoH параметры установлены'}{Style.RESET_ALL}")
    
    # 5. Очистка кэша и обновление DHCP
    print(f"\n{Fore.CYAN}[4]{Style.RESET_ALL} Очистка кэша и обновление DHCP...")
    
    # Очистка DNS кэша
    flush_cmd = "Clear-DnsClientCache; ipconfig /flushdns"
    code, out, err = run_powershell_command(flush_cmd)
    print(f"   {Fore.GREEN}[✓] DNS кэш очищен{Style.RESET_ALL}")
    
    # Обновление DHCP для активных адаптеров
    renew_cmd = '''
    Get-NetAdapter -Physical | Where-Object { $_.Status -eq 'Up' } | ForEach-Object {
        $adapterName = $_.Name
        # Выпускаем и обновляем IP
        ipconfig /release "$adapterName" 2>$null
        Start-Sleep -Milliseconds 500
        ipconfig /renew "$adapterName" 2>$null
        Write-Output "$adapterName: IP обновлен"
    }
    '''
    code, out, err = run_powershell_command(renew_cmd)
    if out:
        for line in out.split('\n'):
            if line:
                print(f"   {Fore.GREEN}[✓] {line}{Style.RESET_ALL}")
    
    # 6. Перезапуск службы DNS
    print(f"\n{Fore.CYAN}[5]{Style.RESET_ALL} Перезапуск DNS службы...")
    restart_cmd = '''
    Restart-Service -Name Dnscache -Force -ErrorAction SilentlyContinue
    if ($?) { Write-Output "Служба DNS перезапущена" }
    else { Write-Output "Служба DNS не перезапущена (уже работает)" }
    '''
    code, out, err = run_powershell_command(restart_cmd)
    print(f"   {Fore.GREEN}[✓] {out}{Style.RESET_ALL}")
    
    # Итог
    print(f"\n{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] СБРОС WINDOWS 10 ЗАВЕРШЕН{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}Результат:{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}• DNS серверы: {Fore.GREEN}Автоматически (DHCP){Style.RESET_ALL}")
    print(f"   {Fore.WHITE}• DoH шифрование: {Fore.YELLOW}Включено (ручной шаблон){Style.RESET_ALL}")
    print(f"   {Fore.WHITE}• Шаблон URL: {Fore.CYAN}{doh_template}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}• Обработано адаптеров: {reset_count}/{len(adapters)}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}[!] Для проверки откройте: ncpa.cpl → Свойства → IPv4{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}[Нажмите Enter для возврата в меню...]{Style.RESET_ALL}")

def main():
    if not is_admin():
        print_banner()
        print(f"{Fore.YELLOW}[!] Требуются права администратора...{Style.RESET_ALL}")
        time.sleep(2)
        elevate()
    
    print_banner()
    reset_windows10_dhcp()

if __name__ == "__main__":
    main()