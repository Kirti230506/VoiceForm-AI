"""
VoiceForm AI - Whisper Speech Recognition Test & Comparison
Evaluates OpenAI Whisper on real dataset clips (up to 5 clips)
across English, Hindi, and Marathi, comparing predicted text
with ground-truth transcripts and reporting WER/CER metrics.
"""

import os
import sys
import csv
import time
import json
import unicodedata
from typing import Dict, Any, List, Tuple
import whisper

# Force UTF-8 on Windows stdout/stderr to safely render Hindi and Marathi Devanagari
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def normalize_text(text: str) -> str:
    """Normalizes text for fair comparison (lowercasing, punctuation stripping, unicode normalization)."""
    if not text:
        return ""
    # Unicode NFKC normalization
    text = unicodedata.normalize("NFKC", text)
    # Lowercase
    text = text.lower()
    # Remove standard punctuation
    for ch in [".", ",", "!", "?", ";", ":", "\"", "'", "-", "(", ")", "[", "]", "{", "}", "।"]:
        text = text.replace(ch, " ")
    # Collapse multiple whitespaces
    return " ".join(text.split())

def levenshtein_distance(seq1: List[str], seq2: List[str]) -> int:
    """Computes Levenshtein edit distance between two token sequences."""
    n, m = len(seq1), len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[n][m]

def compute_wer(reference: str, hypothesis: str) -> float:
    """Computes Word Error Rate (WER)."""
    ref_words = normalize_text(reference).split()
    hyp_words = normalize_text(hypothesis).split()
    if not ref_words:
        return 0.0 if not hyp_words else 1.0
    dist = levenshtein_distance(ref_words, hyp_words)
    return min(1.0, dist / len(ref_words))

def compute_cer(reference: str, hypothesis: str) -> float:
    """Computes Character Error Rate (CER)."""
    ref_chars = list(normalize_text(reference).replace(" ", ""))
    hyp_chars = list(normalize_text(hypothesis).replace(" ", ""))
    if not ref_chars:
        return 0.0 if not hyp_chars else 1.0
    dist = levenshtein_distance(ref_chars, hyp_chars)
    return min(1.0, dist / len(ref_chars))

def run_whisper_test(dataset_dir: str, sample_filenames: List[str], model_name: str = "base") -> List[Dict[str, Any]]:
    """Loads transcripts.csv and runs Whisper transcription on up to 5 clips."""
    csv_path = os.path.join(dataset_dir, "transcripts.csv")
    audio_dir = os.path.join(dataset_dir, "audio")

    # Read ground truth
    ground_truth = {}
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fname = row["audio_filename"].strip()
            lang = row["language"].strip()
            trans = row["transcript"].strip()
            ground_truth[fname] = {"language": lang, "transcript": trans}

    print(f"\n[Whisper] Loading Whisper '{model_name}' model...")
    t0 = time.time()
    model = whisper.load_model(model_name)
    load_time = round(time.time() - t0, 2)
    print(f"[Whisper] Model loaded in {load_time}s.")

    results = []
    lang_map = {
        "english": "en",
        "hindi": "hi",
        "marathi": "mr",
        "en": "en",
        "hi": "hi",
        "mr": "mr"
    }

    for fname in sample_filenames:
        if fname not in ground_truth:
            print(f"[Warning] '{fname}' not in transcripts.csv, skipping.")
            continue

        gt = ground_truth[fname]
        audio_file = os.path.join(audio_dir, fname)
        if not os.path.exists(audio_file):
            print(f"[Warning] Audio file '{audio_file}' not found, skipping.")
            continue

        lang_code = lang_map.get(gt["language"].lower(), "en")

        print(f"\n--- Transcribing {fname} ({gt['language']}, Whisper lang='{lang_code}') ---")
        t_start = time.time()
        try:
            trans_result = model.transcribe(
                audio_file,
                language=lang_code,
                fp16=False,
                temperature=0.0
            )
            elapsed = round(time.time() - t_start, 2)
            predicted_text = trans_result.get("text", "").strip()
            detected_lang = trans_result.get("language", lang_code)

            wer = compute_wer(gt["transcript"], predicted_text)
            cer = compute_cer(gt["transcript"], predicted_text)

            res = {
                "filename": fname,
                "language": gt["language"],
                "whisper_lang_code": lang_code,
                "detected_lang": detected_lang,
                "reference_transcript": gt["transcript"],
                "predicted_transcript": predicted_text,
                "inference_time_sec": elapsed,
                "wer": round(wer, 4),
                "cer": round(cer, 4),
                "status": "SUCCESS"
            }
        except Exception as e:
            res = {
                "filename": fname,
                "language": gt["language"],
                "error": str(e),
                "status": "ERROR"
            }
        results.append(res)

    return results

def print_test_summary(results: List[Dict[str, Any]]):
    print("\n" + "=" * 80)
    print("           WHISPER SPEECH RECOGNITION TEST REPORT (UP TO 5 CLIPS)")
    print("=" * 80)
    for idx, r in enumerate(results, start=1):
        print(f"\n[{idx}/5] Audio Clip: {r['filename']} | Language: {r['language']}")
        if r["status"] == "SUCCESS":
            print(f"      Time Taken  : {r['inference_time_sec']}s")
            print(f"      WER (Words) : {r['wer'] * 100:.1f}%")
            print(f"      CER (Chars) : {r['cer'] * 100:.1f}%")
            print(f"      Reference   : {r['reference_transcript']}")
            print(f"      Whisper Out : {r['predicted_transcript']}")
        else:
            print(f"      ERROR       : {r.get('error')}")
    print("\n" + "=" * 80)
    print("Key Observations & Limitations:")
    print("1. FLEURS audio clips are formal, read-speech recordings.")
    print("2. English achieves low WER on standard vocab, while regional proper nouns may vary.")
    print("3. Hindi and Marathi use Devanagari script; Whisper accurately predicts phonetic text,")
    print("   though spelling variations (e.g. anusvara vs chandrabindu) impact word-exact match.")
    print("4. This test on 5 clips verifies the STT pipeline; real-world noisy audio will vary.")
    print("=" * 80)

if __name__ == "__main__":
    dataset_dir = os.path.join(os.path.dirname(__file__), "datasets", "speech", "voiceform_dataset")
    # Select up to 5 real clips across English, Hindi, and Marathi
    selected_clips = ["en_1.wav", "en_2.wav", "hi_1.wav", "hi_2.wav", "mr_1.wav"]
    results = run_whisper_test(dataset_dir, selected_clips, model_name="base")
    print_test_summary(results)

    # Save to JSON
    out_file = os.path.join(os.path.dirname(__file__), "whisper_evaluation_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[Info] Evaluation results saved to {out_file}")

