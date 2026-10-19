"""
VoiceForm AI - Dataset Validation Script
Validates the multilingual speech dataset (English, Hindi, Marathi).
Checks CSV structure, columns, audio file readability, formats, and matches.
"""

import os
import csv
import sys
import wave
import json
from typing import Dict, Any, List, Optional

SUPPORTED_LANGUAGES = {"english", "hindi", "marathi", "en", "hi", "mr"}
POSSIBLE_DATASET_PATHS = [
    os.path.join(os.path.dirname(__file__), "datasets", "speech", "voiceform_dataset"),
    os.path.join(os.path.dirname(__file__), "datasets", "speech"),
    os.path.join(os.path.dirname(__file__), "datasets"),
]

def find_dataset_dir() -> Optional[str]:
    """Locate the actual speech dataset directory containing transcripts.csv."""
    for path in POSSIBLE_DATASET_PATHS:
        csv_file = os.path.join(path, "transcripts.csv")
        if os.path.exists(csv_file):
            return path
    return None

def validate_audio_file(audio_path: str) -> Dict[str, Any]:
    """Validates audio file readability, format, channels, sample rate, and duration using standard wave module."""
    if not os.path.exists(audio_path):
        return {"readable": False, "error": "File does not exist"}
    
    file_size = os.path.getsize(audio_path)
    if file_size == 0:
        return {"readable": False, "error": "Audio file is 0 bytes (empty)"}
    
    try:
        with wave.open(audio_path, "rb") as wf:
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            duration = n_frames / float(framerate) if framerate > 0 else 0
            
            return {
                "readable": True,
                "channels": channels,
                "sample_width_bytes": sample_width,
                "sample_rate_hz": framerate,
                "duration_seconds": round(duration, 2),
                "file_size_bytes": file_size,
                "format": "WAV"
            }
    except wave.Error as e:
        return {"readable": False, "error": f"Invalid or non-PCM WAV format: {str(e)}"}
    except Exception as e:
        return {"readable": False, "error": f"Read error: {str(e)}"}

def validate_dataset(dataset_dir: Optional[str] = None, max_audio_checks: Optional[int] = 5) -> Dict[str, Any]:
    """
    Performs full dataset validation.
    If max_audio_checks is provided, checks up to that number of audio files (e.g. 5 for initial check).
    """
    report = {
        "dataset_found": False,
        "dataset_path": None,
        "csv_exists": False,
        "csv_path": None,
        "columns_found": [],
        "expected_columns": ["audio_filename", "language", "transcript"],
        "columns_valid": False,
        "total_rows": 0,
        "languages_count": {},
        "audio_folder_exists": False,
        "audio_folder_path": None,
        "audio_files_found_on_disk": 0,
        "tested_audio_samples": [],
        "missing_audio_files": [],
        "empty_transcripts": [],
        "duplicate_filenames": [],
        "duplicate_transcripts": [],
        "unsupported_languages": [],
        "orphaned_audio_files": [],
        "errors": [],
        "warnings": [],
        "status": "FAILED"
    }

    # 1. Locate dataset
    target_dir = dataset_dir or find_dataset_dir()
    if not target_dir or not os.path.exists(target_dir):
        report["errors"].append(f"Speech dataset not found. Checked: {POSSIBLE_DATASET_PATHS}")
        return report

    report["dataset_found"] = True
    report["dataset_path"] = target_dir

    # 2. Check transcripts.csv
    csv_path = os.path.join(target_dir, "transcripts.csv")
    if not os.path.exists(csv_path):
        report["errors"].append(f"transcripts.csv missing at: {csv_path}")
        return report

    report["csv_exists"] = True
    report["csv_path"] = csv_path

    # 3. Check audio folder
    audio_dir = os.path.join(target_dir, "audio")
    if os.path.exists(audio_dir) and os.path.isdir(audio_dir):
        report["audio_folder_exists"] = True
        report["audio_folder_path"] = audio_dir
        audio_files_disk = set(os.listdir(audio_dir))
        report["audio_files_found_on_disk"] = len(audio_files_disk)
    else:
        report["audio_folder_exists"] = False
        report["warnings"].append(f"No dedicated 'audio' subdirectory at: {audio_dir}. Audio files may be in root.")
        audio_dir = target_dir
        audio_files_disk = set(os.listdir(target_dir))

    # 4. Read & validate CSV
    rows = []
    seen_filenames = set()
    seen_transcripts = set()
    referenced_filenames = set()

    try:
        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            columns = [c.strip() for c in (reader.fieldnames or [])]
            report["columns_found"] = columns
            
            # Check required columns
            missing_cols = [c for c in report["expected_columns"] if c not in columns]
            if missing_cols:
                report["errors"].append(f"Missing required CSV columns: {missing_cols}. Found: {columns}")
                report["columns_valid"] = False
            else:
                report["columns_valid"] = True

            for row_idx, row in enumerate(reader, start=1):
                report["total_rows"] += 1
                fname = (row.get("audio_filename") or "").strip()
                lang = (row.get("language") or "").strip()
                transcript = (row.get("transcript") or "").strip()

                referenced_filenames.add(fname)

                # Check duplicates
                if fname in seen_filenames:
                    report["duplicate_filenames"].append({"row": row_idx, "filename": fname})
                else:
                    seen_filenames.add(fname)

                if transcript and transcript in seen_transcripts:
                    report["duplicate_transcripts"].append({"row": row_idx, "filename": fname, "transcript": transcript[:40] + "..."})
                else:
                    if transcript:
                        seen_transcripts.add(transcript)

                # Check empty transcripts
                if not transcript:
                    report["empty_transcripts"].append({"row": row_idx, "filename": fname})

                # Check language
                lang_clean = lang.lower()
                if lang_clean not in SUPPORTED_LANGUAGES:
                    report["unsupported_languages"].append({"row": row_idx, "filename": fname, "language": lang})
                else:
                    report["languages_count"][lang] = report["languages_count"].get(lang, 0) + 1

                # Check file existence on disk
                audio_path = os.path.join(audio_dir, fname)
                if not os.path.exists(audio_path):
                    # Also try target_dir if audio/ was used
                    alt_path = os.path.join(target_dir, fname)
                    if os.path.exists(alt_path):
                        audio_path = alt_path
                    else:
                        report["missing_audio_files"].append({"row": row_idx, "filename": fname, "expected_path": audio_path})

                rows.append({
                    "row_idx": row_idx,
                    "filename": fname,
                    "language": lang,
                    "transcript": transcript,
                    "audio_path": audio_path
                })

    except Exception as e:
        report["errors"].append(f"Failed to read CSV: {str(e)}")
        return report

    # 5. Check orphaned audio files on disk (audio files not mentioned in CSV)
    wav_files_disk = {f for f in audio_files_disk if f.lower().endswith((".wav", ".mp3", ".m4a", ".flac", ".ogg"))}
    orphaned = wav_files_disk - referenced_filenames
    if orphaned:
        report["orphaned_audio_files"] = sorted(list(orphaned))

    # 6. Test audio readability on samples (up to max_audio_checks)
    sample_rows = rows[:max_audio_checks] if max_audio_checks else rows
    for r in sample_rows:
        val_res = validate_audio_file(r["audio_path"])
        sample_info = {
            "row": r["row_idx"],
            "filename": r["filename"],
            "language": r["language"],
            "transcript_preview": (r["transcript"][:60] + "...") if len(r["transcript"]) > 60 else r["transcript"],
            **val_res
        }
        report["tested_audio_samples"].append(sample_info)
        if not val_res.get("readable"):
            report["errors"].append(f"Audio file '{r['filename']}' unreadable: {val_res.get('error')}")

    # Determine final status
    if not report["errors"] and report["columns_valid"] and len(report["missing_audio_files"]) == 0:
        report["status"] = "PASSED"
    elif len(report["errors"]) == 0 and len(report["missing_audio_files"]) == 0:
        report["status"] = "PASSED_WITH_WARNINGS"
    else:
        report["status"] = "FAILED"

    return report

def format_report_text(report: Dict[str, Any]) -> str:
    """Generates human-readable console and log report."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  VOICEFORM AI - DATASET VALIDATION REPORT [{report['status']}]")
    lines.append("=" * 70)
    lines.append(f"Dataset Location : {report['dataset_path']}")
    lines.append(f"CSV Path         : {report['csv_path']}")
    lines.append(f"CSV Columns      : {', '.join(report['columns_found'])} (Valid: {report['columns_valid']})")
    lines.append(f"Audio Folder     : {report['audio_folder_path']} (Files on disk: {report['audio_files_found_on_disk']})")
    lines.append(f"Total Rows       : {report['total_rows']}")
    lines.append("-" * 70)
    lines.append("Records per Language:")
    for lang, count in report["languages_count"].items():
        lines.append(f"  - {lang}: {count} clips")
    lines.append("-" * 70)
    lines.append(f"Audio Samples Tested (Initial Test: {len(report['tested_audio_samples'])} clips):")
    for s in report["tested_audio_samples"]:
        read_status = "OK" if s.get("readable") else f"FAILED ({s.get('error')})"
        dur = f"{s.get('duration_seconds', 0)}s" if s.get("readable") else "N/A"
        sr = f"{s.get('sample_rate_hz', 0)} Hz" if s.get("readable") else "N/A"
        ch = f"{s.get('channels', 0)} ch" if s.get("readable") else "N/A"
        lines.append(f"  [{read_status}] {s['filename']:<12} | Lang: {s['language']:<8} | Dur: {dur:<7} | {sr} {ch}")
        lines.append(f"         Transcript: \"{s['transcript_preview']}\"")
    
    if report["missing_audio_files"]:
        lines.append("-" * 70)
        lines.append(f"Missing Audio Files ({len(report['missing_audio_files'])}):")
        for m in report["missing_audio_files"]:
            lines.append(f"  - Row {m['row']}: {m['filename']}")

    if report["empty_transcripts"]:
        lines.append(f"Empty Transcripts: {len(report['empty_transcripts'])}")
    if report["duplicate_filenames"]:
        lines.append(f"Duplicate Filenames: {len(report['duplicate_filenames'])}")
    if report["duplicate_transcripts"]:
        lines.append(f"Duplicate Transcripts: {len(report['duplicate_transcripts'])}")
    if report["orphaned_audio_files"]:
        lines.append(f"Orphaned Audio Files (not in CSV): {report['orphaned_audio_files']}")
    if report["errors"]:
        lines.append("-" * 70)
        lines.append("Errors:")
        for err in report["errors"]:
            lines.append(f"  ❌ {err}")
    if report["warnings"]:
        lines.append("-" * 70)
        lines.append("Warnings:")
        for warn in report["warnings"]:
            lines.append(f"  ⚠️ {warn}")

    lines.append("=" * 70)
    return "\n".join(lines)

if __name__ == "__main__":
    max_clips = 5
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        max_clips = int(sys.argv[1])
    elif "--all" in sys.argv:
        max_clips = None

    rep = validate_dataset(max_audio_checks=max_clips)
    print(format_report_text(rep))
    if rep["status"] == "FAILED":
        sys.exit(1)
    sys.exit(0)
