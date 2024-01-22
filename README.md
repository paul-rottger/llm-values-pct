Brief explanation of the main experimental pipeline

### 1. Generate Prompts
Manually edit and run `generate_prompts.py` in /src/ to generate prompts for the model to complete. The prompts are saved in /data/prompts/.

### 2. Generate Completions
Run the bash scripts in /bash/ to generate completions for the prompts. The completions are saved in /data/completions/EXPERIMENT_NAME.

### 3. Analyse Completions
Run the notebooks in /notebooks/ to analyse the completions.