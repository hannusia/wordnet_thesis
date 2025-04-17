import jsonlines
import pandas as pd

google = "SlidingWindowGoogleTranslator(group_by=3,add_or=True,add_quotes=True,combine_in_one=True,add_aux_words=True)"
bing = "SlidingWindowBingTranslator(group_by=3,add_or=True,add_quotes=True,combine_in_one=True,add_aux_words=True)"

rows = []
counter = 0

with jsonlines.open('pwn_translated_basic/wordnet_exported.json') as reader:
    for obj in reader:
        try:
            row = [obj["_id"], obj["ili"], list(obj["words"].values())[0], obj["definition"][0]]

            g = obj["results"][google]
            b = obj["results"][bing]

            try:

                if len(g["terms"]) >= 1:
                    row.append(g["terms"][0][0])
                else:
                    row.append(None)
                
                if len(g["definitions"]) >= 1:
                    row.append(g["definitions"][0][0])
                else:
                    row.append(None)


                if len(b["terms"]) >= 1:
                    row.append(b["terms"][0][0])
                else:
                    row.append(None)
                
                if len(b["definitions"]) >= 1:
                    row.append(b["definitions"][0][0])
                else:
                    row.append(None)

                rows.append(row)

            except:
                print(b)
            
        except:
            # print(obj["_id"])
            counter += 1
    
print(counter)


pd.DataFrame.from_records(rows, columns=["id", "ili", "lemma_en", "gloss_en", "google_lemma", "google_gloss", "bing_lemma", "bing_gloss"]).to_csv("wn_trans.csv", index=False)
