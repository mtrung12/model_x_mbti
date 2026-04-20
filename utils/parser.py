import re

def extract_result(text):
    """
    Parses MBTI dimensions from text and returns a 4-letter string.
    Works for Zero-shot, One-shot, and CoT formats.
    """
    # Define the order of dimensions
    dimensions = [
        ('E', 'I'),
        ('S', 'N'),
        ('T', 'F'),
        ('J', 'P')
    ]
    
    result = ""
    
    for pair in dimensions:
        # Regex explanation:
        # Look for the Letter (e.g., 'E' or 'I') that follows a label like "Letter:" or "E/I:"
        # Or simply find the first occurrence of one of the two letters in that dimension.
        pattern = rf"\b({'|'.join(pair)})\b"
        
        # We search specifically for the "Letter: [X]" format first for CoT accuracy
        cot_pattern = rf"Letter:\s*({'|'.join(pair)})"
        match_cot = re.search(cot_pattern, text, re.IGNORECASE)
        
        if match_cot:
            result += match_cot.group(1).upper()
        else:
            # Fallback for simpler formats (Zero-shot/One-shot)
            match_simple = re.search(pattern, text, re.IGNORECASE)
            if match_simple:
                result += match_simple.group(1).upper()
            else:
                result += "?" # Placeholder if a dimension is missing
                
    return result

