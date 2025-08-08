from openai import AzureOpenAI
import os
import streamlit as st
st.title("🦁 Welcome to Lion Chatbot 🦁")
st.write("こんにちは、ここはLionが活躍する特別な空間です！")

# デバッグ用メッセージを追加
st.text("テスト段階のメッセージですが、このデザインを楽しんでください！")

# Azure OpenAI の API キーとエンドポイントを環境変数から取得  
azure_endpoint = os.environ["CHATBOT_AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["CHATBOT_AZURE_OPENAI_API_KEY"]
deployment_name = "gpt-4o-mini" # 先ほど作成したモデルのデプロイ名に置き換えてください
api_version = "2024-12-01-preview" # 先ほど作成したモデルの API バージョンに置き換えてください

# Azure OpenAI クライアントを作成
try:
    client = AzureOpenAI(
    azure_endpoint=azure_endpoint,  
    api_key=api_key,
    api_version=api_version
    )
    st.write("Enter a message to start a chat.")
except Exception as e:
    st.write(f"Error initializing Azure OpenAI client:, {e}")

# チャット履歴を保持するリスト  
chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
  
# ユーザーからのメッセージに対して応答を生成する関数  
def get_response(message):  
    chat_history.append({"role": "user", "content": message}) 
    # 履歴を確認するためのデバッグメッセージ
    print(f"Chat history before API call: {chat_history}")
    try:
        response = client.chat.completions.create(
        model=deployment_name, 
        messages=chat_history
        )
        # 応答内容を確認するためのデバッグメッセージ
        print(f"API Response: {response}")
        assistant_message = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    except Exception as e:
        # エラー詳細を確認するためのデバッグメッセージ
        print(f"Error details: {e}")
        return f"Error during API call: {e}"

# Streamlitフォームの作成
with st.form("interaction_form"):
    user_input = st.text_input("You:", key="user_input_key")
    if st.form_submit_button("Send"):
        if user_input:
            chat_response = get_response(user_input)
            st.write("ChatGPT:", chat_response)
        else:
            st.write("メッセージを入力してください！")    
  
