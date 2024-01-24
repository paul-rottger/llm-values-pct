#!/bin/sh

#SBATCH --job-name=explicit_paraphrase_experiments_240124
#SBATCH --time=01:00:00
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --mem=64000MB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --account=rottger
#SBATCH --output=./logs/slurm-%A.out

# activate conda environment
source /home/Rottger/.bashrc
conda activate llmvalues-env

# check python version
python3 --version

# to surpress annoyingly verbose warning
export TOKENIZERS_PARALLELISM=true

# store repo path
REPO=$(git rev-parse --show-toplevel)

# set params
PROVIDER="meta-llama"
MODEL_NAME="Llama-2-13b-chat-hf"
EXPERIMENT="explicit_paraphrase_experiments_240124"

python $REPO/src/2_get_completions_simplegen.py \
    --model_name_or_path $PROVIDER/$MODEL_NAME \
    --test_data_input_path $REPO/data/prompts/$EXPERIMENT.csv \
    --n_test_samples 0 \
    --batch_size 8 \
    --input_col "full_prompt" \
    --test_data_output_path $REPO/data/completions/$EXPERIMENT/$MODEL_NAME.csv \
    --load_in_8bit False \
    --log_level "debug" \
