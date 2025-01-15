import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
    return model

def main():
    st.title("🤖 심리상담 챗봇")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        # PDF 파일 업로드
        uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
        
        if uploaded_file:
            pdf_text = extract_text_from_pdf(uploaded_file)
            st.success("PDF 파일이 성공적으로 업로드되었습니다!")
            
            # 챗봇 초기화
            model = init_gemini(api_key)
            
            # 채팅 기록 초기화
            if "messages" not in st.session_state:
                st.session_state.messages = []
                
            # 채팅 기록 표시
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # 사용자 입력
            if prompt := st.chat_input("무엇을 도와드릴까요?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # 컨텍스트 설정
                context = f"""
                당신은 전문 심리상담사입니다. 다음 문서를 참고하여 사용자의 질문에 답변해주세요:
                {pdf_text}
                
                사용자의 질문: {prompt}
                """
                
                # Gemini 응답 생성
                with st.chat_message("assistant"):
                    response = model.generate_content(context)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

if __name__ == "__main__":
    main()
