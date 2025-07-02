import google.generativeai as genai
from typing import Dict, Any, Optional
import json
from config import GEMINI_API_KEY, DEFAULT_MODEL

COMPANY_NAME = "서던포스트"

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        """Gemini AI 클라이언트 초기화"""
        self.api_key = api_key or GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API 키가 필요합니다. .env 파일에 GEMINI_API_KEY를 설정하거나 직접 전달하세요.")
        
        # Gemini API 설정
        genai.configure(api_key=self.api_key)
        self.model = DEFAULT_MODEL
    
    def _prepend_company(self, prompt: str) -> str:
        # 모든 프롬프트에 회사명 안내 추가
        company_info = f"\n\n[참고: 우리 회사명은 '{COMPANY_NAME}'입니다. 모든 답변, 제안서, 분석에 반드시 이 회사명을 반영하세요.]"
        return prompt + company_info

    def generate_chat(self, messages, model: Optional[str] = None, max_tokens: int = 8192, temperature: float = 0.7) -> Dict[str, Any]:
        """
        채팅형 대화 지원 (messages: [{role, content}])
        """
        try:
            gemini_model = genai.GenerativeModel(
                model_name=model or self.model,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            # 마지막 user 메시지에 회사명 자동 추가
            chat_messages = []
            for m in messages:
                if m["role"] == "user":
                    chat_messages.append({"role": "user", "parts": [self._prepend_company(m["content"])]})
                else:
                    chat_messages.append({"role": m["role"], "parts": [m["content"]]})
            response = gemini_model.generate_content(chat_messages)
            # finish_reason 안전하게 추출
            finish_reason = None
            try:
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'finish_reason'):
                        finish_reason = candidate.finish_reason
                    elif isinstance(candidate, dict):
                        finish_reason = candidate.get('finish_reason', None)
            except Exception as e:
                print("finish_reason 추출 오류:", e)
                finish_reason = None
            reached_limit = (finish_reason == 'MAX_TOKENS' or finish_reason == 'LENGTH')
            return {
                "success": True,
                "content": response.text,
                "usage": {},
                "model": model or self.model,
                "reached_limit": reached_limit
            }
        except Exception as e:
            return {"success": False, "error": str(e), "content": None, "reached_limit": False}

    def generate_proposal(self, 
                         system_prompt: str, 
                         user_prompt: str, 
                         model: Optional[str] = None,
                         max_tokens: int = 4000,
                         temperature: float = 0.7) -> Dict[str, Any]:
        """
        입찰제안서 생성
        
        Args:
            system_prompt: 시스템 프롬프트
            user_prompt: 사용자 프롬프트
            model: 사용할 모델명
            max_tokens: 최대 토큰 수
            temperature: 창의성 조절 (0.0-1.0)
        
        Returns:
            API 응답 결과
        """
        try:
            # Gemini 모델 생성
            gemini_model = genai.GenerativeModel(
                model_name=model or self.model,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            # 전체 프롬프트 구성
            full_prompt = self._prepend_company(f"{system_prompt}\n\n{user_prompt}")
            
            # 응답 생성
            response = gemini_model.generate_content(full_prompt)
            
            return {
                "success": True,
                "content": response.text,
                "usage": {
                    "input_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "output_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0
                },
                "model": model or self.model
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": None
            }
    
    def enhance_proposal(self, 
                        original_proposal: str, 
                        enhancement_type: str,
                        additional_info: str = "") -> Dict[str, Any]:
        """
        기존 제안서 개선
        
        Args:
            original_proposal: 원본 제안서
            enhancement_type: 개선 유형 (문체, 구조, 내용 등)
            additional_info: 추가 정보
        
        Returns:
            개선된 제안서
        """
        enhancement_prompts = {
            "문체": "다음 제안서의 문체를 더 전문적이고 설득력 있게 개선해주세요.",
            "구조": "다음 제안서의 구조를 더 체계적이고 읽기 쉽게 개선해주세요.",
            "내용": "다음 제안서의 내용을 더 구체적이고 경쟁력 있게 개선해주세요.",
            "길이": "다음 제안서를 요구사항에 맞게 길이를 조정해주세요."
        }
        
        system_prompt = f"""당신은 입찰제안서 개선 전문가입니다.\n{enhancement_prompts.get(enhancement_type, '제안서를 개선해주세요.')}\n\n개선 시 다음 사항을 고려하세요:\n1. 원본의 핵심 내용 유지\n2. 더 명확하고 구체적인 표현\n3. 경쟁력 강화\n4. 전문성 향상"""

        user_prompt = f"""원본 제안서:\n{original_proposal}\n\n{additional_info}\n\n위 제안서를 개선해주세요."""

        return self.generate_proposal(system_prompt, user_prompt)
    
    def analyze_requirements(self, tender_document: str) -> Dict[str, Any]:
        """
        입찰 문서 분석
        
        Args:
            tender_document: 입찰 문서 내용
        
        Returns:
            분석 결과
        """
        system_prompt = """당신은 입찰 문서 분석 전문가입니다.\n주어진 입찰 문서를 분석하여 다음 사항들을 추출해주세요:\n1. 주요 요구사항\n2. 평가 기준\n3. 제출 서류\n4. 주의사항\n5. 우선순위가 높은 항목들"""

        user_prompt = f"""다음 입찰 문서를 분석해주세요:\n\n{tender_document}\n\n위 문서를 체계적으로 분석하여 제안서 작성에 필요한 핵심 정보를 추출해주세요."""

        return self.generate_proposal(system_prompt, user_prompt)
    
    def get_available_models(self) -> list:
        """사용 가능한 모델 목록 조회"""
        try:
            models = genai.list_models()
            gemini_models = [model.name for model in models if "gemini" in model.name]
            return gemini_models if gemini_models else [DEFAULT_MODEL]
        except Exception as e:
            return [DEFAULT_MODEL] 