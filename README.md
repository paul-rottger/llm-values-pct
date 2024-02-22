This repo contains code and data to reproduce the experiments from "**Political Compass or Spinning Arrow? Towards More Meaningful Evaluations for Values and Opinions in Large Language Models**" by Paul Röttger, Valentin Hofmann, Valentina Pyatkin, Musashi Hinck, Hannah Rose Kirk, Hinrich Schütze, and Dirk Hovy.

For details, please refer to the paper (Link TBU).

### Repo Structure
```
.
├── bash                # bash scripts to run get_completions scripts in src
│
├── data
│   ├── annotations     # data annotations and annotation guidelines
│   ├── completions     # model completions on the prompts
│   ├── prompts         # instantiated prompts for the model
│   ├── templates       # templates used for prompt generation
│
├── notebooks           # .ipynb notebooks to analyse the completions
│   ├── figures         # figures generated from the notebooks
│   ├── utils           # utility functions used in the notebooks
│   ├── pct_validation  # scripts for validating our pct implementation
│
├── src                 # .py scripts to generate prompts and get completions
```

Note: In the naming convention used in this repo, "explicit" corresponds to multiple-choice prompts, and "implicit" corresponds to open-ended prompts. "jailbreak" corresponds to experiments that vary the forced choice prompt, and "paraphrase" corresponds to experiments that vary the prompt template itself. See for example ./data/prompts.