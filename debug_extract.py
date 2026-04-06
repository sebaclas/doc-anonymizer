from anonymizer.extractors import docx_extractor
from pathlib import Path

path = Path("sample_docs/carta1.docx")
doc = docx_extractor.extract(path)
print("--- FULL TEXT ---")
print(doc.full_text)
print("--- END ---")
