import pandas as pd

def generate_prompts(prompt_templates_df, pct_df, answer_options_df, jailbreaks_df):
    """
    Generates prompts from templates and options.
    """

    # initialize empty dataframe
    prompts_df = pd.DataFrame()

    # iterate through templates
    for i, row in prompt_templates_df.iterrows():

        for _, pct_row in pct_df.iterrows():

            for _, answer_options_row in answer_options_df.iterrows():

                for _, jailbreaks_row in jailbreaks_df.iterrows():

                    inputs = {"pct_proposition": pct_row.pct_proposition,
                              "answer_options": answer_options_row.answer_options,
                              "jailbreak": jailbreaks_row.jailbreak}
                    
                    prompts_df = prompts_df._append({"prompt": row.prompt_template.format(**inputs)}, ignore_index=True)

    return prompts_df

def main():

    # set input file paths
    prompt_templates_df = pd.read_csv("../data/templates/prompt_templates.csv")
    pct_df = pd.read_csv("../data/templates/pct_propositions.csv")
    answer_options_df = pd.read_csv("../data/templates/answer_options.csv")
    jailbreaks_df = pd.read_csv("../data/templates/jailbreaks.csv")

    # (optional) select specific templates and options for testing
    answer_options_df = answer_options_df[answer_options_df.note=="main"]
    jailbreaks_df = jailbreaks_df[jailbreaks_df.note=="main"]

    # generate prompts
    prompts_df = generate_prompts(prompt_templates_df, pct_df, answer_options_df, jailbreaks_df)

    # create id column, move to front
    prompts_df["id"] = prompts_df.index + 1
    prompts_df = prompts_df[["id"] + prompts_df.columns[:-1].tolist()]

    # save prompts
    prompts_df.to_csv("../data/prompts/test.csv", index=False)

    return

if __name__ == "__main__":
    main()