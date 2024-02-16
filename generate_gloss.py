from api_key import OPENAI_API_KEY
from prompts import *
import pandas as pd
import json
import os
from openai import OpenAI


# read input data
df = pd.read_csv("input_data.csv")

client = OpenAI(api_key = OPENAI_API_KEY)

responses = {}

for index, row in df.iterrows():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a lexicographer that is helping to generate glosses for Ukrainian WordNet."},
            # {"role": "user", "content": simple_prompt.format(lemma_ukr=row["lemma_ua"], lemma_eng=row["lemma_en"], gloss=row["gloss"],
            #          gloss_trans1=row["gloss_trans1"], gloss_trans2=row["gloss_trans2"])},
            {"role": "user", "content": guideline_prompt_with_reasoning.format(lemma_ukr=row["lemma_ua"], lemma_eng=row["lemma_en"], gloss=row["gloss"],
                     gloss_trans1=row["gloss_trans1"], gloss_trans2=row["gloss_trans2"])},
            ]
            )
    
    responses[row["lemma_ua"]] = response.choices[0].message.content

i = len(os.listdir("results")) + 1
with open(f'results/result{i}.json', 'w', encoding='utf8') as file:
    json_string = json.dumps([{'lemma': k, 'gloss': v} for k,v in responses.items()], indent=4, ensure_ascii=False)
    file.write(json_string)
    