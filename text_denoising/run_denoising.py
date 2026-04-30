from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib import error, request

import spacy
from tqdm import tqdm


@dataclass(frozen=True)
class ChunkRecord:
    source_file: Path
    chunk_index: int
    sentence_start: int
    sentence_end: int
    sentences: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Split texts into sentence chunks, classify them with Ollama, "
            "and write denoised outputs with provenance markers."
        )
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("custom_family_bench/royalty/texts"),
        help="Directory containing the raw .txt files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("text_denoising/denoised_texts"),
        help="Directory where denoised .txt files will be written.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        default=Path("text_denoising/prompt.md"),
        help="System prompt file used for chunk classification.",
    )
    parser.add_argument(
        "--model",
        default="llama3.2",
        help="Ollama model name to query.",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:11434",
        help="Base URL for the Ollama API.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=4,
        help="Number of sentences per chunk.",
    )
    return parser.parse_args()


def load_spacy_pipeline() -> spacy.language.Language:
    try:
        return spacy.load("en_core_web_sm")
    except OSError as exc:
        raise SystemExit(
            "spaCy model 'en_core_web_sm' is not installed. Install it before running this script."
        ) from exc


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_system_prompt(prompt_file: Path) -> str:
    prompt = read_text(prompt_file).strip()
    if not prompt:
        raise SystemExit(f"System prompt file is empty: {prompt_file}")
    return prompt


def sentence_chunks(sentences: list[str], chunk_size: int) -> Iterable[tuple[int, list[str]]]:
    for chunk_start in range(0, len(sentences), chunk_size):
        yield chunk_start, sentences[chunk_start : chunk_start + chunk_size]


def build_chunk_records(source_file: Path, sentences: list[str], chunk_size: int) -> list[ChunkRecord]:
    records: list[ChunkRecord] = []
    for chunk_number, (chunk_start, chunk_sentences) in enumerate(
        sentence_chunks(sentences, chunk_size),
        start=1,
    ):
        records.append(
            ChunkRecord(
                source_file=source_file,
                chunk_index=chunk_number,
                sentence_start=chunk_start + 1,
                sentence_end=chunk_start + len(chunk_sentences),
                sentences=chunk_sentences,
            )
        )
    return records


def classify_chunk(base_url: str, model: str, system_prompt: str, chunk_record: ChunkRecord) -> str:
    user_prompt = "\n".join(chunk_record.sentences)
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    api_url = f"{base_url.rstrip('/')}/api/chat"
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        api_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=120) as response:
            body = response.read().decode("utf-8")
    except error.URLError as exc:
        raise RuntimeError(f"Failed to query Ollama at {api_url}: {exc}") from exc

    payload = json.loads(body)
    message = payload.get("message", {})
    content = str(message.get("content", "")).strip()
    if not content:
        raise RuntimeError(f"Empty response returned for {chunk_record.provenance}")
    return content


def is_yes(response: str) -> bool:
    if "YES" in response:
        return True
    return False


def format_kept_chunk(chunk_record: ChunkRecord) -> str:
    body = " ".join(sentence.strip() for sentence in chunk_record.sentences if sentence.strip())
    return body


def process_text_file(
    source_file: Path,
    output_dir: Path,
    nlp: spacy.language.Language,
    system_prompt: str,
    base_url: str,
    model: str,
    chunk_size: int,
 ) -> tuple[Path, int, int]:
    text = read_text(source_file)
    doc = nlp(text)
    sentences = [sentence.text.strip() for sentence in doc.sents if sentence.text.strip()]
    first_sentence = sentences[:1]
    remaining_sentences = sentences[1:]
    records = build_chunk_records(source_file, remaining_sentences, chunk_size)
    
    kept_chunks: list[str] = []
    if first_sentence:
        kept_chunks.append(first_sentence[0])

    pbar = tqdm(records, desc=f"Processing {source_file.name}", leave=False)
    for chunk_record in pbar:
        response = classify_chunk(base_url, model, system_prompt, chunk_record)
        if is_yes(response):
            kept_chunks.append(format_kept_chunk(chunk_record))
        pbar.set_postfix({"retained": len(kept_chunks), "total": len(records), "rate": f"{len(kept_chunks)/len(records)*100:.1f}%"})

    pbar.close()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / source_file.name
    output_path.write_text("\n".join(kept_chunks) + ("\n" if kept_chunks else ""), encoding="utf-8")
    return output_path, len(kept_chunks), len(records) + (1 if first_sentence else 0)


def iter_input_files(input_dir: Path) -> list[Path]:
    return sorted(path for path in input_dir.glob("*.txt") if path.is_file())


def main() -> None:
    args = parse_args()
    nlp = load_spacy_pipeline()
    system_prompt = load_system_prompt(args.prompt_file)
    input_files = iter_input_files(args.input_dir)

    if not input_files:
        raise SystemExit(f"No .txt files found in {args.input_dir}")

    total_chunks = 0
    total_retained = 0
    pbar = tqdm(input_files, desc="Processing files")
    for source_file in pbar:
        _, retained, chunks = process_text_file(
            source_file=source_file,
            output_dir=args.output_dir,
            nlp=nlp,
            system_prompt=system_prompt,
            base_url=args.base_url,
            model=args.model,
            chunk_size=args.chunk_size,
        )
        total_chunks += chunks
        total_retained += retained
        rate = f"{(total_retained/total_chunks*100):.1f}%" if total_chunks else "0.0%"
        pbar.set_postfix({"global_retained": total_retained, "global_total": total_chunks, "global_rate": rate})

    print(f"\nGlobal retention: {total_retained}/{total_chunks} chunks retained ({(total_retained/total_chunks*100) if total_chunks else 0:.1f}%)")


if __name__ == "__main__":
    main()