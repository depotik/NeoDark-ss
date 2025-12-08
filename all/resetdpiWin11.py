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
    print_center('\033[95m║   DNS RESET TOOL - Сброс настроек к DHCP             ║\033[0m')
    print_center('\033[95m║   Target: Windows 11 | DoH: Manual Template         ║\033[0m')
    print_center('\033[95m╚═══════════════════════════════════════════════════════╝\033[0m')
    print()

def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], 
                               capture_output=True, text=True, encoding='cp866')
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def reset_to_dhcp():
    print("\033[36m[*] Сброс настроек DNS к DHCP...\033[0m")
    print("\033[97m[!] DoH шаблон останется включенным\033[0m")
    
    doh_template = "https://xbox-dns.ru/dns-query"
    doh_server = "176.99.11.77"
    
    # 1. Убедимся, что DoH шаблон зарегистрирован
    print("\n\033[36m[1]\033[0m Регистрация DoH шаблона...")
    register_doh_cmd = f'''
    $server = "{doh_server}"
    $template = "{doh_template}"
    # Проверяем, зарегистрирован ли уже
    $existing = Get-DnsClientDohServerAddress | Where-Object {{ $_.ServerAddress -eq $server }}
    if (-not $existing) {{
        Add-DnsClientDohServerAddress -ServerAddress $server -DohTemplate $template -AllowFallbackToUdp $false -AutoUpgrade $false
        Write-Output "DoH шаблон зарегистрирован"
    }} else {{
        Write-Output "DoH шаблон уже зарегистрирован"
    }}
    '''
    code, out, err = run_powershell_command(register_doh_cmd)
    print(f"   \033[92m[✓] {out}\033[0m")
    
    # 2. Получение всех адаптеров
    print("\n\033[36m[2]\033[0m Поиск сетевых адаптеров...")
    get_adapters_cmd = '''
    Get-NetAdapter -Physical | ForEach-Object {
        Write-Output "$($_.Name)|$($_.Status)"
    }
    '''
    code, out, err = run_powershell_command(get_adapters_cmd)
    
    if not out:
        print("   \033[93m[!] Адаптеры не найдены\033[0m")
        return
    
    adapters = [line.split('|') for line in out.split('\n') if line]
    print(f"   \033[92m[+] Найдено адаптеров: {len(adapters)}\033[0m")
    
    # 3. Сброс DNS к DHCP для каждого адаптера
    print("\n\033[36m[3]\033[0m Сброс DNS настроек к DHCP...")
    
    for adapter_info in adapters:
        if len(adapter_info) != 2:
            continue
            
        adapter_name, adapter_status = adapter_info
        adapter_name = adapter_name.strip()
        
        # Индикатор статуса
        status_icon = "\033[92m●\033[0m" if adapter_status == "Up" else "\033[90m●\033[0m"
        print(f"   {status_icon} \033[97m{adapter_name}:\033[0m", end=" ")
        
        # Сброс DNS серверов (возврат к DHCP)
        reset_cmd = f'''
        $adapterName = "{adapter_name}"
        # Удаляем статические DNS серверы
        Remove-DnsClientServerAddress -InterfaceAlias $adapterName -Confirm:$false -ErrorAction SilentlyContinue
        # Проверяем, что DNS теперь автоматические
        $current = Get-DnsClientServerAddress -InterfaceAlias $adapterName -AddressFamily IPv4 -ErrorAction SilentlyContinue
        if ($current.ServerAddresses.Count -eq 0) {{
            Write-Output "DNS: Автоматически (DHCP)"
        }} else {{
            # Если остались серверы, устанавливаем пустой список для принудительного DHCP
            Set-DnsClientServerAddress -InterfaceAlias $adapterName -ResetServerAddresses -ErrorAction SilentlyContinue
            Write-Output "DNS: Сброшено к DHCP"
        }}
        '''
        code, out_reset, err_reset = run_powershell_command(reset_cmd)
        print(f"\033[92m{out_reset}\033[0m")
        
        # 4. Настройка DoH в реестре для ручного шаблона
        print(f"     \033[97mНастройка DoH шаблона...\033[0m")
        set_doh_cmd = f'''
        $adapterName = "{adapter_name}"
        $server = "{doh_server}"
        $adapter = Get-NetAdapter -Name $adapterName -ErrorAction SilentlyContinue
        if ($adapter) {{
            $ifGuid = $adapter.InterfaceGuid
            
            # Убедимся, что путь существует
            $regPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\InterfaceSpecificParameters\\$ifGuid\\DohInterfaceSettings"
            if (!(Test-Path $regPath)) {{
                New-Item -Path $regPath -Force | Out-Null
            }}
            
            # Настройка DoH для указанного сервера
            $dohServerPath = "$regPath\\Doh\\$server"
            if (!(Test-Path $dohServerPath)) {{
                New-Item -Path $dohServerPath -Force | Out-Null
            }}
            
            # Устанавливаем флаг для ручного шаблона
            New-ItemProperty -Path $dohServerPath -Name "DohFlags" -Value 1 -PropertyType QWORD -Force | Out-Null
            
            # Дополнительно: настраиваем, чтобы Windows знала о ручном шаблоне
            $settingsPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters\\DohInterfaceSettings"
            if (!(Test-Path $settingsPath)) {{
                New-Item -Path $settingsPath -Force | Out-Null
            }}
            New-ItemProperty -Path $settingsPath -Name "DohFlags" -Value 1 -PropertyType DWORD -Force | Out-Null
            
            Write-Output "DoH: Включено (ручной шаблон)"
        }}
        '''
        code, out_doh, err_doh = run_powershell_command(set_doh_cmd)
        print(f"     \033[92m[✓] {out_doh if out_doh else 'DoH настроен'}\033[0m")
    
    # 5. Очистка кэша
    print("\n\033[36m[4]\033[0m Очистка DNS кэша...")
    flush_cmd = "Clear-DnsClientCache"
    code, out, err = run_powershell_command(flush_cmd)
    print(f"   \033[92m[✓] DNS кэш очищен\033[0m")
    
    # 6. Обновление DHCP для активных адаптеров
    print("\n\033[36m[5]\033[0m Обновление DHCP...")
    renew_cmd = '''
    Get-NetAdapter -Physical | Where-Object { $_.Status -eq 'Up' } | ForEach-Object {
        $adapterName = $_.Name
        # Освобождаем и обновляем IP
        ipconfig /release "$adapterName" 2>$null
        ipconfig /renew "$adapterName" 2>$null
        Write-Output "$adapterName: DHCP обновлен"
    }
    '''
    code, out, err = run_powershell_command(renew_cmd)
    if out:
        for line in out.split('\n'):
            if line:
                print(f"   \033[92m[✓] {line}\033[0m")
    
    # Итог
    print("\n\033[92m" + "═" * 60 + "\033[0m")
    print("\033[92m[✓] Сброс настроек завершен!\033[0m")
    print("\n\033[97mРезультат:\033[0m")
    print("   \033[97mDNS серверы: \033[92mАвтоматически (DHCP)\033[0m")
    print("   \033[97mDoH шаблон:  \033[92mВключено (ручной шаблон)\033[0m")
    print(f"   \033[97mШаблон URL:  \033[96m{doh_template}\033[0m")
    print("\033[93m\n[!] Откройте настройки сети для проверки\033[0m")
    print("\033[92m" + "═" * 60 + "\033[0m")
    input("\n\033[36m[Нажмите Enter для выхода...]\033[0m")

def main():
    if not is_admin():
        print_banner()
        print("\033[93m[!] Запрос прав администратора...\033[0m")
        time.sleep(1)
        elevate()
    
    print_banner()
    reset_to_dhcp()

if __name__ == "__main__":
    main()