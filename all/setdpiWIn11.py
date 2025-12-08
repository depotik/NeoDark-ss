#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import ctypes
import time

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

def print_center(text):
    try:
        width = os.get_terminal_size().columns
    except:
        width = 120
    for line in text.split('\n'):
        print(line.center(width))

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = '''\033[36m
███╗   ██╗███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗  ██║   ██║██║  ██║███████║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝  ██║   ██║██║  ██║██╔══██║██╔══██╗██╔═██╗ 
██║ ╚████║███████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██╗
 ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝\033[0m'''
    
    print_center(banner)
    print_center('\033[93m NeoDark-CLI | Creator: @weeaave\033[0m')
    print_center('\033[90mSpecial for NeoDark Ecosystem | DNS Configuration Tool\033[0m')
    print()
    print_center('\033[95m╔═══════════════════════════════════════════════════════╗\033[0m')
    print_center('\033[95m║   DOH SETUP TOOL - Настройка DNS через HTTPS         ║\033[0m')
    print_center('\033[95m║   Target: Windows 11 | Mode: Manual Configuration   ║\033[0m')
    print_center('\033[95m╚═══════════════════════════════════════════════════════╝\033[0m')
    print()

def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], 
                               capture_output=True, text=True, encoding='cp866')
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def setup_doh():
    print("\033[36m[*] Настройка DNS через HTTPS (DoH)...\033[0m")
    
    dns_server_primary = "176.99.11.77"
    dns_server_secondary = "80.78.247.254"
    doh_template = "https://xbox-dns.ru/dns-query"
    
    print(f"\033[92m[+] DNS серверы: {dns_server_primary}, {dns_server_secondary}\033[0m")
    print(f"\033[92m[+] DoH шаблон: {doh_template}\033[0m")
    
    # 1. Регистрация DoH сервера
    print("\n\033[36m[1]\033[0m Регистрация DoH шаблона...")
    add_doh_cmd = f'''
    $server = "{dns_server_primary}"
    $template = "{doh_template}"
    Add-DnsClientDohServerAddress -ServerAddress $server -DohTemplate $template -AllowFallbackToUdp $false -AutoUpgrade $false -ErrorAction SilentlyContinue
    Write-Output "DoH шаблон зарегистрирован"
    '''
    code, out, err = run_powershell_command(add_doh_cmd)
    print(f"   \033[92m[✓] {out}\033[0m")
    
    # 2. Получение активных адаптеров
    print("\n\033[36m[2]\033[0m Поиск активных адаптеров...")
    get_adapters_cmd = '''
    Get-NetAdapter -Physical | Where-Object { $_.Status -eq 'Up' } | ForEach-Object {
        Write-Output $_.Name
    }
    '''
    code, out, err = run_powershell_command(get_adapters_cmd)
    
    if not out:
        print("   \033[93m[!] Активные адаптеры не найдены\033[0m")
    else:
        adapters = out.split('\n')
        print(f"   \033[92m[+] Найдено адаптеров: {len(adapters)}\033[0m")
        
        for adapter in adapters:
            adapter = adapter.strip()
            if not adapter:
                continue
                
            print(f"   \033[97m• Обработка адаптера: {adapter}\033[0m")
            
            # Установка DNS серверов
            set_dns_cmd = f'''
            $adapterName = "{adapter}"
            $dnsAddresses = "{dns_server_primary}", "{dns_server_secondary}"
            Set-DnsClientServerAddress -InterfaceAlias $adapterName -ServerAddresses $dnsAddresses -ErrorAction SilentlyContinue
            Write-Output "DNS серверы установлены"
            '''
            code, out_dns, err_dns = run_powershell_command(set_dns_cmd)
            print(f"     \033[92m[✓] {out_dns}\033[0m")
            
            # Настройка DoH в реестре
            enable_doh_cmd = f'''
            $adapterName = "{adapter}"
            $server = "{dns_server_primary}"
            $adapter = Get-NetAdapter -Name $adapterName -ErrorAction SilentlyContinue
            if ($adapter) {{
                $ifGuid = $adapter.InterfaceGuid
                $regPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\InterfaceSpecificParameters\\$ifGuid\\DohInterfaceSettings"
                
                # Создаем путь если не существует
                if (!(Test-Path $regPath)) {{
                    New-Item -Path $regPath -Force | Out-Null
                }}
                
                $dohPath = "$regPath\\Doh\\$server"
                if (!(Test-Path $dohPath)) {{
                    New-Item -Path $dohPath -Force | Out-Null
                }}
                
                New-ItemProperty -Path $dohPath -Name "DohFlags" -Value 1 -PropertyType QWORD -Force | Out-Null
                Write-Output "DoH настроен в реестре"
            }}
            '''
            code, out_doh, err_doh = run_powershell_command(enable_doh_cmd)
            print(f"     \033[92m[✓] {out_doh if out_doh else 'DoH настроен'}\033[0m")
    
    # 3. Очистка кэша
    print("\n\033[36m[3]\033[0m Очистка DNS кэша...")
    flush_cmd = "Clear-DnsClientCache"
    code, out, err = run_powershell_command(flush_cmd)
    print(f"   \033[92m[✓] DNS кэш очищен\033[0m")
    
    print("\n\033[92m" + "═" * 60 + "\033[0m")
    print("\033[92m[✓] Настройка завершена!\033[0m")
    print("\033[97mDNS серверы: \033[92mРучные\033[0m")
    print("\033[97mDoH шаблон: \033[92mВключен (ручной)\033[0m")
    print("\033[93m" + "═" * 60 + "\033[0m")
    input("\n\033[36m[Нажмите Enter для выхода...]\033[0m")

def main():
    if not is_admin():
        print_banner()
        print("\033[93m[!] Запрос прав администратора...\033[0m")
        time.sleep(1)
        elevate()
    
    print_banner()
    setup_doh()

if __name__ == "__main__":
    main()