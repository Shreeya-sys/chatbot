from pathlib import Path

import chromadb
from pypdf import PdfReader

from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_DIMENSIONS
from src.local_embeddings import LocalHashEmbeddingFunction


DATA_DIR = Path("data")

SEED_DOCUMENTS = {
    "data/antibiotics/cdc_antibiotic_basics.txt": {
        "source": "CDC",
        "title": "Antibiotic Use Basics",
        "url": "https://www.cdc.gov/antibiotic-use/about/index.html",
        "text": (
            "Antibiotics are medicines used to treat certain bacterial infections. Antibiotics do not work "
            "on viruses, such as those that cause colds, flu, or COVID-19. Taking antibiotics when they are "
            "not needed can cause side effects and contribute to antibiotic resistance."
        ),
    },
    "data/antibiotics/medlineplus_antibiotics.txt": {
        "source": "MedlinePlus",
        "title": "Antibiotics",
        "url": "https://medlineplus.gov/antibiotics.html",
        "text": (
            "Antibiotics fight bacterial infections. They are not effective against viral infections. "
            "People should take antibiotics only as directed by a healthcare provider and should not save "
            "antibiotics for later use or use another person's prescription."
        ),
    },
    "data/respiratory_infections/cdc_flu.txt": {
        "source": "CDC",
        "title": "About Flu",
        "url": "https://www.cdc.gov/flu/about/index.html",
        "text": (
            "Influenza is a contagious respiratory illness caused by influenza viruses. Antibiotics do not "
            "treat influenza itself because flu is viral. A clinician may prescribe antibiotics if a bacterial "
            "infection is suspected or confirmed in addition to a viral illness."
        ),
    },
    "data/dehydration/medlineplus_dehydration.txt": {
        "source": "MedlinePlus",
        "title": "Dehydration",
        "url": "https://medlineplus.gov/dehydration.html",
        "text": (
            "Dehydration happens when the body does not have as much water and fluids as it needs. Treatment "
            "depends on severity. Mild dehydration may improve with fluids, but severe dehydration needs urgent "
            "medical care. Drinking excessive water very quickly can be unsafe and is not always appropriate."
        ),
    },
    "data/dehydration/who_rehydration.txt": {
        "source": "WHO",
        "title": "Oral Rehydration Salts",
        "url": "https://www.who.int/",
        "text": (
            "Oral rehydration therapy replaces water and electrolytes lost during dehydration, especially from "
            "diarrhoeal illness. Rehydration should replace both fluid and salts; rapid excessive plain-water "
            "intake is not a universal or risk-free treatment."
        ),
    },
    "data/general_health/soil_salinity_scope.txt": {
        "source": "General agriculture note",
        "title": "Soil Salinity Scope Example",
        "url": "",
        "text": (
            "Soil salinity is outside the healthcare scope. Common causes include poor drainage, high evaporation, "
            "saline irrigation water, seawater intrusion, and overuse of fertilizers. Farmers may reduce salinity "
            "through drainage, leaching salts with suitable water, salt-tolerant crops, and careful irrigation management."
        ),
    },
}


def ensure_seed_data() -> None:
    for file_name, payload in SEED_DOCUMENTS.items():
        path = Path(file_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(payload["text"], encoding="utf-8")


def read_document(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    cleaned = " ".join(text.split())
    if len(cleaned) <= chunk_size:
        return [cleaned]
    chunks = []
    start = 0
    while start < len(cleaned):
        end = start + chunk_size
        chunks.append(cleaned[start:end])
        start = max(end - overlap, start + 1)
    return chunks


def metadata_for(path: Path) -> dict:
    normalized = str(path).replace("\\", "/")
    if normalized in SEED_DOCUMENTS:
        payload = SEED_DOCUMENTS[normalized]
        return {key: payload[key] for key in ("source", "title", "url")}
    return {"source": path.parent.name.replace("_", " ").title(), "title": path.stem, "url": ""}


def build_vectorstore() -> int:
    ensure_seed_data()
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embedder = LocalHashEmbeddingFunction(dimensions=EMBEDDING_DIMENSIONS)
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedder)

    ids = []
    documents = []
    metadatas = []

    for path in DATA_DIR.rglob("*"):
        if path.suffix.lower() not in {".txt", ".md", ".pdf"}:
            continue
        text = read_document(path)
        for index, chunk in enumerate(chunk_text(text)):
            ids.append(f"{path.as_posix()}::{index}")
            documents.append(chunk)
            metadatas.append(metadata_for(path))

    if ids:
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    return len(ids)


if __name__ == "__main__":
    total = build_vectorstore()
    print(f"Indexed {total} chunks into ChromaDB.")
