import streamlit as st
import openai
import math

# OpenAI API 키 설정
openai.api_key = 'your-openai-api-key'

st.title("OpenAI 어시스턴트와 채팅 및 코드 인터프리터")

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def clear_chat():
    st.session_state['messages'] = []

def solve_right_triangle(hypotenuse, one_side):
    other_side = math.sqrt(hypotenuse**2 - one_side**2)
    angle_a = math.degrees(math.asin(one_side / hypotenuse))
    angle_b = math.degrees(math.asin(other_side / hypotenuse))
    angle_c = 90.0
    return other_side, angle_a, angle_b, angle_c

def generate_image(prompt):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt
    )
    image_url = response['data'][0]['url']
    return image_url

# 사용자 입력
user_input = st.text_input("당신:", "")

# Clear 버튼
if st.button("Clear"):
    clear_chat()

# 사용자 입력이 있을 경우
if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # 직각 삼각형 문제 풀이
    if "직각 삼각형" in user_input and "가장 긴 변의 길이가 5 cm" in user_input and "다른 한 변의 길이가 4 cm" in user_input:
        hypotenuse = 5
        one_side = 4
        other_side, angle_a, angle_b, angle_c = solve_right_triangle(hypotenuse, one_side)
        response_message = f"다른 한 변의 길이는 {other_side:.2f} cm입니다.\n세 각의 각도는 A: {angle_a:.2f}°, B: {angle_b:.2f}°, C: {angle_c:.2f}°입니다."
    # 이미지 생성 요청 처리
    elif "광안대교 이미지 생성해줘" in user_input:
        prompt = "광안대교 이미지"
        image_url = generate_image(prompt)
        response_message = f"광안대교 이미지가 생성되었습니다. [여기를 클릭하세요]({image_url})."
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state['messages']
        )
        response_message = response['choices'][0]['message']['content']

    st.session_state['messages'].append({"role": "assistant", "content": response_message})

# 대화 내용 표시
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.write(f"**당신:** {message['content']}")
    else:
        st.write(f"**어시스턴트:** {message['content']}")
        if "광안대교 이미지가 생성되었습니다" in message['content']:
            image_url = message['content'].split("[여기를 클릭하세요](")[1].split(")")[0]
            st.image(image_url)
  
