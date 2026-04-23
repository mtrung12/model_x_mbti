import re


DIMENSIONS = [
    ("EI", ("E", "I")),
    ("SN", ("S", "N")),
    ("TF", ("T", "F")),
    ("JP", ("J", "P")),
]


def _normalize(text: str) -> str:
    return text.strip() if isinstance(text, str) else ""


def _extract_last_labeled_letters(text: str) -> str:
    """
    Extract answers from compact outputs like:
    E/I: I
    S/N: N
    T/F: F
    J/P: P

    Using the last match for each label avoids one-shot example leakage when
    the model echoes a template before giving its final answer.
    """
    result = []
    for label, pair in DIMENSIONS:
        left, right = pair
        pattern = rf"\b{left}\s*/\s*{right}\s*:\s*([{left}{right}])\b"
        matches = re.findall(pattern, text, re.IGNORECASE)
        result.append(matches[-1].upper() if matches else "?")
    return "".join(result)


def extract_zeroshot_result(text: str) -> str:
    """
    Parse terse labeled outputs from zero-shot prompts.
    """
    return _extract_last_labeled_letters(_normalize(text))


def extract_oneshot_result(text: str) -> str:
    """
    Parse one-shot outputs. The response may include explanatory lead-in text,
    and the prompt itself contains an example with the same labels, so we keep
    the last labeled answer for each dimension.
    """
    return _extract_last_labeled_letters(_normalize(text))


def extract_cot_result(text: str) -> str:
    """
    Parse chain-of-thought outputs shaped like:
    E/I:
    Evidence:
    Reasoning:
    Letter: I

    If section-based parsing fails, fall back to sequential Letter: matches.
    """
    normalized = _normalize(text)
    result = []
    label_token = r"\*{0,2}\s*Letter\s*:?\s*\*{0,2}"

    for label, pair in DIMENSIONS:
        left, right = pair
        section_pattern = (
            rf"(?:^|\n|#|\*)\s*{left}\s*/\s*{right}\s*:\s*"
            rf"[\s\S]*?{label_token}\s*([{left}{right}])\b"
        )
        match = re.search(section_pattern, normalized, re.IGNORECASE)
        result.append(match.group(1).upper() if match else "?")

    parsed = "".join(result)
    if "?" not in parsed:
        return parsed

    letter_matches = re.findall(
        rf"{label_token}\s*([EISNTFJP])\b", normalized, re.IGNORECASE
    )
    if len(letter_matches) >= 4:
        return "".join(letter.upper() for letter in letter_matches[:4])

    return parsed


def _extract_full_type(text: str) -> str | None:
    """
    Extract an explicit 4-letter MBTI type only when the model clearly marks it
    as the answer, not when it appears incidentally in evidence or user text.
    """
    patterns = [
        r"\b(?:MBTI|Type|Result|Answer)\s*[:\-]\s*([EI][SN][TF][JP])\b",
        r"\b([EI][SN][TF][JP])\b\s*(?:type|personality type)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).upper()
    return None
