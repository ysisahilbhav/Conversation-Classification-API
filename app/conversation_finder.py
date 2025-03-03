from connection_details import get_connected
import pandas as pd


def fetch_data():
    connection=get_connected()
    cursor = connection.cursor()

    cursor.execute("SELECT conversationId, message, conversationincomingtime FROM conversationincoming")
    incoming = cursor.fetchall()
    cursor.execute("SELECT conversationId, message, conversationoutgoingtime FROM conversationoutgoing")
    outgoing = cursor.fetchall()
    cursor.close()
    connection.close()
    df_incoming = pd.DataFrame(incoming, columns=["ConversationId", "Message", "Timestamp"])
    df_outgoing = pd.DataFrame(outgoing, columns=["ConversationId", "Message", "Timestamp"])

    # Combine the DataFrames
    df_combined = pd.concat([df_incoming, df_outgoing], ignore_index=True)


    # Sort by ConversationId and Timestamp
    df_combined.sort_values(by=["ConversationId", "Timestamp"], inplace=True)
   
    df_cleaned = df_combined.dropna(subset=["Message"])

    #Combine all the data belonging to the conversation_id into a single line.
    grouped = df_cleaned.groupby("ConversationId").apply(
        lambda x: ",".join(x.sort_values(by="Timestamp")["Message"])
    ).reset_index()

    grouped.columns = ["ConversationId", "CombinedMessages"]
    # grouped.to_pickle("combined_conversations_final.pkl")

    return grouped

def search_by_id(conversationid : int, flag :bool):
    try :
        if flag=="true":
            try:
                print("hello")
                df=fetch_data()
                print(df)
            except Exception as e:
                print(f"Data fetch error: {e}")
                return {"message": "Cannot load the data from the server"}
        else :
            df = pd.read_pickle("combined_conversations_final.pkl")

        result = df[df["ConversationId"] == conversationid]
        print(result)
        # Print the combined message
        if not result.empty:
            return result["CombinedMessages"].values[0]
        else:
            return {"message" : f"No conversation found with ConversationId - {conversationid}"}
    except Exception as e:
        print(f"Data processing error: {e}")
        return {"message" : "Data could not be fetched at this moment please try again later"}


