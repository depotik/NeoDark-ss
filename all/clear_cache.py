import os
import shutil
import tempfile
import platform
import sys
from pathlib import Path

def clear_temp_dirs():
    """
    Очищает папки временных файлов для освобождения места на диске.
    """
    system = platform.system()
    deleted_files = 0
    deleted_dirs = 0
    freed_space = 0
    
    print("🔍 Начинаем очистку временных файлов...")
    
    # Список путей для очистки в зависимости от ОС
    temp_paths = []
    
    if system == "Windows":
        temp_paths.extend([
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            r'C:\Windows\Temp',
        ])
        
        # Добавляем пути к пользовательским временными файлами
        user_profile = os.environ.get('USERPROFILE', '')
        if user_profile:
            temp_paths.append(os.path.join(user_profile, 'AppData', 'Local', 'Temp'))
            
    elif system in ["Linux", "Darwin"]:  # Linux или macOS
        temp_paths.extend([
            '/tmp',
            '/var/tmp',
        ])
        
        # Для macOS также добавляем специфические пути
        if system == "Darwin":
            home = os.environ.get('HOME', '')
            if home:
                temp_paths.append(os.path.join(home, 'Library', 'Caches'))
    
    # Уникальные и существующие пути
    unique_paths = set()
    for path in temp_paths:
        if path and os.path.exists(path):
            unique_paths.add(path)
    
    # Очистка каждого пути
    for temp_path in unique_paths:
        print(f"⏳ Очистка: {temp_path}")
        try:
            # Пробегаем по всем файлам и папкам в директории
            for item in Path(temp_path).iterdir():
                try:
                    # Пропускаем системные файлы, которые нельзя удалять
                    if system == "Windows" and item.name in ['.', '..']:
                        continue
                    
                    if item.is_file():
                        # Получаем размер файла перед удалением
                        size = item.stat().st_size
                        item.unlink()
                        deleted_files += 1
                        freed_space += size
                        print(f"  ✅ Удалён файл: {item.name}")
                        
                    elif item.is_dir():
                        # Рекурсивно удаляем папку
                        size = sum(f.stat().st_size for f in item.glob('**/*') if f.is_file())
                        shutil.rmtree(item)
                        deleted_dirs += 1
                        freed_space += size
                        print(f"  📁 Удалена папка: {item.name}")
                        
                except (PermissionError, OSError) as e:
                    # Пропускаем файлы, которые не можем удалить
                    print(f"  ⚠️  Пропущен: {item.name} (Нет доступа)")
                    continue
                    
        except Exception as e:
            print(f"❌ Ошибка при очистке {temp_path}: {str(e)}")
            continue
    
    # Форматируем освобожденное место в человекочитаемый формат
    def format_bytes(bytes_count):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.2f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.2f} PB"
    
    print("\n✅ Очистка временных файлов завершена!")
    print(f"📊 Статистика:")
    print(f"   🗑️  Удалено файлов: {deleted_files}")
    print(f"   📁 Удалено папок: {deleted_dirs}")
    print(f"   💾 Освобождено: {format_bytes(freed_space)}")

def clear_application_cache():
    """
    Очищает кэш приложений и браузеров.
    """
    print("\n🔍 Очистка кэша приложений...")
    
    system = platform.system()
    cleared_apps = 0
    
    if system == "Windows":
        # Очистка кэша популярных браузеров на Windows
        user_profile = os.environ.get('USERPROFILE', '')
        appdata = os.environ.get('APPDATA', '')
        localappdata = os.environ.get('LOCALAPPDATA', '')
        
        browser_cache_paths = [
            # Chrome
            os.path.join(localappdata, 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(localappdata, 'Google', 'Chrome', 'User Data', 'Default', 'GPUCache'),
            
            # Firefox
            os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles'),
            
            # Edge
            os.path.join(localappdata, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(localappdata, 'Microsoft', 'Edge', 'User Data', 'Default', 'GPUCache'),
            
            # Opera
            os.path.join(appdata, 'Opera Software', 'Opera Stable', 'Cache'),
        ]
        
        for cache_path in browser_cache_paths:
            if os.path.exists(cache_path):
                try:
                    if os.path.isfile(cache_path):
                        size = os.path.getsize(cache_path)
                        os.remove(cache_path)
                        print(f"  ✅ Очищен кэш: {cache_path}")
                        cleared_apps += 1
                    elif os.path.isdir(cache_path):
                        # Подсчитываем размер перед удалением
                        size = sum(f.stat().st_size for f in Path(cache_path).glob('**/*') if f.is_file())
                        shutil.rmtree(cache_path)
                        print(f"  ✅ Очищен кэш: {cache_path}")
                        cleared_apps += 1
                except (PermissionError, OSError) as e:
                    print(f"  ⚠️  Не удалось очистить: {cache_path}")
                    
    elif system == "Darwin":  # macOS
        home = os.environ.get('HOME', '')
        if home:
            browser_cache_paths = [
                # Safari
                os.path.join(home, 'Library', 'Caches', 'com.apple.Safari'),
                
                # Chrome
                os.path.join(home, 'Library', 'Caches', 'Google', 'Chrome'),
                
                # Firefox
                os.path.join(home, 'Library', 'Caches', 'Firefox'),
            ]
            
            for cache_path in browser_cache_paths:
                if os.path.exists(cache_path):
                    try:
                        shutil.rmtree(cache_path)
                        print(f"  ✅ Очищен кэш: {cache_path}")
                        cleared_apps += 1
                    except (PermissionError, OSError) as e:
                        print(f"  ⚠️  Не удалось очистить: {cache_path}")
                        
    print(f"📊 Кэш {cleared_apps} приложений успешно очищен!")

def main():
    print("🔥 Утилита очистки кэша NeoDark")
    print("=" * 40)
    
    try:
        clear_temp_dirs()
        clear_application_cache()
        
        print("\n🎉 Полная очистка завершена!")
        print("Система теперь работает быстрее и имеет больше свободного места.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Очистка была прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка во время очистки: {str(e)}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()