from openai import OpenAI
import streamlit as st


api_key = sk-proj-yKWGbnHznn8PZbP1CAkWT3BlbkFJYxluBHJWAz70PgHY4sMC
if api_key:
    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    system_message = '''
    너는 부경대학교 학생의 학교생활을 도와주는 친절한 챗봇 '백경이'야 질문에 답을 할때 항상 반말로 해줘. 무슨일이 있어도 반말로 해줘 
    그리고 주어진 데이터 범위의 밖의 것들은 미안하지만 모른다고 대답해야해!.
    '''

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        st.session_state.messages = [{"role": "system", "content": system_message}]

    for idx, message in enumerate(st.session_state.messages):
        if idx > 0:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("안녕, 나는 대학 생활을 도와주는 백경이야. 뭘 도와줄까 ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("Clear"):
        st.session_state.messages = [{"role": "system", "content": system_message}]

    if st.button("Exit Chat"):
        del st.session_state.messages
else:
    st.info("API key를 입력해주세요.")


interpreter_code = st.text_area("Code Interpreter")

if interpreter_code:
    try:
        exec(interpreter_code)
    except Exception as e:
        st.error(f"Error: {e}")
