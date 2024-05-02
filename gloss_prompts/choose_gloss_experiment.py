from api_key import OPENAI_API_KEY
from prompts import *
import pandas as pd
import json
from openai import OpenAI
from time import time

# read input data
df = pd.read_csv("test_sample.csv")

client = OpenAI(api_key = OPENAI_API_KEY)

##### zero-shot prompt
start = time()
responses = {}

for index, row in df.iterrows():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a lexicographer that is helping to generate glosses for Ukrainian WordNet."},
            {"role": "user", "content": zero_shot_prompt.format(lemma_ukr=row["lemma"], lemma_eng=row["lemma_en"], gloss=row["gloss_en"],
                     gloss_trans1=row["google_gloss"], gloss_trans2=row["bing_gloss"], gloss_trans3=row["deepl_gloss"])},
            ]
            )
    
    responses[row["lemma"]] = response.choices[0].message.content

print(f"zero-shot prompt: {time() - start} s")

with open(f'results/zero_shot.json', 'w', encoding='utf8') as file:
    json_string = json.dumps([{'lemma': k, 'gloss': v} for k,v in responses.items()], indent=4, ensure_ascii=False)
    file.write(json_string)


#### one-shot prompt
# responses = {}
example = """
<reseacher>: Generate gloss in Ukrainian WordNet for lemma "яблуко"
which is lemma "apple" in English WordNet, 
based on gloss from English Wordnet: "fruit with red or yellow or green skin and sweet to tart crisp whitish flesh"
and its translations in Ukrainian, each translation in separate angle brackets: <{плід з червоною або жовтою або зеленою шкіркою і солодкою до терпкої хрусткою білуватою м’якоттю}>, 
<фрукти з червоною або жовтою або зеленою шкіркою і солодкою, щоб терпкати хрустку білувату м'якоть>.

<lexigographer>: плід з червоною, жовтою або зеленою шкіркою та солодко-терпкою хрусткою білуватою м'якоттю.
"""

start = time()
responses = {}

for index, row in df.iterrows():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a lexicographer that is helping to generate glosses for Ukrainian WordNet."},
            {"role": "user", "content": one_shot_prompt.format(example = example, lemma_ukr=row["lemma"], lemma_eng=row["lemma_en"], gloss=row["gloss_en"],
                     gloss_trans1=row["google_gloss"], gloss_trans2=row["bing_gloss"]), gloss_trans3=row["deepl_gloss"]},
            ]
            )
    
    responses[row["lemma"]] = response.choices[0].message.content

with open(f'results/one_shot_3_5.json', 'w', encoding='utf8') as file:
    json_string = json.dumps([{'lemma': k, 'gloss': v} for k,v in responses.items()], indent=4, ensure_ascii=False)
    file.write(json_string)


#### zero_shot_cot_reasoning
start = time()
responses = {}

for index, row in df.iterrows():
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

with open(f'results/zero_shot_cot_reas.json', 'w', encoding='utf8') as file:
    json_string = json.dumps([{'lemma': k, 'gloss': v} for k,v in responses.items()], indent=4, ensure_ascii=False)
    file.write(json_string)


#### guideline_prompt_with_reasoning
start = time()
responses = {}

for index, row in df.iterrows():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a lexicographer that is helping to generate glosses for Ukrainian WordNet."},    
            {"role": "user", "content": guideline_prompt_with_reasoning.format(lemma_ukr=row["lemma"], lemma_eng=row["lemma_en"], gloss=row["gloss_en"],
                     gloss_trans1=row["google_gloss"], gloss_trans2=row["bing_gloss"]), gloss_trans3=row["deepl_gloss"]},
            ],
            functions = functions,
            function_call = {
                "name": functions[0]["name"]
                }
            )
    
    responses[row["lemma"]] = json.loads(response.choices[0].message.function_call.arguments)["gloss"]

with open(f'results/guideline_prompt_with_reasoning.json', 'w', encoding='utf8') as file:
    json_string = json.dumps([{'lemma': k, 'gloss': v} for k,v in responses.items()], indent=4, ensure_ascii=False)
    file.write(json_string)

#### one_shot_cot
start = time()
responses = {}

for index, row in df.iterrows():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a lexicographer that is helping to generate glosses for Ukrainian WordNet."},    
            {"role": "user", "content": one_shot_cot.format(example=example, lemma_ukr=row["google_lemma"], lemma_eng=row["lemma_en"], gloss=row["gloss_en"],
                     gloss_trans1=row["google_gloss"], gloss_trans2=row["bing_gloss"]), gloss_trans3=row["deepl_gloss"]},
            ],
            functions = functions,
            function_call = {
                "name": functions[0]["name"]
                }
            )
    
    responses[row["lemma"]] = json.loads(response.choices[0].message.function_call.arguments)["gloss"]

with open(f'results/one_shot_cot.json', 'w', encoding='utf8') as file:
    json_string = json.dumps([{'lemma': k, 'gloss': v} for k,v in responses.items()], indent=4, ensure_ascii=False)
    file.write(json_string)
