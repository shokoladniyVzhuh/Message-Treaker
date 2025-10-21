#!/bin/bash

# Message Treaker - Простой запуск
echo "🚀 MESSAGE TREAKER - БЫСТРЫЙ ЗАПУСК"
echo "=================================="

# Проверяем виртуальное окружение
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "💡 Создайте его: python3 -m venv venv"
    echo "💡 Активируйте: source venv/bin/activate"
    echo "💡 Установите зависимости: pip install -r requirements.txt"
    exit 1
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем .env файл
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "💡 Скопируйте: cp env.example .env"
    echo "💡 Заполните API ключи в .env"
    exit 1
fi

# Запускаем полную систему
echo "🚀 Запуск полной системы..."
python3 start_full.py

