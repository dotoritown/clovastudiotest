import streamlit as st
import requests
import json
import time

def call_api(system_prompt, user_input):
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
                "prompt": system_prompt
            }
        }
    }
    
    try:
        with st.spinner('API 요청 처리 중...'):
            response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "API 요청 시간이 초과되었습니다. 나중에 다시 시도해주세요."}
    except requests.exceptions.RequestException as e:
        return {"error": f"API 요청 중 오류가 발생했습니다: {str(e)}"}

# Streamlit 앱
st.title("API 요청")

system_prompt = st.text_area("System Prompt를 입력하세요:", 
                             "- 보고서 목차를 작성한다.\n- 서론, 본론, 결론으로 나누어 체계적으로 목차를 작성한다.\n- 각 항목의 예제 문장을 함께 출력한다.",
                             height=150)

user_input = st.text_input("User Input을 입력하세요:", "보고서 주제: 탄소 중립을 위한 노력")

if st.button("API 호출"):
    result = call_api(system_prompt, user_input)
    if "error" in result:
        st.error(result["error"])
    else:
        st.success("API 호출 성공!")
        
        # 결과 표시
        st.subheader("API 응답 결과:")
        
        # 응답에서 텍스트 추출 (실제 구조에 따라 조정 필요)
        if "completions" in result and result["completions"]:
            response_text = result["completions"][0].get("text", "텍스트 없음")
            st.write(response_text)
        else:
            st.write("응답에서 텍스트를 찾을 수 없습니다.")
        
        # 전체 JSON 응답 표시
        st.subheader("전체 응답:")
        st.json(result)

# 디버깅을 위한 정보 표시
st.sidebar.title("디버그 정보")
st.sidebar.json({
    "System Prompt": system_prompt,
    "User Input": user_input
})
