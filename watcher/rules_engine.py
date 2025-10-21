# watcher/rules_engine.py
import re
from typing import Literal, Optional

def matches(text: str, pattern: str, match_type: Literal['substring','regex']) -> Optional[str]:
    """Check if text matches pattern according to match_type"""
    if match_type == 'substring':
        return pattern if pattern.lower() in text.lower() else None
    else:
        try:
            m = re.search(pattern, text, re.IGNORECASE|re.MULTILINE)
            return m.group(0) if m else None
        except re.error as e:
            print(f"Regex error: {e}")
            return None



