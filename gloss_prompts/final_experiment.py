from api_key import OPENAI_API_KEY
from prompts import *
import pandas as pd
import json
from openai import OpenAI

# read input data
df = pd.read_csv("wn.csv")

client = OpenAI(api_key = OPENAI_API_KEY)

responses = {}

for index, row in df.iterrows():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a lexicographer that is helping to generate glosses for Ukrainian WordNet."},    
                {"role": "user", "content": zero_shot_cot_reasoning.format(lemma_ukr=row["lemma"], lemma_eng=row["lemma_en"], gloss=row["gloss_en"],
                        gloss_trans1=row["google_gloss"], gloss_trans2=row["bing_gloss"]), gloss_trans3=row["deepl_gloss"]},
                ],
                functions = functions,
                function_call = {
                    "name": functions[0]["name"]
                    }
                )
        
        responses[row["lemma"]] = json.loads(response.choices[0].message.function_call.arguments)["gloss"]

        with open(f'generated/glosses.txt', "a", encoding='utf8') as file:
            lemma = row['lemma']
            gloss =  responses[lemma]
            entry = f"{row['id_from']}\t{lemma}\t{gloss} \n"
            file.write(entry)
    except:
         with open(f'errors_n127.txt', "a", encoding='utf8') as file_er:
             file_er.write(f"{row['lemma']}\n")
