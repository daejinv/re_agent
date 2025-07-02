import google.generativeai as genai
import os

# API 키 설정
API_KEY = "AIzaSyBQTovczMgxdVExbcstS7A-aLB2regABM4"

def test_api_connection():
    """API 연결 테스트"""
    try:
        # Gemini API 설정
        genai.configure(api_key=API_KEY)
        
        # 모델 생성 (gemini-1.5-flash 사용)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 간단한 메시지 전송 테스트
        response = model.generate_content("안녕하세요! API 연결 테스트입니다. 간단히 '연결 성공'이라고 답변해주세요.")
        
        print("✅ Gemini API 연결 성공!")
        print(f"응답: {response.text}")
        print(f"모델: gemini-1.5-flash")
        
        return True
        
    except Exception as e:
        print(f"❌ API 연결 실패: {str(e)}")
        return False

def test_proposal_generation():
    """제안서 생성 테스트"""
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        system_prompt = """당신은 입찰제안서 작성 전문가입니다. 
주어진 정보를 바탕으로 고품질의 입찰제안서를 작성해주세요."""

        user_prompt = """다음 정보를 바탕으로 입찰제안서를 작성해주세요:

**입찰 정보:**
- 입찰명: 2024년 IT 시스템 구축 사업
- 입찰기관: 서울시청
- 사업규모: 5억원
- 사업기간: 2024.01 ~ 2024.12

**회사 정보:**
- 회사명: (주)테크솔루션
- 주요사업: IT 시스템 구축, 소프트웨어 개발
- 경험사례: 다수의 공공기관 IT 시스템 구축 경험

위 정보를 바탕으로 전문적이고 경쟁력 있는 입찰제안서를 작성해주세요."""

        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = model.generate_content(full_prompt)
        
        print("\n✅ 제안서 생성 테스트 성공!")
        print("=" * 50)
        print("생성된 제안서:")
        print("=" * 50)
        print(response.text)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 제안서 생성 테스트 실패: {str(e)}")
        return False

def test_available_models():
    """사용 가능한 모델 확인"""
    try:
        genai.configure(api_key=API_KEY)
        models = genai.list_models()
        
        print("\n📋 사용 가능한 Gemini 모델:")
        for model in models:
            if "gemini" in model.name:
                print(f"- {model.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 모델 목록 조회 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Gemini API 연결 테스트 시작...")
    print(f"API 키: {API_KEY[:20]}...{API_KEY[-10:]}")
    print("-" * 50)
    
    # 기본 연결 테스트
    if test_api_connection():
        print("\n" + "=" * 50)
        # 제안서 생성 테스트
        test_proposal_generation()
        print("\n" + "=" * 50)
        # 사용 가능한 모델 확인
        test_available_models()
    else:
        print("\n❌ API 키가 유효하지 않거나 연결에 문제가 있습니다.")
        print("다음 사항을 확인해주세요:")
        print("1. API 키가 올바른지 확인")
        print("2. 인터넷 연결 상태 확인")
        print("3. Google AI Studio 계정 상태 확인") 