import anthropic
from typing import Dict, Any, Optional
import json
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL

class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None):
        """Claude AI 클라이언트 초기화"""
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("Anthropic API 키가 필요합니다. .env 파일에 ANTHROPIC_API_KEY를 설정하거나 직접 전달하세요.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = DEFAULT_MODEL
    
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
            response = self.client.messages.create(
                model=model or self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            return {
                "success": True,
                "content": response.content[0].text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "model": response.model
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
        
        system_prompt = f"""당신은 입찰제안서 개선 전문가입니다.
{enhancement_prompts.get(enhancement_type, "제안서를 개선해주세요.")}

개선 시 다음 사항을 고려하세요:
1. 원본의 핵심 내용 유지
2. 더 명확하고 구체적인 표현
3. 경쟁력 강화
4. 전문성 향상"""

        user_prompt = f"""원본 제안서:
{original_proposal}

{additional_info}

위 제안서를 개선해주세요."""

        return self.generate_proposal(system_prompt, user_prompt)
    
    def analyze_requirements(self, tender_document: str) -> Dict[str, Any]:
        """
        입찰 문서 분석
        
        Args:
            tender_document: 입찰 문서 내용
        
        Returns:
            분석 결과
        """
        system_prompt = """당신은 입찰 문서 분석 전문가입니다.
주어진 입찰 문서를 분석하여 다음 사항들을 추출해주세요:
1. 주요 요구사항
2. 평가 기준
3. 제출 서류
4. 주의사항
5. 우선순위가 높은 항목들"""

        user_prompt = f"""다음 입찰 문서를 분석해주세요:

{tender_document}

위 문서를 체계적으로 분석하여 제안서 작성에 필요한 핵심 정보를 추출해주세요."""

        return self.generate_proposal(system_prompt, user_prompt)
    
    def get_available_models(self) -> list:
        """사용 가능한 모델 목록 조회"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data if "claude" in model.id]
        except Exception as e:
            return [DEFAULT_MODEL] 