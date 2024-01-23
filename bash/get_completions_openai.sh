#!/bin/sh

REPO=$(git rev-parse --show-toplevel)

source $REPO/env/bin/activate

EXPERIMENT="implicit_paraphrase_experiments_230124"
MODEL_NAME="gpt-3.5-turbo-1106"

python ../src/2_get_completions_openai.py \
    --gen_model $MODEL_NAME \
    --input_path $REPO/data/prompts/$EXPERIMENT.csv \
    --input_col "full_prompt" \
    --caching_path $REPO/data/cache \
    --output_path $REPO/data/completions/$EXPERIMENT/$MODEL_NAME.csv \
    --n_batches 1 \
    --start_batch 0 \
    --max_workers 3 \
    --n_samples 0