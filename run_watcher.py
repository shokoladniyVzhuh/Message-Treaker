#!/usr/bin/env python3
"""
Message Treaker Watcher Runner
Запуск демона для мониторинга Telegram
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from watcher.main import main
import asyncio

if __name__ == "__main__":
    print("🚀 Starting Message Treaker Watcher...")
    asyncio.run(main())



