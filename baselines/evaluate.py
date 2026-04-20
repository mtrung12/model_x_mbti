import os
from typing import Dict

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

from utils.log import write_classification_report


def build_report_df(y_true, y_pred) -> pd.DataFrame:
    report_dict = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    return pd.DataFrame(report_dict).transpose()


def evaluate(
    prediction_csv: str,
    model_name: str,
    run_time: float,
    prompt_mode: str,
    res_dir: str,
    run_id: str,
    vector_db_dir: str = None,
) -> Dict[str, object]:
    df = pd.read_csv(prediction_csv)
    trait_cols = ["IE", "NS", "TF", "JP"]
    required_cols = trait_cols + [f"pred_{trait}" for trait in trait_cols]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Missing required columns in {prediction_csv}: {', '.join(missing_cols)}"
        )

    n_records = len(df)
    pred_cols = [f"pred_{trait}" for trait in trait_cols]
    normalized_pred_df = df[pred_cols].apply(
        lambda col: col.astype("string").str.strip()
    )
    fail_mask = normalized_pred_df.isna().any(axis=1) | normalized_pred_df.eq("").any(axis=1)
    fail_count = int(fail_mask.sum())

    summary_rows = []
    report_paths = {}

    for trait in trait_cols:
        valid_df = df[[trait, f"pred_{trait}"]].dropna().copy()
        valid_df[trait] = valid_df[trait].astype(str).str.strip()
        valid_df[f"pred_{trait}"] = valid_df[f"pred_{trait}"].astype(str).str.strip()
        valid_df = valid_df[valid_df[f"pred_{trait}"] != ""]

        y_true = valid_df[trait]
        y_pred = valid_df[f"pred_{trait}"]
        accuracy = accuracy_score(y_true, y_pred) if len(valid_df) > 0 else 0.0
        report_df = build_report_df(y_true, y_pred) if len(valid_df) > 0 else pd.DataFrame()

        report_path = os.path.join(res_dir, f"{model_name}/{prompt_mode}/{run_id}/{trait}_classification_report.txt")
        write_classification_report(
            report_path=report_path,
            save_df=report_df,
            model_name=model_name,
            test_csv=prediction_csv,
            n_records=n_records,
            fail_count=fail_count,
            prompt_mode=prompt_mode,
            vector_db_dir=vector_db_dir or "N/A",
            time=run_time,
        )
        report_paths[trait] = report_path

        summary_rows.append(
            {
                "trait": trait,
                "n_samples": len(valid_df),
                "accuracy": accuracy,
                "macro_precision": report_df.loc["macro avg", "precision"]
                if "macro avg" in report_df.index
                else None,
                "macro_recall": report_df.loc["macro avg", "recall"]
                if "macro avg" in report_df.index
                else None,
                "macro_f1": report_df.loc["macro avg", "f1-score"]
                if "macro avg" in report_df.index
                else None,
                "weighted_precision": report_df.loc["weighted avg", "precision"]
                if "weighted avg" in report_df.index
                else None,
                "weighted_recall": report_df.loc["weighted avg", "recall"]
                if "weighted avg" in report_df.index
                else None,
                "weighted_f1": report_df.loc["weighted avg", "f1-score"]
                if "weighted avg" in report_df.index
                else None,
            }
        )

    summary_df = pd.DataFrame(summary_rows)
    summary_path = os.path.join(res_dir, f"{model_name}/{prompt_mode}/{run_id}/evaluation_summary.csv")
    summary_df.to_csv(summary_path, index=False)

    print(f"Loaded predictions from {prediction_csv}")
    print(f"Saved evaluation summary to {summary_path}")
    for trait, report_path in report_paths.items():
        print(f"Saved {trait} report to {report_path}")

    return {
        "summary_csv": summary_path,
        "report_paths": report_paths,
        "n_records": n_records,
        "fail_count": fail_count,
    }
