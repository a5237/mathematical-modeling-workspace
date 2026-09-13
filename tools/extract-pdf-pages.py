#!/usr/bin/env python3
"""Extract complete PDF pages or normalized page regions into temporary files."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


TOOL_VERSION = "1.0.0"
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_ROOT = WORKSPACE_ROOT / "var" / "temp" / "pdf-extracts"


class PdfExtractError(RuntimeError):
    """A user-actionable PDF extraction error."""


def configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(WORKSPACE_ROOT).as_posix()
    except ValueError:
        return path.name


def safe_filename_part(value: str, fallback: str = "document") -> str:
    normalized = unicodedata.normalize("NFKD", value)
    text = normalized.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    if text:
        return text
    codepoints = "-".join(f"u{ord(character):x}" for character in normalized if character.isalnum())
    return codepoints[:80].rstrip("-") or fallback


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def parse_pages(specification: str, page_count: int) -> list[int]:
    if specification.strip().casefold() == "all":
        return list(range(1, page_count + 1))

    pages: list[int] = []
    seen: set[int] = set()
    for raw_part in specification.split(","):
        part = raw_part.strip()
        if not part:
            raise PdfExtractError("--pages contains an empty item")
        range_match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if range_match:
            start, end = map(int, range_match.groups())
            if end < start:
                raise PdfExtractError(f"descending page range is not allowed: {part}")
            candidates = range(start, end + 1)
        elif part.isdigit():
            candidates = (int(part),)
        else:
            raise PdfExtractError(f"invalid page item: {part!r}")
        for page_number in candidates:
            if not 1 <= page_number <= page_count:
                raise PdfExtractError(
                    f"page {page_number} is outside the document range 1..{page_count}"
                )
            if page_number not in seen:
                seen.add(page_number)
                pages.append(page_number)
    if not pages:
        raise PdfExtractError("no pages were selected")
    return pages


def validate_crop(values: Sequence[float] | None) -> tuple[float, float, float, float] | None:
    if values is None:
        return None
    left, top, right, bottom = values
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise PdfExtractError(
            "--crop must satisfy 0 <= left < right <= 1 and 0 <= top < bottom <= 1"
        )
    return left, top, right, bottom


def page_tag(pages: Sequence[int]) -> str:
    expanded = "-".join(f"{page:03d}" for page in pages)
    if len(expanded) <= 60:
        return expanded
    return f"{pages[0]:03d}-{pages[-1]:03d}-{len(pages)}pages"


def temporary_sibling(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_path = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    os.close(descriptor)
    return Path(raw_path)


def write_bytes_atomic(path: Path, payload: bytes) -> None:
    temporary = temporary_sibling(path)
    try:
        temporary.write_bytes(payload)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    write_bytes_atomic(
        path,
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )


def clip_rect(page: object, crop: tuple[float, float, float, float] | None) -> object:
    import pymupdf

    page_rect = page.rect
    if crop is None:
        return page_rect
    left, top, right, bottom = crop
    return pymupdf.Rect(
        page_rect.x0 + left * page_rect.width,
        page_rect.y0 + top * page_rect.height,
        page_rect.x0 + right * page_rect.width,
        page_rect.y0 + bottom * page_rect.height,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Extract selected PDF pages or normalized page regions for visual analysis, "
            "OCR and temporary reference."
        )
    )
    parser.add_argument("input", type=Path, help="source PDF file")
    parser.add_argument(
        "--pages",
        default="1",
        help="one-based pages such as 2,5-7, or 'all' (default: 1)",
    )
    parser.add_argument(
        "--crop",
        nargs=4,
        type=float,
        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"),
        help="normalized crop rectangle using a top-left origin and values from 0 to 1",
    )
    parser.add_argument(
        "--format",
        choices=("pdf", "png", "both"),
        default="both",
        help="output type (default: both)",
    )
    parser.add_argument(
        "--dpi",
        type=positive_int,
        default=180,
        help="PNG rendering resolution (default: 180)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="output directory; defaults under var/temp/pdf-extracts/",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="allow replacement of existing extraction files",
    )
    parser.add_argument("--version", action="version", version=TOOL_VERSION)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    configure_utf8_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        input_path = args.input.expanduser().resolve()
        if not input_path.is_file():
            raise PdfExtractError(f"input PDF does not exist: {args.input}")
        if input_path.suffix.casefold() != ".pdf":
            raise PdfExtractError("input file must use a .pdf suffix")
        crop = validate_crop(args.crop)

        import pymupdf

        document = pymupdf.open(input_path)
        try:
            if document.needs_pass:
                raise PdfExtractError("encrypted PDF requires a password and cannot be opened")
            pages = parse_pages(args.pages, document.page_count)
            stem = safe_filename_part(input_path.stem)
            suffix = "-crop" if crop is not None else ""
            tag = page_tag(pages)
            output_dir = (
                args.output_dir.expanduser().resolve()
                if args.output_dir is not None
                else (DEFAULT_OUTPUT_ROOT / stem).resolve()
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            pdf_path = output_dir / f"{stem}-pages-{tag}{suffix}.pdf"
            png_paths = [
                output_dir / f"{stem}-page-{page_number:03d}{suffix}.png"
                for page_number in pages
            ]
            report_path = output_dir / f"{stem}-pages-{tag}{suffix}-capture-report.json"
            destinations = [report_path]
            if args.format in {"pdf", "both"}:
                destinations.append(pdf_path)
            if args.format in {"png", "both"}:
                destinations.extend(png_paths)
            for destination in destinations:
                if destination.resolve() == input_path:
                    raise PdfExtractError("output must not overwrite the source PDF")
                if destination.exists() and not args.overwrite:
                    raise PdfExtractError(
                        f"output already exists: {display_path(destination)}; pass --overwrite explicitly"
                    )

            outputs: list[dict[str, object]] = []
            if args.format in {"pdf", "both"}:
                extracted = pymupdf.open()
                try:
                    for page_number in pages:
                        source_page = document[page_number - 1]
                        clip = clip_rect(source_page, crop)
                        target_page = extracted.new_page(width=clip.width, height=clip.height)
                        target_page.show_pdf_page(
                            target_page.rect,
                            document,
                            page_number - 1,
                            clip=clip,
                        )
                    write_bytes_atomic(
                        pdf_path,
                        extracted.tobytes(garbage=4, deflate=True),
                    )
                finally:
                    extracted.close()
                outputs.append(
                    {"file": display_path(pdf_path), "kind": "pdf", "exists": pdf_path.is_file()}
                )

            if args.format in {"png", "both"}:
                scale = args.dpi / 72
                matrix = pymupdf.Matrix(scale, scale)
                for page_number, png_path in zip(pages, png_paths, strict=True):
                    source_page = document[page_number - 1]
                    clip = clip_rect(source_page, crop)
                    pixmap = source_page.get_pixmap(matrix=matrix, clip=clip, alpha=False)
                    write_bytes_atomic(png_path, pixmap.tobytes("png"))
                    outputs.append(
                        {
                            "file": display_path(png_path),
                            "kind": "png",
                            "page": page_number,
                            "width_pixels": pixmap.width,
                            "height_pixels": pixmap.height,
                            "exists": png_path.is_file(),
                        }
                    )

            report: dict[str, object] = {
                "tool": "tools/extract-pdf-pages.py",
                "tool_version": TOOL_VERSION,
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "input": {"file": display_path(input_path), "exists": input_path.is_file()},
                "page_count": document.page_count,
                "selected_pages": pages,
                "crop": list(crop) if crop is not None else None,
                "dpi": args.dpi if args.format in {"png", "both"} else None,
                "outputs": outputs,
            }
            write_json_atomic(report_path, report)
        finally:
            document.close()

        print(
            json.dumps(
                {
                    "status": "ok",
                    "output_directory": display_path(output_dir),
                    "report": display_path(report_path),
                    "outputs": len(outputs),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except PdfExtractError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc.__class__.__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
