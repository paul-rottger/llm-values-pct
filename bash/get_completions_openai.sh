#!/bin/sh

REPO=$(git rev-parse --show-toplevel)

source $REPO/env/bin/activate

python ../src/2_get_completions_openai.py \
    --gen_model "gpt-4-0613" \
    --input_path $REPO/data/prompts/jailbreak_experiments_180124.csv \
    --input_col "full_prompt" \
    --caching_path $REPO/data/cache \
    --output_path $REPO/data/completions/jailbreak_experiments_180124/gpt-4-0613.csv \
    --n_batches 1 \
    --start_batch 0 \
    --max_workers 3 \
    --n_samples 0