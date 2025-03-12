from fastapi import FastAPI
import uvicorn
from zeroshot import bart
from conversation_finder import search_by_id
from test import bert,gpt,llama,gpt_api
app = FastAPI()


@app.get("/classify/{conversation_id}")
def classify_conversation(conversationid: int, fetch_data : bool=True):
    try :
        conversation = search_by_id(conversationid,fetch_data)
        print("Conversation : \n",conversation)
        if isinstance(conversation, dict) and "message" in conversation:
            return conversation
        try :
            label_bert=bert(conversation)
            # label_llama=llama(conversation)
            label_gpt=gpt_api(conversation)
            classification_label,classification_score=bart(conversation)
            if classification_label == "unsuccessful":
                label_bart=0
            else :
                label_bart=1
            return {"bart" : {"class" :label_bart,"score" : classification_score},"bert" : "NA","llama" : "NA","gpt" :label_gpt}
        except Exception as e:
            return {"message" : "An exception occured while classifying the data."}
    except Exception as e:
        return {"message" : "An exception occurred while finding the particular data."}
      

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run()