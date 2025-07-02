import google.generativeai as genai

# API 키 설정
API_KEY = "AIzaSyBQTovczMgxdVExbcstS7A-aLB2regABM4"

def test_api():
    try:
        print("🔍 API 테스트 시작...")
        genai.configure(api_key=API_KEY)
        
        # gemini-1.5-flash 모델 사용 (무료 할당량이 더 많음)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("안녕하세요! 간단한 테스트입니다.")
        
        print("✅ API 연결 성공!")
        print(f"응답: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ API 오류: {str(e)}")
        return False

if __name__ == "__main__":
    test_api() 