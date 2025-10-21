# watcher/main.py
import asyncio
import sqlite3
import time
from contextlib import closing
from loguru import logger
from watcher.tg_client import client, start_listening
from watcher.rules_engine import matches
from watcher.actions import trigger
from watcher.settings import DB_PATH

COOLDOWN_SEC = 60
_last_trigger_at = {}  # rule_id -> unix timestamp

def can_fire(rule_id: int) -> bool:
    """Check if rule can fire based on cooldown"""
    now = time.time()
    last = _last_trigger_at.get(rule_id, 0)
    if now - last < COOLDOWN_SEC:
        return False
    _last_trigger_at[rule_id] = now
    return True

def init_database():
    """Initialize database with required tables"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY,
                chat_id TEXT NOT NULL,
                pattern TEXT NOT NULL,
                match_type TEXT NOT NULL DEFAULT 'substring',
                action TEXT NOT NULL DEFAULT 'alarm',
                action_payload TEXT,
                enabled INTEGER NOT NULL DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS hits (
                id INTEGER PRIMARY KEY,
                rule_id INTEGER NOT NULL,
                message_id TEXT,
                chat_id TEXT,
                matched_text TEXT,
                triggered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(id)
            )
        """)
        conn.commit()
        logger.info("Database initialized")

def load_rules():
    """Load enabled rules from database"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute("SELECT * FROM rules WHERE enabled=1").fetchall()

def log_hit(rule_id, message_id, chat_id, matched_text):
    """Log rule hit to database"""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "INSERT INTO hits(rule_id, message_id, chat_id, matched_text) VALUES(?,?,?,?)",
            (rule_id, str(message_id), chat_id, matched_text)
        )
        conn.commit()

async def handler(event, text, chat_id, message_id):
    """Handle new message event"""
    rules = load_rules()
    
    for rule in rules:
        m = matches(text, rule["pattern"], rule["match_type"])
        if m:
            # Check if rule applies to this chat
            rule_chat_id = rule["chat_id"]
            is_chat_ok = (rule_chat_id == "*" or rule_chat_id == chat_id)

            if is_chat_ok and can_fire(rule["id"]):
                trigger(rule["action"], rule["action_payload"])
                log_hit(rule["id"], message_id, chat_id, m)

async def main():
    """Main watcher loop"""
    logger.info("Starting Message Treaker Watcher...")
    
    # Initialize database
    init_database()
    
    # Start Telegram client
    await client.start()
    logger.info("Telegram client started")
    
    # Start listening
    start_listening(handler)
    logger.info("Watcher started. Waiting for messages...")
    
    # Keep running
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
