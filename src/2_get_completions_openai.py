import openai
from openai import OpenAI

import fire
import time
import pandas as pd
import httpx

from retrying import retry
from decouple import config
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

tqdm.pandas()


class GPTWrapper:

    def __init__(self, gen_model):
        self.model_name = gen_model
        self.client = OpenAI(
            api_key=config('OPENAI_API_KEY'), # reads from a file called ".env" in root directory of repo
            #timeout=httpx.Timeout(15.0, read=5.0, write=10.0, connect=3.0)
        )

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000) # 2^x * 1000 milliseconds between each retry, up to 10 seconds, then 10 seconds afterwards
    def get_completion(self, prompt):
    
        input = [{"role": "system", "content": ""},
                 {"role": "user", "content": prompt}]

        try:
            response = self.client.chat.completions.create(model = self.model_name,
                messages = input,
                temperature = 0,
                max_tokens = 256,
                top_p = 1,
                frequency_penalty = 0,
                presence_penalty = 0,
                )

            return response.choices[0].message.content
        
        except openai.OpenAIError as e:
            print(f"OpenAIError: {e}. Retrying with exponential backoff.")
            raise e

    def get_parallel_completions(self, prompts, max_workers):
        completions = thread_map(self.get_completion, prompts, max_workers=max_workers)
        return [c for c in completions]


def main(gen_model: str, input_path: str, input_col: str, caching_path: str, output_path: str,
         n_batches: int, start_batch: int, n_samples: int = 0,
         max_workers: int = 1, seed: int = 1234):
    
    # load csv
    df = pd.read_csv(input_path)
    print(f"Loaded data from {input_path}: {df.shape[0]} rows")

    # optional: select random sample from entries -- useful for debugging
    if n_samples > 0:
        df = df.sample(n_samples, random_state=seed)
        print(f"Sampled {n_samples} rows from data")

    # split df into n_batches, even if n_batches does not divide df evenly
    df_dict = {}
    for i in range(n_batches):
        df_dict[i] = df.iloc[i::n_batches].copy()

    # initialize GPTWrapper
    gpt = GPTWrapper(gen_model)
    print(f"Initialized OpenAI model: {gen_model}")
    
    # for each batch from start_batch, get completions and save to csv
    for i in range(start_batch, n_batches):
        print(f"Processing batch {i+1} of {n_batches} with {max_workers} workers")
        df_dict[i]["completion"] = gpt.get_parallel_completions(df_dict[i][input_col], max_workers = max_workers)
        df_dict[i].to_csv(caching_path + f"/batch_{i}.csv", index=False)

    # concatenate all batches from the caching path
    df = pd.concat([pd.read_csv(caching_path + f"/batch_{i}.csv") for i in range(n_batches)])

    # write model name to column
    df["model"] = gen_model

    # save final dataframe to csv
    df.to_csv(output_path, index=False)

    return


if __name__ == "__main__":
    st = time.time()
    fire.Fire(main)
    et = time.time()
    print(f'Execution time: {et - st:.2f} seconds')