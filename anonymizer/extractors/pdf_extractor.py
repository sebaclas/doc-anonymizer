from pathlib import Path
import pdfplumber
from anonymizer.models import Document


def extract(path: str | Path) -> Document:
    path = Path(path)
    paragraphs = []

    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.splitlines():
                line = line.strip()
                if line:
                    paragraphs.append(line)

    full_text = "\n".join(paragraphs)
    return Document(path=str(path), paragraphs=paragraphs, full_text=full_text)
