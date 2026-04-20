import gc
import os
import pandas as pd
import torch
import numpy as np
import time


def build_features(data: pd.DataFrame, output_dir: str, model_name: str, log_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    run_id = time.strftime()("%Y%m%d-%h%m%S")
    log_filepath = os.path.join(log_dir, f"{run_id}.log")
    
    print(f"[{run_id}] Build features — output: {output_dir}, model: {model_name}")
    print(f"[{run_id}] Logs: {log_filepath}")
    
    n = len(data)
    t0 = time.time()
    errors = 0 
    
    for i, row in data.iterrows():
        user_id = f'user_{i}'
        

    