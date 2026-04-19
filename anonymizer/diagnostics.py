import re
from typing import List, Optional, Tuple, Any
from anonymizer.models import Entity, EntityType, Document
from anonymizer.config import current_settings
from anonymizer.detectors import ner, patterns as pat_module, detector, amounts
from anonymizer.detectors.ner import _LABEL_MAP

def check_filters(text: str) -> List[str]:
    """Check why a piece of text might be filtered out by the NER pipeline."""
    reasons = []
    text_strip = text.strip()
    
    if len(text_strip) < 3:
        reasons.append("Length < 3 chars")
    
    if text_strip.lower() in current_settings.ner_stopwords:
        reasons.append(f"In stopwords list: '{text_strip.lower()}'")
        
    if all(c.isdigit() or c in ".,-%$/\n\t " for c in text_strip):
        reasons.append("Contains only digits/symbols")
        
    if "\n" in text_strip:
        reasons.append("Contains newlines (NER split by line)")
        
    return reasons

def find_raw_matches(text: str, target: str) -> List[Tuple[int, int]]:
    """Find all raw occurrences of target in text (case insensitive)."""
    return [(m.start(), m.end()) for m in re.finditer(re.escape(target), text, re.IGNORECASE)]

def check_shadowing(all_candidates: List[Entity], target_span: Tuple[int, int]) -> Optional[Entity]:
    """Check if the target span is shadowed by another higher-priority entity."""
    t_start, t_end = target_span
    
    # Sort identical to detector._deduplicate logic
    priority = {"known": 0, "regex": 1, "ner": 2, "text2num": 3}
    sorted_ents = sorted(all_candidates, key=lambda e: (
        e.start, 
        priority.get(e.source, 3), 
        -(e.end - e.start)
    ))

    # Simulate the deduplicator's selection
    last_end = -1
    for ent in sorted_ents:
        is_target = (ent.start == t_start and ent.end == t_end)
        
        if ent.start >= last_end:
            # This entity was selected
            if is_target:
                return None # Not shadowed, it's accepted!
            last_end = ent.end
        else:
            # This entity was shadowed/discarded
            if is_target:
                # We found why our target was discarded! 
                # Find which one specifically overlapped it.
                for accepted in all_candidates:
                    # An entity overlaps target if it was selected and covers any part of target
                    # But actually we want the one that caused the skip.
                    # In _deduplicate, it's the one that set last_end.
                    pass
                # The one that caused the skip is the one currently in the "selected" set that overlaps
                # But for simplicity, we'll return the one that is currently 'active' (last_end setter)
                # or just any overlapping higher priority one.
                for other in sorted_ents:
                    if other == ent: continue
                    # Overlap check
                    if not (other.end <= ent.start or other.start >= ent.end):
                        # It overlaps. If it's earlier in sorted_ents, it shadowed it.
                        if sorted_ents.index(other) < sorted_ents.index(ent):
                            return other
                return Entity(text="Unknown", entity_type=EntityType.CUSTOM, start=0, end=0, source="unknown")

    return None

def diagnose_span(text: str, target_text: str, expected_type: Optional[EntityType] = None) -> dict:
    """Perform a full autopsy on why target_text might be missing."""
    results = {
        "text": text,
        "target": target_text,
        "raw_matches": [],
        "filters": [],
        "candidates": [],
        "shadowed_by": None,
        "final_result": None,
        "status": "not_found"
    }

    # 1. Raw matches
    matches = find_raw_matches(text, target_text)
    results["raw_matches"] = matches
    if not matches:
        results["status"] = "not_in_text"
        return results

    # 2. Filter check
    results["filters"] = check_filters(target_text)

    # 3. Get all candidates (skip deduplication for now)
    doc = Document(path="diagnostic_mock", full_text=text)
    
    # Manually run detectors to get raw candidates
    ner_ents = ner.detect(text)
    from anonymizer.config import load_custom_patterns
    active_patterns = load_custom_patterns()
    regex_ents = pat_module.detect(text, active_patterns)
    # Get known entities from current settings if available
    from anonymizer import known_entities as ke_module
    known_entities = ke_module.load()
    known_ents = detector._detect_known(text, known_entities)
    
    amount_ents = amounts.detect(text)
    
    all_candidates = ner_ents + regex_ents + known_ents + amount_ents
    results["candidates"] = [
        {"text": e.text, "type": e.entity_type.value, "source": e.source, "span": (e.start, e.end)} 
        for e in all_candidates
    ]

    # Check if target is among candidates
    target_candidates = [e for e in all_candidates if e.text.lower() == target_text.lower()]
    
    # 4. Final detection
    final_entities = detector.detect_all(doc)
    found_in_final = [e for e in final_entities if e.text.lower() == target_text.lower()]
    
    if found_in_final:
        results["status"] = "found"
        results["final_result"] = found_in_final[0]
        return results

    # 5. Shadow/Filter check
    if target_candidates:
        # It was found as a candidate but not in final results
        # Check first span for shadowing
        shadow = check_shadowing(all_candidates, (target_candidates[0].start, target_candidates[0].end))
        if shadow:
            results["shadowed_by"] = {
                "text": shadow.text,
                "type": shadow.entity_type.value,
                "source": shadow.source,
                "span": (shadow.start, shadow.end)
            }
            results["status"] = "shadowed"
        else:
            # If it's a candidate but not in final, and no shadow found,
            # it might be due to a filter (currently only NER has filters in detect())
            # but regex/known don't.
            if results["filters"]:
                results["status"] = "filtered"
            else:
                results["status"] = "unexplained_missing"
    else:
        # Not even found as a candidate
        results["status"] = "ner_regex_failure"
        if results["filters"]:
            # Add filter info to details if it was missed
            pass

    return results
