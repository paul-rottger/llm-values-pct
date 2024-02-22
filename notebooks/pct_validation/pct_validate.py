"""

Validating local PCT implementation

Author: Dr Musashi Hinck


notes:
  quick script to validate local pct implementation
  will try using requests to complete form 
"""

# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup

# %%
from utils.completion_helpers import (
    load_completions,
    validate_completion,
    extract_choice,
)
from utils.plot_helpers import make_validity_bar_chart
from utils.pct_helpers import calculate_pct_coordinates, plot_pct
from pct import PCT, URL, ALL_ITEMS


# %% Load data/from Paul's notebook
# load completions for specified experiment
df_dict = load_completions(
    experiment="explicit_paraphrase_experiments_240124",
    select_models=["gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106"],
)  # , "Mistral-7B-Instruct-v0.1", "Mistral-7B-Instruct-v0.2"])

# validate completions
for df in df_dict:
    df_dict[df]["validation_label"] = df_dict[df]["completion"].apply(
        validate_completion
    )

# extract choice from completion
for df in df_dict:
    df_dict[df]["choice_label"] = df_dict[df]["completion"].apply(extract_choice)

# show rows where validation outcome is unknown despite label being valid
for df in df_dict:
    print(df)
    print(
        df_dict[df][
            (df_dict[df]["choice_label"] == "unknown")
            & (df_dict[df]["validation_label"] == "valid")
        ]
    )

# for each model for each template calculate PCT coordinates:
pct_dict = {}

for model in df_dict:
    print(model)
    pct_dict[model] = {}
    for template in sorted(df_dict[model].templ_id.unique()):
        pct_dict[model][template] = calculate_pct_coordinates(
            df_dict[model][
                df_dict[model].templ_id == template
            ].choice_label.reset_index(drop=True),
            DEBUG=True,
        )

# %%
pct_dict['gpt-3.5-turbo-1106']['templ-01']

# %% Use GPT responses
df = df_dict["gpt-3.5-turbo-1106"].copy()

labelmap = {
    "unknown": 0, # Forcing for test
    "1) strongly disagree": 0,
    "2) disagree": 1,
    "3) agree": 2,
    "4) strongly agree": 3,
}

# Our implementation
calculate_pct_coordinates(df['choice_label'].replace('unknown', '1) strongly disagree').reset_index(drop=True)) # (-2.37, -4.154102564102564)

# Website
pct = PCT(URL, ALL_ITEMS)
pct_ans = df.loc[df['templ_id'].eq('templ-01'), 'choice_label'].apply(labelmap.get).tolist()
pct.set_values(vals=pct_ans)
pct.take_test() # {'ec': -2.38, 'soc': -4.15}
