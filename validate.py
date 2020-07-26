from typing import Optional

def validate_answer(text: str) -> Optional[int]:

    try:
        text.replace(",", ".")
        answer = float(text)

    except (TypeError, ValueError):
        return None

    if answer < 0 or answer > 100:
        return None
    return answer