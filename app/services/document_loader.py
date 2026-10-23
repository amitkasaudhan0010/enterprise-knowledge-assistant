from pathlib import Path

from pypdf import PdfReader


def load_document(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".txt":
        text = file_path.read_text(encoding="utf-8")

    elif suffix == ".pdf":
        reader = PdfReader(str(file_path))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    else:
        raise ValueError("Only PDF and TXT files are supported.")

    text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    if not text:
        raise ValueError(
            "No extractable text found in the document."
        )

    return text