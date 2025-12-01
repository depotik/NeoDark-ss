import os
import sys
import platform
import random
from datetime import datetime, timedelta

def print_header():
    """Выводит заголовок программы"""
    print("🔍 Проверка активности сессий")
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

def get_current_sessions():
    """Получает список текущих сессий (демо)"""
    print("🔄 Получение списка сессий...")
    
    # Генерируем демонстрационные данные
    sessions = []
    
    # Текущая сессия
    current_time = datetime.now()
    sessions.append({
        "id": "sess_" + ''.join(random.choices("0123456789abcdef", k=8)),
        "user": os.getlogin() if hasattr(os, 'getlogin') else "current_user",
        "type": "local",
        "status": "active",
        "login_time": current_time - timedelta(hours=2, minutes=30),
        "last_activity": current_time - timedelta(minutes=5),
        "ip": "127.0.0.1",
        "location": "Local Machine"
    })
    
    # Другие сессии
    session_types = ["remote", "ssh", "web", "mobile"]
    session_users = ["admin", "guest", "user1", "user2", "developer"]
    locations = ["Office Network", "Home Network", "VPN Connection", "Mobile Network"]
    
    for i in range(random.randint(2, 5)):
        sessions.append({
            "id": "sess_" + ''.join(random.choices("0123456789abcdef", k=8)),
            "user": random.choice(session_users),
            "type": random.choice(session_types),
            "status": random.choice(["active", "idle", "disconnected"]),
            "login_time": current_time - timedelta(hours=random.randint(1, 24)),
            "last_activity": current_time - timedelta(minutes=random.randint(1, 120)),
            "ip": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "location": random.choice(locations)
        })
    
    return sessions

def display_sessions(sessions):
    """Отображает список сессий"""
    print("\n📋 Активные сессии:")
    print("-" * 60)
    
    status_icons = {
        "active": "🟢",
        "idle": "🟡",
        "disconnected": "🔴"
    }
    
    type_icons = {
        "local": "🖥️",
        "remote": "🌐",
        "ssh": "🔌",
        "web": "🕸️",
        "mobile": "📱"
    }
    
    for i, session in enumerate(sessions, 1):
        icon = status_icons.get(session['status'], "⚪")
        type_icon = type_icons.get(session['type'], "❓")
        
        print(f"   {i}. {icon} {type_icon} {session['user']} ({session['type']})")
        print(f"      ID: {session['id']}")
        print(f"      IP: {session['ip']} ({session['location']})")
        print(f"      Вход: {session['login_time'].strftime('%Y-%m-%d %H:%M')}")
        print(f"      Активность: {session['last_activity'].strftime('%Y-%m-%d %H:%M')}")
        print(f"      Статус: {session['status']}")
        print()

def show_session_statistics(sessions):
    """Показывает статистику сессий"""
    print("📊 Статистика сессий:")
    print("-" * 25)
    
    total_sessions = len(sessions)
    active_sessions = len([s for s in sessions if s['status'] == 'active'])
    idle_sessions = len([s for s in sessions if s['status'] == 'idle'])
    disconnected_sessions = len([s for s in sessions if s['status'] == 'disconnected'])
    
    print(f"   Всего сессий: {total_sessions}")
    print(f"   Активных: {active_sessions}")
    print(f"   Неактивных: {idle_sessions}")
    print(f"   Отключенных: {disconnected_sessions}")
    
    # Среднее время сессии
    current_time = datetime.now()
    total_duration = sum([(current_time - s['login_time']).total_seconds() for s in sessions])
    avg_duration = total_duration / len(sessions) if sessions else 0
    
    hours = int(avg_duration // 3600)
    minutes = int((avg_duration % 3600) // 60)
    print(f"   Средняя продолжительность: {hours}ч {minutes}м")

def show_session_actions():
    """Показывает возможные действия с сессиями"""
    print("\n⚙️ Действия с сессиями:")
    print("-" * 25)
    print("   [1] Завершить сессию")
    print("   [2] Отправить сообщение пользователю")
    print("   [3] Заблокировать пользователя")
    print("   [4] Продлить сессию")
    print("   [5] Экспорт списка сессий")

def main():
    """Главная функция проверки активности сессий"""
    # Очищаем экран
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Показываем логотип и заголовок
    show_neodark_logo()
    print_header()
    
    try:
        # Получаем список сессий
        sessions = get_current_sessions()
        
        # Отображаем сессии
        display_sessions(sessions)
        
        # Показываем статистику
        show_session_statistics(sessions)
        
        # Показываем возможные действия
        show_session_actions()
        
        print(f"\n✅ Проверка сессий завершена!")
        print(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Проверка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()