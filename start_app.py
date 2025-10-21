#!/usr/bin/env python3
"""
Автоматический запуск Message Treaker
Запускает API сервер, открывает веб-интерфейс и проверяет готовность
"""

import subprocess
import time
import webbrowser
import requests
import sys
import os
from pathlib import Path

class MessageTreakerLauncher:
    def __init__(self):
        self.api_process = None
        self.api_url = "http://127.0.0.1:8000"
        self.web_file = Path(__file__).parent / "web" / "index.html"
        
    def check_dependencies(self):
        """Проверка зависимостей"""
        print("🔍 Проверка зависимостей...")
        
        # Проверяем виртуальное окружение
        if not os.path.exists("venv"):
            print("❌ Виртуальное окружение не найдено!")
            print("💡 Создайте виртуальное окружение: python3 -m venv venv")
            return False
            
        # Проверяем .env файл
        if not os.path.exists(".env"):
            print("❌ Файл .env не найден!")
            print("💡 Скопируйте env.example в .env и заполните API ключи")
            return False
            
        print("✅ Зависимости в порядке")
        return True
    
    def wait_for_api(self, timeout=30):
        """Ожидание готовности API"""
        print("⏳ Ожидание готовности API сервера...")
        
        for i in range(timeout):
            try:
                response = requests.get(f"{self.api_url}/health", timeout=2)
                if response.status_code == 200:
                    print("✅ API сервер готов!")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                print(f"⏳ Ждем... ({i}/{timeout}s)")
        
        print("❌ API сервер не отвечает в течение 30 секунд")
        return False
    
    def start_api_server(self):
        """Запуск API сервера"""
        print("🚀 Запуск API сервера...")
        
        try:
            # Активируем виртуальное окружение и запускаем API
            if sys.platform.startswith('win'):
                # Windows
                activate_script = "venv\\Scripts\\activate.bat"
                cmd = f"{activate_script} && python run_api.py"
            else:
                # Linux/macOS
                python_path = os.path.join("venv", "bin", "python")
                cmd = [python_path, "run_api.py"]
            
            self.api_process = subprocess.Popen(
                cmd,
                shell=sys.platform.startswith('win'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            print("✅ API сервер запущен в фоновом режиме")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка запуска API сервера: {e}")
            return False
    
    def open_web_interface(self):
        """Открытие веб-интерфейса"""
        print("🌐 Открытие веб-интерфейса...")
        
        if not self.web_file.exists():
            print(f"❌ Файл веб-интерфейса не найден: {self.web_file}")
            return False
        
        try:
            # Открываем в браузере
            webbrowser.open(f"file://{self.web_file.absolute()}")
            print("✅ Веб-интерфейс открыт в браузере")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка открытия браузера: {e}")
            print(f"💡 Откройте файл вручную: {self.web_file.absolute()}")
            return False
    
    def show_status(self):
        """Показ статуса системы"""
        print("\n" + "="*60)
        print("🎉 MESSAGE TREAKER ЗАПУЩЕН!")
        print("="*60)
        print("📱 Веб-интерфейс: Открыт в браузере")
        print("🔗 API сервер: http://127.0.0.1:8000")
        print("📊 API статус: http://127.0.0.1:8000/health")
        print("📋 Правила: http://127.0.0.1:8000/rules")
        print("🔔 История: http://127.0.0.1:8000/hits")
        print("\n💡 Следующие шаги:")
        print("1. В веб-интерфейсе добавьте правила мониторинга")
        print("2. Запустите watcher: python3 run_watcher.py")
        print("3. Отправьте тестовое сообщение в Telegram")
        print("\n⚠️  Для остановки нажмите Ctrl+C")
        print("="*60)
    
    def cleanup(self):
        """Очистка при завершении"""
        if self.api_process:
            print("\n🛑 Остановка API сервера...")
            self.api_process.terminate()
            try:
                self.api_process.wait(timeout=5)
                print("✅ API сервер остановлен")
            except subprocess.TimeoutExpired:
                self.api_process.kill()
                print("⚠️  API сервер принудительно остановлен")
    
    def run(self):
        """Основной цикл запуска"""
        try:
            print("🚀 ЗАПУСК MESSAGE TREAKER")
            print("="*40)
            
            # Проверяем зависимости
            if not self.check_dependencies():
                return False
            
            # Запускаем API сервер
            if not self.start_api_server():
                return False
            
            # Ждем готовности API
            if not self.wait_for_api():
                return False
            
            # Открываем веб-интерфейс
            if not self.open_web_interface():
                print("⚠️  Веб-интерфейс не открылся, но API работает")
            
            # Показываем статус
            self.show_status()
            
            # Ждем завершения
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Завершение работы...")
                
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            return False
        finally:
            self.cleanup()
        
        return True

def main():
    """Точка входа"""
    launcher = MessageTreakerLauncher()
    success = launcher.run()
    
    if not success:
        print("\n❌ Запуск не удался. Проверьте ошибки выше.")
        sys.exit(1)
    else:
        print("\n✅ Message Treaker завершен успешно")

if __name__ == "__main__":
    main()

