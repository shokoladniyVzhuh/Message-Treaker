#!/usr/bin/env python3
"""
Интерактивная настройка мониторинга чатов
Скрипт для настройки правил мониторинга Telegram чатов
"""

import sys
import os
import requests
import json
from telethon import TelegramClient
from watcher.settings import API_ID, API_HASH, SESSION, API_HOST, API_PORT

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ChatMonitorSetup:
    def __init__(self):
        self.api_url = f"http://{API_HOST}:{API_PORT}"
        self.client = None
        
    def connect_telegram(self):
        """Подключение к Telegram"""
        try:
            self.client = TelegramClient(SESSION, API_ID, API_HASH)
            self.client.start()
            print("✅ Подключение к Telegram успешно!")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к Telegram: {e}")
            return False
    
    def get_chat_list(self):
        """Получение списка доступных чатов"""
        if not self.client:
            return []
        
        try:
            dialogs = self.client.iter_dialogs()
            chats = []
            
            for dialog in dialogs:
                chat_info = {
                    'id': dialog.id,
                    'title': dialog.title or dialog.name or "Без названия",
                    'username': dialog.entity.username if hasattr(dialog.entity, 'username') else None,
                    'type': 'channel' if hasattr(dialog.entity, 'broadcast') else 
                           'group' if hasattr(dialog.entity, 'megagroup') else 'private'
                }
                chats.append(chat_info)
            
            return chats
        except Exception as e:
            print(f"❌ Ошибка получения списка чатов: {e}")
            return []
    
    def display_chat_options(self):
        """Отображение опций выбора чатов"""
        print("\n" + "="*50)
        print("🔍 ВЫБОР ЧАТОВ ДЛЯ МОНИТОРИНГА")
        print("="*50)
        print("1. Мониторить по username чата")
        print("2. Мониторить по chat_id")
        print("3. Мониторить все чаты (*)")
        print("4. Найти чат по названию")
        print("0. Выход")
        print("="*50)
    
    def search_chat_by_name(self):
        """Поиск чата по названию"""
        search_term = input("Введите название чата для поиска: ").strip().lower()
        if not search_term:
            print("❌ Название не может быть пустым!")
            return None
        
        chats = self.get_chat_list()
        matches = []
        
        for chat in chats:
            if search_term in chat['title'].lower():
                matches.append(chat)
        
        if not matches:
            print(f"❌ Чаты с названием '{search_term}' не найдены")
            return None
        
        if len(matches) == 1:
            chat = matches[0]
            print(f"✅ Найден чат: {chat['title']} (ID: {chat['id']})")
            return chat['id']
        
        # Если найдено несколько чатов
        print(f"\n🔍 Найдено {len(matches)} чатов:")
        print("-" * 70)
        print(f"{'№':<3} {'ID':<15} {'Username':<20} {'Название':<25}")
        print("-" * 70)
        
        for i, chat in enumerate(matches, 1):
            username = chat['username'] or "нет"
            title = chat['title'][:22] + "..." if len(chat['title']) > 25 else chat['title']
            print(f"{i:<3} {chat['id']:<15} {username:<20} {title:<25}")
        
        print("-" * 70)
        
        while True:
            try:
                choice = int(input(f"Выберите чат (1-{len(matches)}): "))
                if 1 <= choice <= len(matches):
                    selected_chat = matches[choice - 1]
                    print(f"✅ Выбран чат: {selected_chat['title']}")
                    return selected_chat['id']
                else:
                    print(f"❌ Введите число от 1 до {len(matches)}")
            except ValueError:
                print("❌ Введите корректное число")
    
    def get_chat_selection(self):
        """Получение выбора пользователя"""
        while True:
            self.display_chat_options()
            choice = input("\nВыберите опцию (0-4): ").strip()
            
            if choice == "0":
                print("👋 До свидания!")
                return None, None
            
            elif choice == "1":
                username = input("Введите username чата (без @): ").strip()
                if username:
                    return "username", username
                else:
                    print("❌ Username не может быть пустым!")
            
            elif choice == "2":
                chat_id = input("Введите chat_id (число или -1001234567890): ").strip()
                if chat_id:
                    try:
                        # Пробуем преобразовать в число для валидации
                        int(chat_id)
                        return "chat_id", chat_id
                    except ValueError:
                        print("❌ chat_id должен быть числом!")
                else:
                    print("❌ chat_id не может быть пустым!")
            
            elif choice == "3":
                confirm = input("⚠️  Мониторить ВСЕ чаты? (да/нет): ").strip().lower()
                if confirm in ['да', 'yes', 'y', 'д']:
                    return "all", "*"
                else:
                    print("❌ Отменено")
            
            elif choice == "4":
                chat_id = self.search_chat_by_name()
                if chat_id:
                    return "chat_id", str(chat_id)
            
            else:
                print("❌ Неверный выбор! Попробуйте снова.")
    
    def get_pattern_and_action(self):
        """Получение паттерна и действия от пользователя"""
        print("\n" + "="*50)
        print("📝 НАСТРОЙКА ПРАВИЛА")
        print("="*50)
        
        # Паттерн - упрощенный ввод
        print("\n🔍 Что искать в сообщениях?")
        pattern = input("Введите фразу для поиска: ").strip()
        if not pattern:
            print("❌ Фраза не может быть пустой!")
            return None
        
        # Пока что простое действие - вывод в консоль
        print(f"\n✅ Правило настроено!")
        print(f"📝 Ищем фразу: '{pattern}'")
        print(f"⚡ При нахождении: вывод 'найдено!' в консоль")
        
        return {
            'pattern': pattern,
            'match_type': 'substring',  # Всегда substring для простоты
            'action': 'notify',
            'action_payload': f'найдено! (фраза: {pattern})'
        }
    
    def create_rule(self, chat_type, chat_value, rule_data):
        """Создание правила через API"""
        try:
            rule = {
                'chat_id': chat_value,
                'pattern': rule_data['pattern'],
                'match_type': rule_data['match_type'],
                'action': rule_data['action'],
                'action_payload': rule_data['action_payload'],
                'enabled': True
            }
            
            response = requests.post(f"{self.api_url}/rules", json=rule)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Правило создано успешно! ID: {result['id']}")
                return True
            else:
                print(f"❌ Ошибка создания правила: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при создании правила: {e}")
            return False
    
    def test_api_connection(self):
        """Проверка подключения к API"""
        try:
            response = requests.get(f"{self.api_url}/health")
            if response.status_code == 200:
                print("✅ API сервер доступен!")
                return True
            else:
                print(f"❌ API сервер недоступен: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Не удается подключиться к API: {e}")
            print(f"💡 Убедитесь, что API сервер запущен: python run_api.py")
            return False
    
    def run(self):
        """Основной цикл настройки"""
        print("🚀 НАСТРОЙКА МОНИТОРИНГА TELEGRAM ЧАТОВ")
        print("="*50)
        
        # Проверяем API
        if not self.test_api_connection():
            return
        
        # Подключаемся к Telegram
        if not self.connect_telegram():
            return
        
        while True:
            # Выбор чата
            chat_type, chat_value = self.get_chat_selection()
            if chat_type is None:
                break
            
            # Настройка правила
            rule_data = self.get_pattern_and_action()
            if rule_data is None:
                continue
            
            # Показываем сводку
            print("\n" + "="*50)
            print("📋 СВОДКА НАСТРОЙКИ")
            print("="*50)
            print(f"Чат: {chat_value}")
            print(f"Ищем фразу: '{rule_data['pattern']}'")
            print(f"Действие: вывод в консоль")
            
            # Подтверждение
            confirm = input("\nСоздать это правило? (да/нет): ").strip().lower()
            if confirm in ['да', 'yes', 'y', 'д']:
                if self.create_rule(chat_type, chat_value, rule_data):
                    print("✅ Правило успешно создано!")
                    print("💡 Теперь запустите watcher: python run_watcher.py")
                else:
                    print("❌ Не удалось создать правило")
            else:
                print("❌ Отменено")
            
            # Продолжить?
            continue_setup = input("\nСоздать еще одно правило? (да/нет): ").strip().lower()
            if continue_setup not in ['да', 'yes', 'y', 'д']:
                break
        
        # Закрываем Telegram клиент
        if self.client:
            self.client.disconnect()
        
        print("\n👋 Настройка завершена!")
        print("💡 Теперь запустите watcher: python run_watcher.py")

if __name__ == "__main__":
    setup = ChatMonitorSetup()
    setup.run()
