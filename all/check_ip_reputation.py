import os
import sys
import platform
import json
import time
import ipaddress
from datetime import datetime
import urllib.request
import urllib.parse
import socket

def print_header():
    """Выводит заголовок программы"""
    print("🛡️  Проверка репутации IP-адреса NeoDark")
    print("=" * 55)

def get_target_ip():
    """Получает IP-адрес для проверки"""
    print("Выберите действие:")
    print(" [1] Проверить мой внешний IP")
    print(" [2] Проверить указанный IP")
    print()
    
    choice = input("Выберите опцию (1-2): ").strip()
    
    if choice == "1":
        try:
            # Получаем внешний IP
            print("🔍 Получение внешнего IP-адреса...")
            with urllib.request.urlopen('https://api.ipify.org') as response:
                external_ip = response.read().decode('utf-8')
            print(f"✅ Ваш внешний IP: {external_ip}")
            return external_ip
        except Exception as e:
            print(f"❌ Ошибка получения внешнего IP: {e}")
            return None
    elif choice == "2":
        ip = input("Введите IP-адрес для проверки: ").strip()
        try:
            # Проверяем валидность IP
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            print("❌ Неверный формат IP-адреса")
            return None
    else:
        print("❌ Неверный выбор")
        return None

def check_ip_reputation_virustotal(ip, api_key=None):
    """Проверяет репутацию IP через VirusTotal API"""
    print("🔍 Проверка репутации через VirusTotal...")
    
    if not api_key:
        print("   ⚠️  API-ключ VirusTotal не предоставлен")
        print("   Для получения полной информации зарегистрируйтесь на virustotal.com")
        print("   и получите бесплатный API-ключ")
        return None
    
    try:
        # Формируем URL для запроса
        url = f"https://www.virustotal.com/vtapi/v2/ip-address/report"
        params = {
            'apikey': api_key,
            'ip': ip
        }
        
        # Кодируем параметры
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        # Выполняем запрос
        request = urllib.request.Request(full_url)
        response = urllib.request.urlopen(request)
        
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            return data
        else:
            print(f"   ❌ Ошибка API: {response.getcode()}")
            return None
            
    except Exception as e:
        print(f"   ❌ Ошибка при проверке через VirusTotal: {e}")
        return None

def check_ip_reputation_abuseipdb(ip, api_key=None):
    """Проверяет репутацию IP через AbuseIPDB"""
    print("🔍 Проверка репутации через AbuseIPDB...")
    
    if not api_key:
        print("   ⚠️  API-ключ AbuseIPDB не предоставлен")
        print("   Для получения полной информации зарегистрируйтесь на abuseipdb.com")
        print("   и получите бесплатный API-ключ")
        return None
    
    try:
        # Формируем URL для запроса
        url = "https://api.abuseipdb.com/api/v2/check"
        params = {
            'ipAddress': ip,
            'maxAgeInDays': 90
        }
        
        # Кодируем параметры
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        
        # Выполняем запрос
        request = urllib.request.Request(full_url)
        request.add_header('Key', api_key)
        request.add_header('Accept', 'application/json')
        
        response = urllib.request.urlopen(request)
        
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            return data
        else:
            print(f"   ❌ Ошибка API: {response.getcode()}")
            return None
            
    except Exception as e:
        print(f"   ❌ Ошибка при проверке через AbuseIPDB: {e}")
        return None

def check_ip_basic_info(ip):
    """Получает базовую информацию об IP"""
    print("🔍 Получение базовой информации об IP...")
    
    try:
        # Получаем информацию через ip-api.com (бесплатный сервис)
        url = f"http://ip-api.com/json/{ip}"
        response = urllib.request.urlopen(url)
        
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            return data
        else:
            print(f"   ❌ Ошибка получения информации: {response.getcode()}")
            return None
            
    except Exception as e:
        print(f"   ❌ Ошибка при получении информации: {e}")
        return None

def display_basic_info(info):
    """Отображает базовую информацию об IP"""
    if not info:
        return
    
    print("\n📍 Базовая информация:")
    print(f"   IP: {info.get('query', 'N/A')}")
    print(f"   Страна: {info.get('country', 'N/A')}")
    print(f"   Регион: {info.get('regionName', 'N/A')}")
    print(f"   Город: {info.get('city', 'N/A')}")
    print(f"   Провайдер: {info.get('isp', 'N/A')}")
    print(f"   Организация: {info.get('org', 'N/A')}")
    print(f"   ASN: {info.get('as', 'N/A')}")
    print(f"   Координаты: {info.get('lat', 'N/A')}, {info.get('lon', 'N/A')}")
    print(f"   Часовой пояс: {info.get('timezone', 'N/A')}")
    print()

def display_virustotal_info(info):
    """Отображает информацию от VirusTotal"""
    if not info:
        return
    
    print("🛡️  Репутация VirusTotal:")
    
    response_code = info.get('response_code', 0)
    if response_code == 0:
        print("   ⚠️  IP не найден в базе VirusTotal")
        return
    
    detected_urls = info.get('detected_urls', [])
    resolutions = info.get('resolutions', [])
    
    print(f"   🔍 Обнаружено вредоносных URL: {len(detected_urls)}")
    
    if resolutions:
        print(f"   🌐 Доменов связано: {len(resolutions)}")
        # Показываем последние 3 записи
        for resolution in resolutions[:3]:
            print(f"     • {resolution.get('hostname', 'N/A')} ({resolution.get('last_resolved', 'N/A')})")
        if len(resolutions) > 3:
            print(f"     ... и еще {len(resolutions) - 3}")
    
    print()

def display_abuseipdb_info(info):
    """Отображает информацию от AbuseIPDB"""
    if not info:
        return
    
    print("🛡️  Репутация AbuseIPDB:")
    
    data = info.get('data', {})
    
    ip_address = data.get('ipAddress', 'N/A')
    is_public = data.get('isPublic', 'N/A')
    ip_version = data.get('ipVersion', 'N/A')
    is_whitelisted = data.get('isWhitelisted', None)
    abuse_confidence_score = data.get('abuseConfidenceScore', 0)
    country_code = data.get('countryCode', 'N/A')
    usage_type = data.get('usageType', 'N/A')
    isp = data.get('isp', 'N/A')
    domain = data.get('domain', 'N/A')
    hostnames = data.get('hostnames', [])
    total_reports = data.get('totalReports', 0)
    last_reported_at = data.get('lastReportedAt', 'Никогда')
    
    print(f"   IP: {ip_address}")
    print(f"   Версия: IPv{ip_version}")
    print(f"   Публичный: {'Да' if is_public else 'Нет'}")
    
    if is_whitelisted is not None:
        print(f"   В белом списке: {'Да' if is_whitelisted else 'Нет'}")
    
    # Оценка уровня угрозы
    if abuse_confidence_score >= 70:
        threat_level = "🔴 Высокий"
    elif abuse_confidence_score >= 30:
        threat_level = "🟡 Средний"
    else:
        threat_level = "🟢 Низкий"
    
    print(f"   Уровень угрозы: {threat_level} ({abuse_confidence_score}%)")
    print(f"   Страна: {country_code}")
    print(f"   Тип использования: {usage_type}")
    print(f"   Провайдер: {isp}")
    print(f"   Домен: {domain}")
    
    if hostnames:
        print(f"   Хосты: {', '.join(hostnames)}")
    
    print(f"   Всего отчетов: {total_reports}")
    print(f"   Последний отчет: {last_reported_at}")
    print()

def show_security_recommendations(ip, basic_info, abuse_info):
    """Показывает рекомендации по безопасности"""
    print("💡 Рекомендации по безопасности:")
    
    # Проверяем уровень угрозы
    threat_level = "низкий"
    if abuse_info and 'data' in abuse_info:
        score = abuse_info['data'].get('abuseConfidenceScore', 0)
        if score >= 70:
            threat_level = "высокий"
        elif score >= 30:
            threat_level = "средний"
    
    if threat_level == "высокий":
        print("   🔴 Высокий уровень угрозы!")
        print("   Рекомендуется:")
        print("   • Блокировать этот IP в брандмауэре")
        print("   • Проверить логи на предмет подозрительной активности")
        print("   • Сообщить в соответствующие службы")
    elif threat_level == "средний":
        print("   🟡 Средний уровень угрозы")
        print("   Рекомендуется:")
        print("   • Мониторить активность с этого IP")
        print("   • Проверить правила брандмауэра")
    else:
        print("   🟢 Низкий уровень угрозы")
        print("   IP выглядит безопасным")
    
    # Проверяем тип использования
    if basic_info and basic_info.get('proxy') == 'yes':
        print("   ⚠️  IP используется как прокси")
    elif basic_info and basic_info.get('hosting') == 'yes':
        print("   ⚠️  IP принадлежит хостинг-провайдеру")
    
    print()

def show_api_notice():
    """Показывает уведомление об API ключах"""
    print("ℹ️  Для получения полной информации:")
    print("   • VirusTotal: зарегистрируйтесь на virustotal.com")
    print("   • AbuseIPDB: зарегистрируйтесь на abuseipdb.com")
    print("   Оба сервиса предоставляют бесплатные API-ключи")
    print()

def main():
    """Главная функция проверки репутации IP"""
    print_header()
    
    try:
        # Получаем IP для проверки
        target_ip = get_target_ip()
        if not target_ip:
            input("\nНажмите Enter для выхода...")
            return
        
        print(f"\n🔍 Начинаем проверку IP: {target_ip}")
        print("=" * 55)
        
        # Получаем базовую информацию
        basic_info = check_ip_basic_info(target_ip)
        display_basic_info(basic_info)
        
        # Проверяем через AbuseIPDB (если есть API ключ)
        # В демо-версии просто показываем, что проверка возможна
        print("🔍 Для проверки через AbuseIPDB требуется API-ключ")
        abuse_info = None
        
        # Проверяем через VirusTotal (если есть API ключ)
        print("🔍 Для проверки через VirusTotal требуется API-ключ")
        virustotal_info = None
        
        # Показываем рекомендации
        show_security_recommendations(target_ip, basic_info, abuse_info)
        
        # Показываем уведомление об API
        show_api_notice()
        
        print(f"✅ Проверка завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Проверка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()