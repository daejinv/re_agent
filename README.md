# 🤖 서던포스트 AI 입찰제안서 챗봇

Google Gemini API 기반의 채팅형 입찰제안서 생성/분석/개선 챗봇입니다.

## ✨ 주요 기능
- **채팅형 UI**: 모든 기능을 AI와의 채팅으로 진행 (Streamlit 기반)
- **회사명 자동 반영**: 모든 답변/제안서/분석에 회사명 '서던포스트'가 자동 포함
- **입찰제안서, 분석, 개선, 문서작성 등**: 자연어로 요청하면 AI가 답변
- **대화 이력 다운로드**: 전체 대화 TXT로 저장 가능
- **웹 전용**: Streamlit 웹앱, 클라우드 배포 지원

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd re_agent
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
venv\Scripts\activate  # (Windows)
source venv/bin/activate  # (macOS/Linux)
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. Gemini API 키 설정
- `.env` 파일에 아래와 같이 입력하거나, 웹 UI에서 직접 입력
```
GEMINI_API_KEY=your_gemini_api_key_here
```
- [Google AI Studio](https://aistudio.google.com/app/apikey)에서 키 발급

### 5. 실행
```bash
streamlit run app.py
```
- 브라우저에서 `http://localhost:8501` 접속

## 🌐 웹 배포 가이드

### Streamlit Community Cloud (권장)
1. [https://streamlit.io/cloud](https://streamlit.io/cloud) 회원가입 및 로그인
2. GitHub 저장소 연결 후 배포
3. 환경변수(GEMINI_API_KEY) 설정

### Vercel, Render 등
- `requirements.txt`와 `app.py`만 있으면 대부분의 Python 웹 호스팅에서 바로 배포 가능
- 환경변수(GEMINI_API_KEY) 설정 필수

## 🖥️ 사용법

1. **채팅창에 자연어로 요청**
   - 예시: `입찰제안서 작성해줘`, `이 문서 분석해줘`, `문체를 더 설득력 있게 바꿔줘`
2. **AI가 답변**
   - 모든 답변/제안서에 회사명 '서던포스트'가 자동 반영됨
3. **대화 이력 다운로드**
   - 사이드바에서 TXT로 저장 가능

## 🏗️ 프로젝트 구조
```
re_agent/
├── app.py                 # 메인 Streamlit 채팅앱
├── gemini_client.py       # Gemini API 클라이언트 (회사명 자동 반영)
├── config.py              # 설정
├── requirements.txt       # Python 의존성
└── README.md              # 프로젝트 문서
```

## 💡 팁
- **회사명은 항상 '서던포스트'로 자동 반영** (입력할 필요 없음)
- **입찰제안서, 분석, 개선, 문서작성 등 모든 업무를 자연어로 요청**
- **최신 Gemini 모델로 쉽게 확장 가능**

## 📝 라이선스
MIT 