import pandas as pd
from transformers import pipeline

classifier = pipeline("zero-shot-classification")

candidate_labels = ["successful", "unsuccessful"]


def bart(combinedmessage :str):
    result = classifier(combinedmessage, candidate_labels)

    label=result['labels'][0]
    confidence_score=result['scores'][0]

    return label,confidence_score