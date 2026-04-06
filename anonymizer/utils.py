from pathlib import Path
from anonymizer.extractors import docx_extractor, pdf_extractor
from anonymizer import replacer

def extract_document(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return docx_extractor.extract(path)
    elif suffix == ".pdf":
        doc_obj = pdf_extractor.extract(path)
        # Si el extractor de PDF devolviera un string puro (algunas versiones lo hacían), lo envolvemos.
        # Pero según pdf_extractor.py, ya devuelve un objeto Document. Veamos...
        return doc_obj
    else:
        raise ValueError(f"Formato no soportado: {suffix}")

def anonymize_document(input_path: Path, output_path: Path, mapping: dict, modes: dict = None):
    suffix = input_path.suffix.lower()
    if suffix == ".docx":
        return replacer.anonymize_docx(input_path, output_path, mapping, modes)
    elif suffix == ".pdf":
        return replacer.anonymize_pdf(input_path, output_path, mapping, modes)
    else:
        raise ValueError(f"Formato no soportado: {suffix}")
