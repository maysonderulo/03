import streamlit as st
import openai
import os

# OpenAI API 키 설정
openai.api_key = 'your-openai-api-key'

st.title("OpenAI 어시스턴트와 채팅")

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def clear_chat():
    st.session_state['messages'] = []

# 사용자 입력
user_input = st.text_input("당신:", "")

# Clear 버튼
if st.button("Clear"):
    clear_chat()

# 사용자 입력이 있을 경우
if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=st.session_state['messages']
    )
    assistant_message = response['choices'][0]['message']['content']
    st.session_state['messages'].append({"role": "assistant", "content": assistant_message})

# 대화 내용 표시
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.write(f"**당신:** {message['content']}")
    else:
        st.write(f"**어시스턴트:** {message['content']}")
