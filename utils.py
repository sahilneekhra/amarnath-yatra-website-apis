import re
import time


def extract_slots(text: str) -> int:
    if not text:
        return 0

    if "full" in text.lower():
        return 0

    match = re.search(r'\d+', text.replace(',', ''))
    return int(match.group()) if match else 0


def sleep(seconds: float = 1.0):
    time.sleep(seconds)