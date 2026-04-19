from __future__ import annotations
import re
from anonymizer.models import Entity, EntityType
from anonymizer.config import current_settings

# text_to_num uses language codes like "es", "en", "fr", etc.
# We'll default to "es" for now as per requirements.

def _get_lang():
    # Attempt to derive from settings or use "es" as fallback
    # For now, following task 2.2: "usando 'es' por defecto"
    return "es"

def detect(text: str) -> list[Entity]:
    """
    Detect written numbers in text using text2num.
    Processes line by line to maintain compatibility and avoid cross-line matches.
    """
    try:
        from text_to_num import text2num
    except ImportError:
        # If not installed, return empty list to avoid crashing the whole pipeline
        return []

    lang = _get_lang()
    entities = []
    char_offset = 0

    # Pattern to find candidate sequences of words (alphabetic characters + spaces/hyphens)
    # This reduces the number of calls to text2num
    candidate_pattern = re.compile(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]+(?:[\s-][a-zA-ZáéíóúÁÉÍÓÚñÑ]+)*')

    for line in text.split("\n"):
        if line.strip():
            # Find all sequences of words that could potentially be a number
            for match in candidate_pattern.finditer(line):
                candidate_text = match.group()
                
                # We try to parse the whole candidate.
                # If it's a number like "veinte y cinco", text2num will handle it.
                # However, some candidates might contain non-number words at the start/end
                # like "Tengo veinte". text2num might fail.
                
                # To be robust, we can split into words and try to find the longest sub-sequence
                words = candidate_text.split()
                n = len(words)
                
                # Sliding window to find the longest sequence of words that is a valid number
                i = 0
                while i < n:
                    found_in_window = False
                    for j in range(n, i, -1):
                        window_words = words[i:j]
                        window_text = " ".join(window_words)
                        
                        # Optimization: skip very short words that are likely common stop words
                        # unless they are part of a larger number
                        if len(window_text) < 2 and window_text.lower() not in ["un", "1"]:
                            continue

                        # Try languages
                        val = None
                        for lng in ["es", "en"]:
                            try:
                                val = text2num(window_text, lng)
                                break  # Success
                            except (ValueError, Exception):
                                pass
                        
                        if val is not None:
                            # Filter: skip single-word "un", "una", "a", "one" if they might be just articles
                            # but keep them if they are part of a multi-word number (checked by window size)
                            if len(window_words) == 1 and window_text.lower() in ["un", "una", "a"]:
                                continue
                            
                            # Find the start offset of this window within the candidate
                            # This is a bit tricky due to extra spaces, but search should work
                            start_in_candidate = candidate_text.find(window_text)
                            if start_in_candidate != -1:
                                start_pos = match.start() + start_in_candidate
                                end_pos = start_pos + len(window_text)
                                
                                entities.append(Entity(
                                    text=window_text,
                                    entity_type=EntityType.AMOUNT,
                                    start=start_pos + char_offset,
                                    end=end_pos + char_offset,
                                    source="text2num",
                                    context=f"Valor: {val}"
                                ))
                                i = j  # Move past this sequence
                                found_in_window = True
                                break
                    
                    if not found_in_window:
                        i += 1

        char_offset += len(line) + 1

    return entities
