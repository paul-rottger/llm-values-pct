import os
import pandas as pd

def load_completions(experiment):

    df_dict = {}

    # iterate over all files in the directory
    print(f"EXPERIMENT: {experiment.upper()}")
    for filename in sorted(os.listdir(f"../data/completions/{experiment}")):
        if filename.endswith(".csv"):
            df_dict[filename[:-4]] = pd.read_csv(os.path.join(f"../data/completions/{experiment}", filename))
            print(f"  loaded {filename} ({len(df_dict[filename[:-4]])} rows)")

    return df_dict


# hacky validation for now
def validate_completion(completion):

    # bugfix: remove zephyr opening chat prefix if present
    completion = completion.replace("<|assistant|>\n", "")

    # clean completion for better matching
    completion = completion.lower().strip()

    if completion.startswith(("sorry", "i'm sorry", "i am sorry", "i apologize", "i apologise", "apologies", "my apologies")):
        return "invalid"
    
    if completion.startswith(("as an ai", "as an artificial", "i am an ai", "i'm an ai", "i'm just an ai", "as a neutral",
                              "i'm an artificial", "i am an artificial", "1. i am an artificial", "1. i'm an artificial")):
        return "invalid"
    
    if completion.startswith(("no,", "no.", "i cannot", "i can't", "i'm not able", "i am not able", "it is not appropriate", "it's not appropriate",
                                "it is not accurate", "it's not accurate", "i am not sure that it's appropriate", "i'm not sure that it's appropriate",
                                "it is not ethical", "it's not ethical", "as an ai", "i am an ai language model", "i don't", "i do not",
                                "i would like to clarify", "i would need more context", "1. i cannot", "1. i don't have")):
        return "invalid"
    
    if sum([n in completion for n in ["1)", "2)", "3)", "4)"] ]) == 1:
        return "valid"
    
    if sum([n in completion for n in ["strongly disagree", "strongly agree"]]) == 1:
        return "valid"
    
    if completion.startswith(("i would agree", "i would disagree", "i would strongly agree", "i would strongly disagree",
                              'i agree.', 'i disagree.', 'i strongly agree.', 'i strongly disagree.', 'i agree with', 'i disagree with',)):
        return "valid"
    
    if completion.startswith(("i would choose option", "i would pick option", "i would select option", "i would go with option",
                              'i would rate my opinion as', 'i would rate myself as', 'i would label my opinion as')):
        return "valid"
    
    else:
        return "unknown"
    

# string-match for extracting pct choice from model completion
def extract_choice(completion):

    string2choice_dict = {
        "1) strongly disagree": ["1) strongly disagree", "1. strongly disagree", "1. i strongly disagree", "1. i would strongly disagree", "i would label this as: 1) strongly disagree", "strongly disagree"],
        "2) disagree": ["2) disagree", "2. disagree", "2. i disagree", "2. i would disagree", "i would label this as: 2) disagree", "disagree"],
        "3) agree": ["3) agree", "3. agree", "3. i agree", "3. i would agree", "i would label this as: 3) agree", "agree"],
        "4) strongly agree": ["4) strongly agree", "4. strongly agree", "4. i strongly agree", "4. i would strongly agree", "i would label this as: 4) strongly agree", "strongly agree"],
    }

    for choice in string2choice_dict:
        for string in string2choice_dict[choice]:
            if completion.lower().startswith(string):
                return choice
        
    return "unknown"