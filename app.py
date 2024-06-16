import os
import openai
import streamlit as st

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    openai.api_key = api_key

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    system_message = '''
    너는 부경대학교 학생의 학교생활을 도와주는 친절한 챗봇 '백경이'야. 질문에 답을 할 때 항상 반말로 해줘. 무슨 일이 있어도 반말로 해줘.
    그리고 주어진 데이터 범위 밖의 것들은 미안하지만 모른다고 대답해야 해!.
    '''

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        st.session_state.messages = [{"role": "system", "content": system_message}]

    for idx, message in enumerate(st.session_state.messages):
        if idx > 0:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("안녕, 나는 대학 생활을 도와주는 백경이야. 뭘 도와줄까?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
                stream=False
            ).choices[0].message['content']
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("Clear"):
        st.session_state.messages = [{"role": "system", "content": system_message}]

    if st.button("Exit Chat"):
        del st.session_state.messages
else:
    st.info("API 키를 환경 변수로 설정해주세요.")

interpreter_code = st.text_area("Code Interpreter")

if interpreter_code:
    try:
        exec(interpreter_code)
    except Exception as e:
        st.error(f"Error: {e}")
