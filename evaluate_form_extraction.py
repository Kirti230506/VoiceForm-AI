"""
VoiceForm AI - Form Information Extraction Evaluation Pipeline
Evaluates the NLP/NER extraction engine on held-out test splits.
Computes field-level Precision, Recall, and F1 score without data leakage.
"""

import os
import sys
import json
from typing import Dict, Any, List

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend to sys.path so we can import app modules directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
from app.services.nlp_engine import extract_all_entities

DATASET_FILE = os.path.join(
    os.path.dirname(__file__), "datasets", "form_extraction", "form_extraction_dataset.json"
)

EVALUATED_FIELDS = [
    "full_name",
    "age",
    "gender",
    "education",
    "phone",
    "aadhaar",
    "occupation",
    "annual_income",
    "district",
    "state",
    "social_category"
]

def values_match(field: str, expected: Any, predicted: Any) -> bool:
    """Checks if predicted value matches expected ground-truth."""
    if expected is None and predicted is None:
        return True
    if expected is None or predicted is None:
        return False

    exp_str = str(expected).strip().lower()
    pred_str = str(predicted).strip().lower()

    if field in ["age", "annual_income"]:
        try:
            return float(expected) == float(predicted)
        except (ValueError, TypeError):
            return exp_str == pred_str

    if field in ["phone", "aadhaar"]:
        clean_exp = "".join(filter(str.isdigit, str(expected)))
        clean_pred = "".join(filter(str.isdigit, str(predicted)))
        return clean_exp == clean_pred

    # Substring / fuzzy match for categorized values (e.g. Farmer in Farmer / Shetkari / Kisan)
    if exp_str == pred_str:
        return True
    if exp_str in pred_str or pred_str in exp_str:
        return True

    return False

def evaluate_form_extraction(split: str = "test") -> Dict[str, Any]:
    if not os.path.exists(DATASET_FILE):
        raise FileNotFoundError(f"Dataset file not found: {DATASET_FILE}")

    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        samples = json.load(f)

    eval_samples = [s for s in samples if s.get("split") == split]
    if not eval_samples:
        print(f"[Warning] No samples found for split '{split}'. Using all samples.")
        eval_samples = samples

    field_metrics = {
        f: {"tp": 0, "fp": 0, "fn": 0, "tn": 0} for f in EVALUATED_FIELDS
    }

    detailed_results = []

    for s in eval_samples:
        text = s["text"]
        gt = s["ground_truth"]
        res = extract_all_entities(text)
        pred_struct = res.get("structured_fields", {})

        sample_detail = {
            "id": s["id"],
            "language": s["language"],
            "text": text,
            "fields_compared": {}
        }

        for f in EVALUATED_FIELDS:
            expected = gt.get(f)
            predicted = pred_struct.get(f)

            has_expected = expected is not None
            has_predicted = predicted is not None

            if has_expected and has_predicted:
                if values_match(f, expected, predicted):
                    field_metrics[f]["tp"] += 1
                    status = "TP (Correct)"
                else:
                    field_metrics[f]["fp"] += 1
                    field_metrics[f]["fn"] += 1
                    status = "FP_FN (Mismatch)"
            elif has_expected and not has_predicted:
                field_metrics[f]["fn"] += 1
                status = "FN (Missed)"
            elif not has_expected and has_predicted:
                field_metrics[f]["fp"] += 1
                status = "FP (Spurious)"
            else:
                field_metrics[f]["tn"] += 1
                status = "TN (Correctly Null)"

            sample_detail["fields_compared"][f] = {
                "expected": expected,
                "predicted": predicted,
                "status": status
            }

        detailed_results.append(sample_detail)

    # Compute Precision, Recall, F1
    summary = {}
    total_tp, total_fp, total_fn = 0, 0, 0

    for f, counts in field_metrics.items():
        tp = counts["tp"]
        fp = counts["fp"]
        fn = counts["fn"]

        prec = tp / (tp + fp) if (tp + fp) > 0 else (1.0 if fn == 0 else 0.0)
        rec = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        summary[f] = {
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "tp": tp,
            "fp": fp,
            "fn": fn
        }

        total_tp += tp
        total_fp += fp
        total_fn += fn

    micro_prec = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    micro_rec = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    micro_f1 = (2 * micro_prec * micro_rec) / (micro_prec + micro_rec) if (micro_prec + micro_rec) > 0 else 0.0

    return {
        "split_evaluated": split,
        "total_test_samples": len(eval_samples),
        "overall_micro_metrics": {
            "precision": round(micro_prec, 4),
            "recall": round(micro_rec, 4),
            "f1": round(micro_f1, 4)
        },
        "field_summary": summary,
        "sample_details": detailed_results
    }

def print_evaluation_report(results: Dict[str, Any]):
    print("\n" + "=" * 80)
    print(f"       VOICEFORM AI - FORM EXTRACTION EVALUATION REPORT (Split: {results['split_evaluated'].upper()})")
    print("=" * 80)
    print(f"Total Held-Out Test Samples : {results['total_test_samples']}")
    micro = results["overall_micro_metrics"]
    print(f"Overall Micro Precision     : {micro['precision'] * 100:.1f}%")
    print(f"Overall Micro Recall        : {micro['recall'] * 100:.1f}%")
    print(f"Overall Micro F1 Score      : {micro['f1'] * 100:.1f}%")
    print("-" * 80)
    print(f"{'Field':<18} | {'Precision':<10} | {'Recall':<10} | {'F1 Score':<10} | TP / FP / FN")
    print("-" * 80)
    for f, metrics in results["field_summary"].items():
        counts = f"{metrics['tp']} / {metrics['fp']} / {metrics['fn']}"
        print(f"{f:<18} | {metrics['precision']*100:>8.1f}% | {metrics['recall']*100:>8.1f}% | {metrics['f1']*100:>8.1f}% | {counts}")
    print("=" * 80)

if __name__ == "__main__":
    split_to_use = "test"
    if len(sys.argv) > 1:
        split_to_use = sys.argv[1]

    results = evaluate_form_extraction(split=split_to_use)
    print_evaluation_report(results)

    # Save to JSON
    out_file = os.path.join(os.path.dirname(__file__), "form_extraction_evaluation_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[Info] Results saved to {out_file}")
