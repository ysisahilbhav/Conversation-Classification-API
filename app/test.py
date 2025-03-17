candidate_labels = ["successful", "unsuccessful"]

def bert(data : str):
    import pandas as pd
    from transformers import pipeline

    # Load the pre-trained GPT model for text classification
    classifier = pipeline('text-classification', model='distilbert/distilbert-base-uncased-finetuned-sst-2-english')

    # Define a function to classify the conversation
    def classify_conversation(conversation):
        result = classifier(conversation)
        return result[0]['label']

    # Apply the function to your data
    label = classify_conversation(data)
    if label == "unsuccessful":
        label=0
    else :
        label=1
    print(label)
    return label


def gpt(data : str):
    import pandas as pd
    from transformers import pipeline


    # Load the pre-trained GPT-2 model for text classification
    classifier = pipeline('text-classification', model='bhadresh-savani/gpt2-sentiment-analysis')

    # Define a function to classify the conversation
    def classify_conversation(conversation):
        result = classifier(conversation)
        return result[0]['label']

    # Apply the function to your data
    label = classify_conversation(data)

    
    if label == "unsuccessful":
        label=0
    else :
        label=1

    return label


def llama(data : str):
    import pandas as pd
    from transformers import pipeline
    # Load the pre-trained LLaMA 3.2 1B Instruct model for text classification
    classifier = pipeline('text-generation', model='meta-llama/Llama-3.2-3B-Instruct')

    # Define a function to classify the conversation
    def classify_conversation(conversation):
        prompt = f"Classify the following conversation as successful or unsuccessful:\n\n{conversation}\n\nClassification:"
        result = classifier(prompt, max_length=1500)
        return prompt,result[0]['generated_text'].split("Classification:")[1].strip()

    # Apply the function to your data
    label = classify_conversation(data)

    
    if label == "unsuccessful":
        label=0
    else :
        label=1
    return label




def gpt_api(data : str):
    import openai
    import os
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    THIS_MODEL = "gpt-4o-mini"

    response = client.chat.completions.create(
        model=THIS_MODEL,
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a cool chat-bot response analyst. Your goal is to go through the conversation between a user and the bot and classify it as 'successful' or 'unsuccessful'"
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Classify the conversation as successfull or unsuccessful just give the class as the output nothing else"
                    },
                    {
                        "type": "text",
                        "text": f"{data}"
                    }
                ]
            }
        ],
        max_tokens=300
    )

    label = response.choices[0].message.content
    if label == "unsuccessful":
        label=0
    else :
        label=1
    return label