import pandas as pd
import time 
import fire
import logging
import torch
import os

from simple_generation import SimpleGenerator


def main(
        # data parameters
        test_data_input_path: str,
        n_test_samples: int,
        input_col: str,
        test_data_output_path: str,

        # model parameters
        model_name_or_path: str,

        # inference parameters
        batch_size, # can be int or "auto"
          
        # quantization parameters
        load_in_8bit: bool,
           
        # misc parameters
        log_level: str,
        ):

    ###########################################################
    # SET UP
    ###########################################################

     # set up logging
    logging.basicConfig(level=getattr(logging, log_level.upper()), format='%(asctime)s %(levelname)s %(message)s')

    # set up device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logging.info(f"Running on device: {device}")
    if device == "cuda":
        logging.info(f"CUDA memory: {round(torch.cuda.mem_get_info()[0]/1024**3,2)}GB")

    ###########################################################
    # LOAD DATA
    ###########################################################

    # load TEST data
    test_df = pd.read_csv(test_data_input_path)
    logging.info(f"Loaded TEST data: {test_df.shape[0]} rows")

    # optional: select random sample of rows for TEST -- useful for debugging
    if n_test_samples > 0:
        test_df = test_df.sample(n_test_samples, random_state=123)
        logging.info(f"Sampled {n_test_samples} rows from TEST data")

    # write prompts to list
    input_texts = test_df[input_col].tolist()

    # print 3 random prompts
    logging.info(f"3 random prompts from TEST data:\n{test_df.sample(3, random_state=123)[input_col].tolist()}\n")

    ###########################################################
    # LOAD GENERATOR
    ###########################################################

    logging.info(f"Loading model {model_name_or_path}")

    generator = SimpleGenerator(
        model_name_or_path,
        load_in_8bit = load_in_8bit,
        torch_dtype=torch.bfloat16,
    )

    ###########################################################
    # GET COMPLETIONS
    ###########################################################

    logging.info(f"Generating completions for {len(input_texts)} prompts")

    completions = generator(
        texts = input_texts,
        temperature=0.01,
        max_new_tokens=128,
        top_p=1.0,
        do_sample=True,
        skip_prompt=True,
        batch_size=batch_size,
        starting_batch_size=16,
        apply_chat_template=True,
    )

    logging.info(f"Generated {len(completions)} completions")

    # write new model completions to new column
    test_df["completion"] = completions
    test_df["model"] = model_name_or_path

    # check if output path exists, otherwise create it
    if not os.path.exists(test_data_output_path.rsplit("/", 1)[0]):
        logging.info(f"Creating new path {test_data_output_path.rsplit('/', 1)[0]}")
        os.makedirs(test_data_output_path.rsplit("/", 1)[0])

    logging.info(f"Saving completions to {test_data_output_path}")
    test_df.to_csv(test_data_output_path, index=False)


if __name__ == "__main__":
    st = time.time()
    fire.Fire(main)
    logging.info(f'Total execution time: {time.time() - st:.2f} seconds')