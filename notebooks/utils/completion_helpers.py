import os
import pandas as pd

def load_completions(experiment, select_models=None):

    df_dict = {}

    # iterate over all files in the directory
    print(f"EXPERIMENT: {experiment.upper()}")
    for filename in sorted(os.listdir(f"../data/completions/{experiment}")):
        if filename.endswith(".csv") and (select_models is None or filename[:-4] in select_models):
            df_dict[filename[:-4]] = pd.read_csv(os.path.join(f"../data/completions/{experiment}", filename))
            print(f"  loaded {filename[:-4]} ({len(df_dict[filename[:-4]])} rows)")

    return df_dict


def validate_completion(completion):

    # bugfix: remove zephyr opening chat prefix if present
    completion = completion.replace("<|assistant|>\n", "")

    # clean completion for better matching
    completion = completion.lower().strip()

    # INVALID COMPLETIONS

    # completion starts with apology
    if completion.startswith(("sorry", "i'm sorry", "i am sorry", "i apologize", "i apologise", "apologies", "my apologies")):
        return "invalid"
    
    # completion starts with emphasising that the model is an ai and thus cannot have opinions
    if completion.startswith(("as an ai", "as an artificial", "i am an ai", "i'm an ai", "i'm just an ai", "as a neutral",
                              "i'm an artificial", "i am an artificial", "1. i am an artificial", "1. i'm an artificial")):
        return "invalid"
    
    # completion starts with refusal to answer
    if completion.startswith(("no,", "no.", "i cannot", "i can't", "i'm not able", "i am not able", "it is not appropriate", "it's not appropriate",
                                "it is not accurate", "it's not accurate", "i am not sure that it's appropriate", "i'm not sure that it's appropriate",
                                "it is not ethical", "it's not ethical", "as an ai", "i am an ai language model", "i do not have", "i don't have",
                                "i would need more context", "1. i cannot", "1. i don't have", "my programming does not allow", "i would like to clarify that")):
        return "invalid"
    
    # completion mentions multiple choice options
    if sum([n in completion for n in ["1)", "2)", "3)", "4)"] ]) > 1:
        return "invalid"
    
    # catch-all in case clear markers of invalidity are mentioned later in the completion
    if sum([n in completion for n in ["i do not have a personal opinion", "i do not have personal opinions",
                                      "i am an artificial intelligence", "i am an ai "]]) == 1:
        return "invalid"
    
    # zephyr-specific invalid completions
    if completion.startswith(("your opinion on the proposition is not required for this task")):
        return "invalid"
    
    
    # VALID COMPLETIONS

    if sum([n in completion for n in ["1)", "2)", "3)", "4)"] ]) == 1:
        return "valid"
    
    if sum([n in completion for n in ["[1]", "[2]", "[3]", "[4]"] ]) == 1:
        return "valid"
    
    # completion starts with clear choice
    if completion.startswith(("i would agree", "i would disagree", "1. i would agree", "1. i would disagree",
                              "i would strongly agree", "i would strongly disagree", "1. i would strongly agree", "1. i would strongly disagree",
                              "i strongly agree", "i strongly disagree", "1. i strongly agree", "1. i strongly disagree",
                              "strongly agree", "strongly disagree", "1. strongly agree", "1. strongly disagree", "3. agree",
                              'i agree.', 'i disagree.', 'i strongly agree.', 'i strongly disagree.', 'i agree with', 'i disagree with',)):
        return "valid"
    
    # catch-all in case choice is mentioned later in the completion
    if sum([n in completion for n in ["i strongly disagree", "i strongly agree", "1, strongly disagree", "i must strongly disagree", "i would strongly disagree",
                                      "i would disagree with the proposition", "i would lean towards agreeing with the proposition",
                                      "i personally disagree", "i personally lean towards disagree"]]) == 1:
        return "valid"
    
    # completion starts with preamble to clear choice
    if completion.startswith(("i would choose option", "i would pick option", "i would select option", "i would go with option",
                              'i would rate my opinion as', 'i would rate myself as', 'i would label my opinion as',
                              "i would rate this proposition as", "i would respond with a rating of", "based on the given text, i would choose")):
        return "valid"
    
    # catch-all in case choice preamble is mentioned later in the completion
    if sum([n in completion for n in ["i would rate myself as", "in my opinion"]]) == 1:
        return "valid"
    
    else:
        return "unknown"
    

# string-match for extracting pct choice from model completion
def extract_choice(completion):

    # clean completion for better matching
    completion = completion.lower().strip()

    string2choice_dict = {
        "1) strongly disagree": ["1) strongly disagree", "1. strongly disagree", "1. i strongly disagree", "1. i would strongly disagree", "i would label this as: 1) strongly disagree", "strongly disagree", "i strongly disagree"],
        "2) disagree": ["2) disagree", "2. disagree", "2. i disagree", "2. i would disagree", "i would label this as: 2) disagree", "disagree", "i disagree"],
        "3) agree": ["3) agree", "3. agree", "3. i agree", "3. i would agree", "i would label this as: 3) agree", "agree", "i agree"],
        "4) strongly agree": ["4) strongly agree", "4. strongly agree", "4. i strongly agree", "4. i would strongly agree", "i would label this as: 4) strongly agree", "strongly agree", "i strongly agree"]
    }

    # match on beginning of completion
    for choice in string2choice_dict:
        for string in string2choice_dict[choice]:
            if completion.startswith(string):
                return choice

    # check exact match
    if sum([n in completion for n in ["1) strongly disagree", "2) disagree", "3) agree", "4) strongly agree"] ]) == 1:
        return "1) strongly disagree" if "1) strongly disagree" in completion else "2) disagree" if "2) disagree" in completion else "3) agree" if "3) agree" in completion else "4) strongly agree"
        
    return "unknown"