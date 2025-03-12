import pandas as pd
from transformers import pipeline
template="You are working on improving the chat-bot for which you need to classify the given conversation as {}"
classifier = pipeline("zero-shot-classification")

candidate_labels = ["successful", "unsuccessful"]


def bart(combinedmessage :str):
    result = classifier(combinedmessage, candidate_labels,hypothesis_template=template)

    label=result['labels'][0]
    confidence_score=result['scores'][0]

    return label,confidence_score