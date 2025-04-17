import jsonlines
import pandas as pd

d = {"lemma_ukr": [], "gloss_sum": []}

with jsonlines.open('sum_14_final.jsonlines') as reader:
    counter = 0
    for obj in reader:
        try:
            d["gloss_sum"].append(obj["synsets"][0]["gloss"])
            lemma = "".join(ch for ch in obj["lemma"].lower() if ch.isalnum())
            d["lemma_ukr"].append(lemma)
        except:
            print(obj)
            # break

df = pd.DataFrame(d)

df.to_csv("glosses_sum.csv", index = False)