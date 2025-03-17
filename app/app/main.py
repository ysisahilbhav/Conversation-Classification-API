from fastapi import FastAPI
import uvicorn
from zeroshot import bart
from conversation_finder import search_by_id
app = FastAPI()


@app.get("/classify/{conversation_id}")
def classify_conversation(conversationid: int, fetch_data : bool):
    try :
        conversation = search_by_id(conversationid,fetch_data)
        print(conversation)
        if isinstance(conversation, dict) and "message" in conversation:
            return conversation
        try :
            classification_label,classification_score=bart(conversation)
            if classification_label == "unsuccessful":
                return {"label" : 0}
            return {"label" : 1}
        except Exception as e:
            return {"message" : "An exception occured while classifying the data."}
    except Exception as e:
        return {"message" : "An exception occurred while finding the particular data."}
      

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run()