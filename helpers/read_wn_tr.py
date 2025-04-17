import jsonlines
import pandas as pd

google = "SlidingWindowGoogleTranslator(group_by=3,add_or=True,add_quotes=True,combine_in_one=True,add_aux_words=True)"
bing = "SlidingWindowBingTranslator(group_by=3,add_or=True,add_quotes=True,combine_in_one=True,add_aux_words=True)"

d = {"google_lemma": [], "bing_lemma": [], "google_gloss": [], "bing_gloss": [], "pos": []}

with jsonlines.open('pwn_translated_basic/wordnet_exported.json') as reader:
    counter = 0
    for obj in reader:
        try: 
            g = obj["results"][google]
            b = obj["results"][bing]
            d["pos"].append(obj["pos"])

            try:

                if len(g["terms"]) >= 1:
                    d["google_lemma"].append(g["terms"][0][0])
                else:
                    d["google_lemma"].append(None)
                
                if len(g["definitions"]) >= 1:
                    d["google_gloss"].append(g["definitions"][0][0])
                else:
                    d["google_gloss"].append(None)


                if len(b["terms"]) >= 1:
                    d["bing_lemma"].append(b["terms"][0][0])
                else:
                    d["bing_lemma"].append(None)
                
                if len(b["definitions"]) >= 1:
                    d["bing_gloss"].append(b["definitions"][0][0])
                else:
                    d["bing_gloss"].append(None)

            except:
                print(b)
                break

        except:
            pass

df = pd.DataFrame(d)

df.to_csv("wn_trans.csv", index = False)
