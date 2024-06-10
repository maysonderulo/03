import openai
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="친근한 챗봇 및 DALL-E 이미지 생성기")

# 사이드바에서 페이지 선택
page = st.sidebar.selectbox("페이지를 선택하세요", ["친근한 챗봇", "DALL-E 이미지 생성기"])

# API 키 입력
api_key = st.text_input("Enter your OpenAI API key", type="password")

# API 키 설정
if api_key:
    openai.api_key = api_key

    if page == "친근한 챗봇":
        st.title("친근한 챗봇")

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        system_message = '''
        너의 이름은 친구봇이야.
        너는 항상 반말을 하는 챗봇이야. 다나까나 요 같은 높임말로 절대로 끝내지 마.
        항상 반말로 친근하게 대답해줘.
        영어로 질문을 받아도 무조건 한글로 답변해줘.
        한글이 아닌 답변일 때는 다시 생각해서 꼭 한글로 만들어줘.
        모든 답변 끝에 답변에 맞는 이모티콘도 추가해줘.
        '''

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if len(st.session_state.messages) == 0:
            st.session_state.messages = [{"role": "system", "content": system_message}]

        for idx, message in enumerate(st.session_state.messages):
            if idx > 0:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("무엇을 도와줄까?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=st.session_state.messages
                )
                response_content = response.choices[0].message['content']
                st.markdown(response_content)
                st.session_state.messages.append({"role": "assistant", "content": response_content})

    elif page == "DALL-E 이미지 생성기":
        st.title("DALL-E 이미지 생성기")
        st.write("안뇽! 원하는 이미지 설명을 입력하면 내가 그려줄게!")

        if prompt := st.text_input("이미지 설명을 입력하세요"):
            with st.spinner("이미지를 생성 중입니다..."):
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="256x256"
                )
                image_url = response['data'][0]['url']
                st.image(image_url, caption=prompt)
else:
    st.info("API key를 입력해주세요.")
      
       
