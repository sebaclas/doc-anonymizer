import pytest
from anonymizer.matcher import MatchResult, match_against_db
from anonymizer.known_entities import KnownEntity

def test_fuzzy_match_ensayo():
    # Simulamos una entidad conocida con "Juan Pérez"
    ke = KnownEntity(
        original="Juan Pérez", 
        pseudonym="Persona_A", 
        entity_type="PER", 
        aliases=[]
    )
    
    # Probamos con "Juan Perez" (sin tilde)
    detected = ["Juan Perez"]
    # El threshold por defecto suele ser alto, aquí forzamos 80.0 para el ensayo
    matches, unmatched = match_against_db(detected, [ke], threshold=80.0)
    
    print(f"\n[ENSAYO] Matches: {matches}")
    
    assert len(matches) == 1
    assert matches[0].is_exact is False
    assert matches[0].known.pseudonym == "Persona_A"
    assert len(unmatched) == 0

def test_exact_match_ensayo():
    ke = KnownEntity(
        original="Empresa S.A.", 
        pseudonym="ORG_1", 
        entity_type="ORG", 
        aliases=[]
    )
    
    # Coincidencia exacta (ignorando capitalización por defecto en el matcher)
    matches, unmatched = match_against_db(["empresa s.a."], [ke])
    
    assert len(matches) == 1
    assert matches[0].is_exact is True
    assert matches[0].known.pseudonym == "ORG_1"
