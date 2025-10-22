# watcher/actions.py
import subprocess
import sys
import os
# from playsound import playsound  # УДАЛИТЬ
import simpleaudio as sa # ДОБАВИТЬ
from loguru import logger

def trigger(action: str, payload: str|None):
    """Execute action with payload"""
    try:
        if action == 'notify':
            # Путь относительно скрипта
            current_dir = os.path.dirname(__file__)  # папка, где лежит этот .py
            path = os.path.join(current_dir, "assets", "alarm.wav")
            if os.path.exists(path):
                try:
                    wave_obj = sa.WaveObject.from_wave_file(path)
                    play_obj = wave_obj.play()
                    play_obj.wait_done() # Ждем завершения звука
                    logger.info(f"Alarm triggered: {path}")
                except Exception as e:
                    logger.error(f"Failed to play sound with simpleaudio: {e}")
                    print('\a') # Fallback to system beep
                    logger.info("Alarm triggered: system beep (simpleaudio error)")
            else:
                # Fallback to system beep if file not found
                print('\a')  # ASCII bell
                logger.info("Alarm triggered: system beep (file not found)")
                
        elif action == 'notify':
            # Минимально — распечатать; позже добавить системные уведомления
            message = payload or "Сработало правило"
            print(f"[NOTIFY] {message}")
            
        elif action == 'command':
            if not payload:
                logger.warning("Command action requires payload")
                return
            # Осторожно: исполняем локальную команду
            logger.info(f"Executing command: {payload}")
            subprocess.Popen(payload, shell=True)
            
        else:
            logger.warning(f"Unknown action: {action}")
            
    except Exception as e:
        logger.error(f"Action error ({action}): {e}")

