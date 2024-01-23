import pandas as pd

def generate_prompt_df(df_dict):

    # print number of rows in each input dataframe
    for key in df_dict.keys():
        print(f"  {len(df_dict[key])} {key}")

    # create a dataframe with all possible combinations of the input data
    prompts_df = df_dict["prompt_templates"].copy()
    for key in ["pct_propositions", "answer_options", "jailbreaks"]:
        prompts_df = prompts_df.merge(df_dict[key], how="cross")

    # create prompt column by applying the template to the input data
    prompts_df["full_prompt"] = prompts_df.apply(lambda x: x["templ_prompt"].format(
        pct_prompt=x["pct_prompt"],
        ans_prompt=x["ans_prompt"],
        jail_prompt=x["jail_prompt"] if x["jail_prompt"]==x["jail_prompt"] else "",
    ), axis=1)

    # print number of prompts generated
    print("Generated {} prompts as a combination of all inputs.".format(len(prompts_df)))

    return prompts_df


def main():

    # set input file paths
    df_dict = {}
    for input_file in ["prompt_templates", "pct_propositions", "answer_options", "jailbreaks"]:
        df_dict[input_file] = pd.read_csv(f"../data/templates/{input_file}.csv".format(input_file))

    # (optional) select specific templates and options for testing
    #df_dict["prompt_templates"] = df_dict["prompt_templates"][df_dict["prompt_templates"].templ_note=="implicit"]
    df_dict["prompt_templates"] = df_dict["prompt_templates"][df_dict["prompt_templates"].templ_id=="templ-11"]
    df_dict["answer_options"] = df_dict["answer_options"][df_dict["answer_options"].ans_note=="main"]
    df_dict["jailbreaks"] = df_dict["jailbreaks"][df_dict["jailbreaks"].jail_note=="implicit"]
    #df_dict["jailbreaks"] = df_dict["jailbreaks"][df_dict["jailbreaks"].jail_id=="jail-6"]

    # generate prompts
    prompts_df = generate_prompt_df(df_dict)

    # save prompts -- don't forget to rename the file!
    prompts_df.to_csv("../data/prompts/test.csv", index=False)

    return


if __name__ == "__main__":
    main()