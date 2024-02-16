from api_key import OPENAI_API_KEY
from prompts import *
import pandas as pd
import json
import os
from openai import OpenAI

df = pd.read_csv("input_data.csv")

client = OpenAI(api_key = OPENAI_API_KEY)

