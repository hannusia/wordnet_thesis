from langchain.prompts import PromptTemplate

zero_shot = PromptTemplate.from_template(
    """
    Generate gloss in Ukrainian WordNet for lemma "{lemma_ukr}"
    which is lemma "{lemma_eng}" in English WordNet, 
    based on gloss from English Wordnet: "{gloss}"
    and its translations in Ukrainian, each translation in separate angle brackets: <{gloss_trans1}>, <{gloss_trans2}>, <{gloss_trans3}>. 
    """
)

zero_shot_cot_reasoning = PromptTemplate.from_template(
    """
    Generate gloss in Ukrainian WordNet for lemma "{lemma_ukr}"
    which is lemma "{lemma_eng}" in English WordNet, 
    based on gloss from English Wordnet: "{gloss}"
    and its translations in Ukrainian, each translation in separate angle brackets: <{gloss_trans1}>, <{gloss_trans2}>, <{gloss_trans3}>. 

    Think carefully and logically, provide reasoning to your answer.

    Provide your answer in JSON format with the following keys: reasoning, gloss.
    """
)

one_shot = PromptTemplate.from_template(
    """
    Your task is to answer in a consistent style.
    {example}

    <reseacher>: Generate gloss in Ukrainian WordNet for lemma "{lemma_ukr}"
    which is lemma "{lemma_eng}" in English WordNet, 
    based on gloss from English Wordnet: "{gloss}"
    and its translations in Ukrainian, each translation in separate angle brackets: <{gloss_trans1}>, <{gloss_trans2}>, <{gloss_trans3}>. 
    """
)

one_shot_cot = PromptTemplate.from_template(
    """
    Your task is to answer in a consistent style.
    {example}

    <reseacher>: Generate gloss in Ukrainian WordNet for lemma "{lemma_ukr}"
    which is lemma "{lemma_eng}" in English WordNet, 
    based on gloss from English Wordnet: "{gloss}"
    and its translations in Ukrainian, each translation in separate angle brackets: <{gloss_trans1}>, <{gloss_trans2}>, <{gloss_trans3}>. 

    Think carefully and logically, provide reasoning to your answer.

    Provide your answer in JSON format with the following keys: reasoning, gloss.
    """
)

zero_shot_cot_steps = PromptTemplate.from_template(
    """
    Generate gloss in Ukrainian WordNet for lemma "{lemma_ukr}"
    which is lemma "{lemma_eng}" in English WordNet, 
    based on gloss from English Wordnet: "{gloss}"
    and its translations in Ukrainian, each translation in separate angle brackets: <{gloss_trans1}>, <{gloss_trans2}>, <{gloss_trans3}>. 

    Let's think step by step.

    Provide your answer in JSON format with the following keys: steps, gloss.
    """
)

guideline_prompt_with_reasoning = PromptTemplate.from_template(
    """
    Your task is to propose your variant of Ukrainian gloss for a lemma in Ukrainian WordNet.
    To solve the problem do the following:
        - First, analyze given English gloss, and its translations into Ukrainian
        - Then evaluate each of the variants, and based on given information create your own gloss
        - Make the answer grammatically correct, pay special attention to the conjugation
    
    Give output in following format:
    ```
    gloss: gloss that you generated
    reasoning: explain why you choose this gloss
    ```

    Use the following format:
    Ukrainian lemma:
    ```
    ukrainian lemma here
    ```

    English lemma:
    ```
    english lemma here
    ```

    Gloss from English WordNet:
    ```
    gloss from english wordnet here
    ```

    Gloss translations:
    ```
    one or multiple translation of english gloss into ukrainian elimited by <>
    ```

    Your answer:
    ```
    Ukrainian gloss that you propose here 
    ```

    Ukrainian lemma:
    ```
    {lemma_ukr}
    ```

    English lemma:
    ```
    {lemma_eng}
    ```

    Gloss from English WordNet:
    ```
    {gloss}
    ```

    Gloss translations:
    ```
    <{gloss_trans1}>
    <{gloss_trans2}>
    <{gloss_trans3}>
    ```

    Provide your answer in JSON format with the following keys: reasoning, gloss.
    """
)

functions = [
    {
        "name": "generate_gloss",
        "description": "Generates ukrainian gloss for a given lemma.",
        "parameters": {
            "type": "object",
            "properties": {
                "gloss": {
                    "type": "string",
                    "description": "Gloss that describes given lemma."
                },
                "reasoning": {
                    "type": "string",
                    "description": "Explanation why this gloss was chosen."
                }
            }
        }
    }, 

    {
        "name": "generate_gloss",
        "description": "Generates ukrainian gloss for a given lemma.",
        "parameters": {
            "type": "object",
            "properties": {
                "gloss": {
                    "type": "string",
                    "description": "Gloss that describes given lemma."
                },
                "steps": {
                    "type": "string",
                    "description": "Steps that were taken while solving problem."
                }
            }
        }
    }
]