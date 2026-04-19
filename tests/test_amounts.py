import pytest
from anonymizer.detectors.amounts import detect
from anonymizer.models import EntityType

def test_detect_amounts_spanish():
    text = "El costo es de un mil doscientos pesos y tengo ochenta días."
    entities = detect(text)
    
    # We expect at least two entities: "un mil doscientos" and "ochenta"
    texts = [e.text.lower() for e in entities]
    assert any("mil" in t for t in texts)
    assert any("ochenta" in t for t in texts)
    assert all(e.entity_type == EntityType.AMOUNT for e in entities)

def test_detect_amounts_no_numbers():
    text = "Hola, esta es una frase sin números escritos."
    entities = detect(text)
    assert len(entities) == 0

def test_detect_amounts_mixed():
    text = "Tengo 5 vacas y veintidós gallinas."
    entities = detect(text)
    # text2num should catch "veintidós"
    # numbers like "5" are usually handled by regex, but text2num might catch them too if configured
    texts = [e.text.lower() for e in entities]
    assert "veintidós" in texts
