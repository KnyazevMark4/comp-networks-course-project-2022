import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_checkpoint = 'cointegrated/rubert-tiny-sentiment-balanced'
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
if torch.cuda.is_available():
    model.cuda()
    
def predict_sentiment(text):
    """ Calculate sentiment of a text. `return_type` can be 'label', 'score' or 'proba' """
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(model.device)
        proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()[0]
    prediction = {
      "pred_label": model.config.id2label[proba.argmax()],
      "probabilities": {
        "negative": proba[0],
        "neutral":  proba[1],
        "positive":  proba[2]
      }
    }
    return prediction

# predict_sentiment("Качество продукта соответствует требованиям заказчика")
