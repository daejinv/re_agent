import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Gemini API 키
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBQTovczMgxdVExbcstS7A-aLB2regABM4")

# 기본 모델 설정
DEFAULT_MODEL = "gemini-1.5-flash"

# 프롬프트 템플릿 설정
PROMPT_TEMPLATES = {
    "기본": {
        "system_prompt": """당신은 입찰제안서 작성 전문가입니다. 
주어진 정보를 바탕으로 고품질의 입찰제안서를 작성해주세요.
다음 사항들을 고려하여 작성하세요:
1. 명확하고 구체적인 내용
2. 경쟁력 있는 제안
3. 전문적이고 신뢰할 수 있는 톤
4. 구조화된 형식""",
        "user_prompt_template": """다음 정보를 바탕으로 입찰제안서를 작성해주세요:

**입찰 정보:**
- 입찰명: {tender_name}
- 입찰기관: {organization}
- 사업규모: {project_scale}
- 사업기간: {project_period}

**회사 정보:**
- 회사명: {company_name}
- 주요사업: {main_business}
- 경험사례: {experience}

**특별 요구사항:**
{special_requirements}

위 정보를 바탕으로 전문적이고 경쟁력 있는 입찰제안서를 작성해주세요."""
    },
    
    "기술제안서": {
        "system_prompt": """당신은 기술제안서 작성 전문가입니다.
기술적 우수성과 실행 가능성을 강조하는 기술제안서를 작성해주세요.
다음 사항들을 포함하세요:
1. 기술적 접근 방법
2. 프로젝트 관리 방안
3. 품질 보증 체계
4. 위험 관리 방안""",
        "user_prompt_template": """다음 정보를 바탕으로 기술제안서를 작성해주세요:

**프로젝트 정보:**
- 프로젝트명: {project_name}
- 기술 요구사항: {technical_requirements}
- 납기일: {delivery_date}

**회사 역량:**
- 기술력: {technical_capability}
- 인력 구성: {human_resources}
- 관련 경험: {related_experience}

**특별 고려사항:**
{special_considerations}

기술적 우수성과 실행 가능성을 강조한 기술제안서를 작성해주세요."""
    },
    
    "가격제안서": {
        "system_prompt": """당신은 가격제안서 작성 전문가입니다.
경쟁력 있는 가격과 합리적인 비용 구조를 제시하는 가격제안서를 작성해주세요.
다음 사항들을 포함하세요:
1. 상세한 비용 분석
2. 가격 경쟁력
3. 비용 절감 방안
4. 투명한 가격 구조""",
        "user_prompt_template": """다음 정보를 바탕으로 가격제안서를 작성해주세요:

**사업 정보:**
- 사업명: {business_name}
- 예산 범위: {budget_range}
- 사업 규모: {business_scale}

**비용 구성:**
- 인건비: {labor_cost}
- 재료비: {material_cost}
- 간접비: {overhead_cost}

**특별 조건:**
{special_conditions}

경쟁력 있고 합리적인 가격제안서를 작성해주세요."""
    }
} 