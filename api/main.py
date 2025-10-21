from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from contextlib import closing
from typing import List, Optional
from watcher.settings import DB_PATH

app = FastAPI(title="Message Treaker API", version="1.0.0")

class Rule(BaseModel):
    chat_id: str
    pattern: str
    match_type: str = "substring"
    action: str = "alarm"
    action_payload: Optional[str] = None
    enabled: bool = True

class RuleResponse(BaseModel):
    id: int
    chat_id: str
    pattern: str
    match_type: str
    action: str
    action_payload: Optional[str]
    enabled: bool
    created_at: str

class HitResponse(BaseModel):
    id: int
    rule_id: int
    message_id: str
    chat_id: str
    matched_text: str
    triggered_at: str

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Message Treaker API"}

@app.get("/rules", response_model=List[RuleResponse])
def list_rules():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM rules ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

@app.post("/rules", response_model=dict)
def add_rule(rule: Rule):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO rules(chat_id,pattern,match_type,action,action_payload,enabled) VALUES(?,?,?,?,?,?)",
            (rule.chat_id, rule.pattern, rule.match_type, rule.action, rule.action_payload, 1 if rule.enabled else 0)
        )
        conn.commit()
        return {"id": cur.lastrowid, "message": "Rule created successfully"}

@app.get("/rules/{rule_id}", response_model=RuleResponse)
def get_rule(rule_id: int):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM rules WHERE id=?", (rule_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Rule not found")
        return dict(row)

@app.put("/rules/{rule_id}", response_model=dict)
def update_rule(rule_id: int, rule: Rule):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE rules SET chat_id=?, pattern=?, match_type=?, action=?, action_payload=?, enabled=? WHERE id=?",
            (rule.chat_id, rule.pattern, rule.match_type, rule.action, rule.action_payload, 1 if rule.enabled else 0, rule_id)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rule not found")
        conn.commit()
        return {"message": "Rule updated successfully"}

@app.delete("/rules/{rule_id}")
def delete_rule(rule_id: int):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM rules WHERE id=?", (rule_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rule not found")
        conn.commit()
        return {"message": "Rule deleted successfully"}

@app.get("/hits", response_model=List[HitResponse])
def list_hits(limit: int = 50):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM hits ORDER BY triggered_at DESC LIMIT ?", 
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

@app.get("/hits/rule/{rule_id}", response_model=List[HitResponse])
def get_hits_for_rule(rule_id: int, limit: int = 20):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM hits WHERE rule_id=? ORDER BY triggered_at DESC LIMIT ?", 
            (rule_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]

if __name__ == "__main__":
    import uvicorn
    from watcher.settings import API_HOST, API_PORT
    uvicorn.run(app, host=API_HOST, port=API_PORT)



