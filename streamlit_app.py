import streamlit as st
import requests
import json

def call_api(user_input):
    url = "https://beta-llm-chainer.io.naver.com/v2/chain-completions"
    
    headers = {
        "x-api-key": "731ee770-7e1c-4df0-98de-3faa31ce04ae",
        "x-request-id": "dotori",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    data = {
        "chainId": "chain-beta-E6RHrB7MwGPPyLvFq6z1",
        "userInput": {
            "text": user_input
        },
        "prompts": {
            "systemPrompt": {
                "prompt": "- 보고서 목차를 작성한다.\r\n- 서론, 본론, 결론으로 나누어 체계적으로 목차를 작성한다.\r\n- 각 항목의 예제 문장을 함께 출력한다."
            }
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Streamlit 앱
st.title("보고서 목차 생성기")

user_input = st.text_input("보고서 주제를 입력하세요:", "탄소 중립을 위한 노력")

if st.button("목차 생성"):
    result = call_api(user_input)
    st.write(result)
