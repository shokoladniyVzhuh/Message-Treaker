#!/usr/bin/env python3
"""
Запуск интерактивной настройки мониторинга
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.setup_monitoring import ChatMonitorSetup

if __name__ == "__main__":
    print("🚀 Запуск настройки мониторинга...")
    setup = ChatMonitorSetup()
    setup.run()

