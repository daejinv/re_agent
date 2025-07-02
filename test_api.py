import anthropic
import os

# API 키 설정
API_KEY = "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"

def test_api_connection():
    """API 연결 테스트"""
    try:
        # Anthropic 클라이언트 생성
        client = anthropic.Anthropic(api_key=API_KEY)
        
        # 간단한 메시지 전송 테스트
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "안녕하세요! API 연결 테스트입니다. 간단히 '연결 성공'이라고 답변해주세요."
                }
            ]
        )
        
        print("✅ API 연결 성공!")
        print(f"응답: {response.content[0].text}")
        print(f"모델: {response.model}")
        print(f"사용된 토큰: {response.usage.input_tokens} 입력, {response.usage.output_tokens} 출력")
        
        return True
        
    except Exception as e:
        print(f"❌ API 연결 실패: {str(e)}")
        return False

def test_proposal_generation():
    """제안서 생성 테스트"""
    try:
        client = anthropic.Anthropic(api_key=API_KEY)
        
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

        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        
        print("\n✅ 제안서 생성 테스트 성공!")
        print("=" * 50)
        print("생성된 제안서:")
        print("=" * 50)
        print(response.content[0].text)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 제안서 생성 테스트 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Anthropic API 연결 테스트 시작...")
    print(f"API 키: {API_KEY[:20]}...{API_KEY[-10:]}")
    print("-" * 50)
    
    # 기본 연결 테스트
    if test_api_connection():
        print("\n" + "=" * 50)
        # 제안서 생성 테스트
        test_proposal_generation()
    else:
        print("\n❌ API 키가 유효하지 않거나 연결에 문제가 있습니다.")
        print("다음 사항을 확인해주세요:")
        print("1. API 키가 올바른지 확인")
        print("2. 인터넷 연결 상태 확인")
        print("3. Anthropic 계정 상태 확인") 