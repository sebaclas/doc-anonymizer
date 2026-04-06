from anonymizer.detectors import patterns
from anonymizer.models import EntityType

text = """
El precio es de $ 1.000,50 pagaderos en cuotas.
Total: USD 500.
Monto en moneda local: 50.000 Pesos argentinos.
Transferencia de ARS 10.000 realizada.
Total en euros: 100,50 €.
Otra forma: 1.500USD.
Ignorar esto: 1234.
"""

ents = patterns.detect(text)
for e in ents:
    print(f"{e.entity_type.value}: \"{e.text}\"")

# Check if MONEY is found
has_money = any(e.entity_type == EntityType.MONEY for e in ents)
if has_money:
    print("\nSUCCESS: Money detected!")
else:
    print("\nFAILURE: Money NOT detected!")
