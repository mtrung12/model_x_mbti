import os
import pandas as pd
import time

from baselines.prompt import *
from utils.gpt_client import gpt_call
from utils.hf_client import hf_call
from utils.log import log_to_file
from utils.parser import extract_result

def predict_text(text: str, 
            model_name: str, 
            usr_prompt: str, 
            max_new_tokens: int, 
            record_idx: int,
            log_filepath: str,
            temperature: float,
    ):
    formatted_prompt = usr_prompt.replace("<text>", text)
    if model_name.startswith('gpt'):
        output = gpt_call(formatted_prompt, SYS_PROMPT, model_name, max_new_tokens, temperature)
        log_to_file(log_filepath, SYS_PROMPT, formatted_prompt, output, record_idx)
    else:
        output = hf_call(formatted_prompt, SYS_PROMPT, model_name, max_new_tokens, temperature)
        log_to_file(log_filepath, SYS_PROMPT, formatted_prompt, output, record_idx)

    return output

def predict(text_df: pd.DataFrame, 
            model_name: str, 
            log_dir: str, 
            prompt_mode: str, # cot, zeroshot, oneshot
            max_new_tokens: int, 
            res_dir: str,
            temperature: float,
            example_df: pd.DataFrame = None,
):
    run_id = time.strftime("%Y%m%d-%H%M%S")
    log_filepath = os.path.join(log_dir, f'{model_name}/{prompt_mode}/{run_id}_log.txt')
    res_dir = os.path.join(res_dir, f'{model_name}/{prompt_mode}/{run_id}')
    os.makedirs(res_dir, exist_ok=True)
    usr_prompt = None
    if prompt_mode == 'zeroshot':
        usr_prompt = ZEROSHOT_USR_PROMPT
    elif prompt_mode == 'oneshot':
        usr_prompt = ONESHOT_USR_PROMPT
        random_index = example_df.sample(n=1).index[0]
        usr_prompt = usr_prompt.format(
            example_text=example_df.loc[random_index, 'posts'],
            example_EI=example_df.loc[random_index, 'IE'],
            example_SN=example_df.loc[random_index, 'NS'],
            example_TF=example_df.loc[random_index, 'TF'],
            example_JP=example_df.loc[random_index, 'JP']
        )
    elif prompt_mode == 'cot':
        usr_prompt = COT_USR_PROMPT
    else:
        raise ValueError(f'Unknown prompt_mode: {prompt_mode}. Choose one of the following prompt modes: cot, zeroshot, oneshot')
    
    n = len(text_df)
    print(f"Loaded {n} records for evaluation using {prompt_mode} and {model_name}.")
    
    t0 = time.time()
    pred_types = []
    pred_IE = []
    pred_NS = []
    pred_TF = []
    pred_JP = []
    for idx, row in text_df.iterrows():
        text = row['posts']
        output = predict_text(text, model_name, usr_prompt, max_new_tokens, idx, log_filepath, temperature)
        mbti = extract_result(output)
        pred_types.append(mbti)
        pred_IE.append(mbti[0])
        pred_NS.append(mbti[1])
        pred_TF.append(mbti[2])
        pred_JP.append(mbti[3])
        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{n} records.")

    t1 = time.time()
    print(f"Evaluation completed in {t1 - t0:.2f} seconds.")
    df = text_df.copy()
    df["pred_type"] = pred_types
    df["pred_IE"] = pred_IE
    df["pred_NS"] = pred_NS
    df["pred_TF"] = pred_TF
    df["pred_JP"] = pred_JP
    prediction_filepath = os.path.join(res_dir, 'predictions.csv')
    # Save to a new path
    df.to_csv(prediction_filepath, index=False)
    print(f"Predictions are saved to {prediction_filepath}")
    
    return run_id, t1 - t0, prediction_filepath 
