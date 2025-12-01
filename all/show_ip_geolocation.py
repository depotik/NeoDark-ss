import os
import sys
import platform
import json
import time
import socket
from datetime import datetime
import urllib.request
import urllib.parse

def print_header():
    """Выводит заголовок программы"""
    print("🌐 Отображение IP-адреса и геолокации NeoDark")
    print("=" * 60)

def get_external_ip():
    """Получает внешний IP-адрес"""
    print("🔍 Получение внешнего IP-адреса...")
    
    ip_services = [
        'https://api.ipify.org',
        'https://icanhazip.com',
        'https://ident.me',
        'https://ipecho.net/plain',
        'https://myexternalip.com/raw'
    ]
    
    for service in ip_services:
        try:
            with urllib.request.urlopen(service, timeout=5) as response:
                if response.getcode() == 200:
                    ip = response.read().decode('utf-8').strip()
                    print(f"✅ Внешний IP: {ip}")
                    return ip
        except Exception as e:
            print(f"   ⚠️  Ошибка при использовании {service}: {str(e)[:50]}...")
            continue
    
    print("❌ Не удалось получить внешний IP-адрес")
    return None

def get_internal_ip():
    """Получает внутренний IP-адрес"""
    try:
        # Создаем временный сокет для определения локального IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Подключаемся к произвольному адресу (не отправляя данные)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        print(f"✅ Внутренний IP: {local_ip}")
        return local_ip
    except Exception as e:
        print(f"❌ Ошибка получения внутреннего IP: {e}")
        return None

def get_geolocation_info(ip):
    """Получает геолокационную информацию по IP"""
    print("🔍 Получение геолокационной информации...")
    
    try:
        # Используем бесплатный сервис ip-api.com
        url = f"http://ip-api.com/json/{ip}"
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'NeoDark IP Geolocation Tool')
        
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                if data.get('status') == 'success':
                    print("✅ Геолокация получена")
                    return data
                else:
                    print(f"❌ Ошибка получения геолокации: {data.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"❌ Ошибка HTTP: {response.getcode()}")
                return None
    except Exception as e:
        print(f"❌ Ошибка получения геолокации: {e}")
        return None

def display_ip_info(external_ip, internal_ip):
    """Отображает информацию об IP-адресах"""
    print("\n📋 Информация об IP-адресах:")
    print("-" * 40)
    
    if external_ip:
        print(f"🌐 Внешний IP: {external_ip}")
    else:
        print("🌐 Внешний IP: Не удалось получить")
    
    if internal_ip:
        print(f"🏠 Внутренний IP: {internal_ip}")
    else:
        print("🏠 Внутренний IP: Не удалось получить")
    
    print()

def display_geolocation_info(geo_info):
    """Отображает геолокационную информацию"""
    if not geo_info:
        print("❌ Геолокационная информация недоступна")
        return
    
    print("📍 Геолокационная информация:")
    print("-" * 40)
    
    # Основная информация
    print(f"🌍 Страна: {geo_info.get('country', 'N/A')}")
    if geo_info.get('countryCode'):
        print(f"   Код страны: {geo_info.get('countryCode')}")
    
    print(f"🏙️  Регион: {geo_info.get('regionName', 'N/A')}")
    if geo_info.get('region'):
        print(f"   Код региона: {geo_info.get('region')}")
    
    print(f"🏘️  Город: {geo_info.get('city', 'N/A')}")
    print(f"📮 Почтовый индекс: {geo_info.get('zip', 'N/A')}")
    
    # Координаты
    lat = geo_info.get('lat', 'N/A')
    lon = geo_info.get('lon', 'N/A')
    if lat != 'N/A' and lon != 'N/A':
        print(f"🧭 Координаты: {lat}, {lon}")
    
    # Сетевая информация
    print(f"📡 Провайдер: {geo_info.get('isp', 'N/A')}")
    print(f"🏢 Организация: {geo_info.get('org', 'N/A')}")
    print(f"🔢 ASN: {geo_info.get('as', 'N/A')}")
    
    # Дополнительная информация
    print(f"🕐 Часовой пояс: {geo_info.get('timezone', 'N/A')}")
    print(f"💱 Валюта: {geo_info.get('currency', 'N/A')}")
    print(f"📞 Код телефона: {geo_info.get('mobile', 'N/A')}")
    
    print()

def display_network_info():
    """Отображает информацию о сетевых интерфейсах"""
    print("🔌 Сетевые интерфейсы:")
    print("-" * 40)
    
    try:
        hostname = socket.gethostname()
        print(f"🖥️  Имя хоста: {hostname}")
        
        local_ips = socket.gethostbyname_ex(hostname)[2]
        print("🌐 Локальные IP-адреса:")
        for ip in local_ips:
            if not ip.startswith("127."):
                print(f"   • {ip}")
        
        print()
    except Exception as e:
        print(f"❌ Ошибка получения информации о сетевых интерфейсах: {e}")
        print()

def display_map_link(lat, lon):
    """Отображает ссылку на карту"""
    if lat != 'N/A' and lon != 'N/A':
        print("🗺️  Ссылки на карты:")
        print("-" * 40)
        print(f"   Google Maps: https://www.google.com/maps?q={lat},{lon}")
        print(f"   OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}")
        print()

def show_privacy_notice():
    """Показывает уведомление о конфиденциальности"""
    print("🔒 Уведомление о конфиденциальности:")
    print("-" * 40)
    print("   При использовании этой функции ваш IP-адрес передается")
    print("   сторонним сервисам (ip-api.com) для получения геолокационной")
    print("   информации. Убедитесь, что вы согласны с их политикой")
    print("   конфиденциальности перед использованием.")
    print()

def main():
    """Главная функция отображения IP и геолокации"""
    print_header()
    
    try:
        # Получаем IP-адреса
        external_ip = get_external_ip()
        internal_ip = get_internal_ip()
        
        # Отображаем информацию об IP
        display_ip_info(external_ip, internal_ip)
        
        # Получаем и отображаем геолокационную информацию
        if external_ip:
            geo_info = get_geolocation_info(external_ip)
            display_geolocation_info(geo_info)
            
            # Отображаем ссылку на карту
            if geo_info:
                display_map_link(geo_info.get('lat', 'N/A'), geo_info.get('lon', 'N/A'))
        else:
            print("❌ Невозможно получить геолокацию без внешнего IP-адреса")
            print()
        
        # Отображаем информацию о сетевых интерфейсах
        display_network_info()
        
        # Показываем уведомление о конфиденциальности
        show_privacy_notice()
        
        print(f"✅ Получение информации завершено!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Операция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()