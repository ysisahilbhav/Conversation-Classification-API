from connection_details import get_connected
import pandas as pd
import json

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
    print("No error n database")
    # Combine the DataFrames
    df_combined = pd.concat([df_incoming, df_outgoing], ignore_index=True)


    # Sort by ConversationId and Timestamp
    df_combined.sort_values(by=["ConversationId", "Timestamp"], inplace=True)
   
    df_cleaned = df_combined.dropna(subset=["Message"])
    print("Database cleaned")
    #Combine all the data belonging to the conversation_id into a single line.
    grouped = df_cleaned.groupby("ConversationId").apply(
    lambda x: ",".join(x.sort_values(by="Timestamp")["Message"].apply(extract_text))).reset_index()
    print("Error in groupby")
    grouped.columns = ["ConversationId", "CombinedMessages"]
    # grouped = pd.DataFrame(grouped)
    grouped.to_pickle("combined_conversations_final.pkl")

    return grouped

def fetch_data_by_id(id : int):
    connection=get_connected()
    cursor = connection.cursor()

    cursor.execute(f"SELECT conversationId, message, conversationincomingtime FROM conversationincoming where conversationId={id}")
    incoming = cursor.fetchall()
    cursor.execute(f"SELECT conversationId, message, conversationoutgoingtime FROM conversationoutgoing where conversationId={id}")
    outgoing = cursor.fetchall()

    cursor.close()
    connection.close()

    df_incoming = pd.DataFrame(incoming, columns=["ConversationId", "Message", "Timestamp"])
    df_outgoing = pd.DataFrame(outgoing, columns=["ConversationId", "Message", "Timestamp"])

    # Apply extract_text to the messages
    df_incoming["Message"] = df_incoming["Message"].apply(extract_text)
    df_outgoing["Message"] = df_outgoing["Message"].apply(extract_text)

    # Add labels to the messages
    df_incoming["Message"] = "user : " + df_incoming["Message"]
    df_outgoing["Message"] = "bot : " + df_outgoing["Message"]

    # Combine the DataFrames
    df_combined = pd.concat([df_incoming, df_outgoing], ignore_index=True)

    df_cleaned = df_combined.dropna(subset=["Message"])
    print(df_cleaned)
    # grouped = df_cleaned.groupby("ConversationId").apply(
    # lambda x: ",".join(x.sort_values(by="Timestamp")["Message"].apply(extract_text))).reset_index()
    grouped = df_cleaned.groupby("ConversationId").apply(
    lambda x: ",".join(
        x.sort_values(by="Timestamp")["Message"]
        .dropna()  # This line filters out None values
    )
).reset_index()
   
    grouped.columns = ["ConversationId", "CombinedMessages"]

    grouped = pd.DataFrame(grouped)
    print(grouped)
    return grouped


def search_by_id(conversationid : int, flag :bool):
    try :
        if flag:
            try:
                # df=fetch_data()
                df=fetch_data_by_id(conversationid)
            except Exception as e:
                print(f"Data fetch error: {e}")
                return {"message" : f"No conversation found with ConversationId - {conversationid}"}
        else :
            print("pickle\n\n\n\n")
            df = pd.read_pickle("combined_conversations_final.pkl")
        result=df
        # result = df[df["ConversationId"] == conversationid]
  
        if not result.empty:
            return result["CombinedMessages"].values[0]
        else:
            return {"message" : f"No conversation found with ConversationId - {conversationid}"}
    except Exception as e:
        print(f"Data processing error: {e}")
        return {"message" : "Data could not be fetched at this moment please try again later"}
    

def extract_text(message):
    try:
        message_list = json.loads(message)
        if isinstance(message_list, list) and len(message_list) > 0:
            return message_list[0].get('text', '')
    except json.JSONDecodeError:
        return message