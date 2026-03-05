import json
from typing import List
from openai import OpenAI
from app.core.config import settings
from app.core.prompt import SYSTEM_PROMPT
from app.services.hardware_mgr import hardware_mgr

class LLMService:
    def __init__(self):
        self.client = None
        if settings.DOUBAO_API_KEY and settings.DOUBAO_ENDPOINT_ID:
            self.client = OpenAI(
                api_key=settings.DOUBAO_API_KEY,
                base_url=settings.DOUBAO_API_BASE,
            )
        self.system_prompt = SYSTEM_PROMPT

    def generate_code(self, query: str, modules: List[str]) -> dict:
        # Validate modules
        valid_modules = []
        invalid_modules = []
        
        components = hardware_mgr.get_all_components()
        component_map = {comp['name']: comp for comp in components}

        for mod in modules:
            if mod in component_map:
                valid_modules.append(component_map[mod])
            else:
                invalid_modules.append(mod)

        if invalid_modules:
            return {
                "connection": f"哎呀，找不到这些硬件：{', '.join(invalid_modules)}。请检查一下拼写哦！",
                "micropython_code": "# 硬件未找到",
                "mixly_steps": "请重新选择正确的硬件模块。"
            }

        # Prepare context for LLM
        hardware_context = "用户已选择的硬件信息：\n"
        for comp in valid_modules:
            hardware_context += f"- {comp['name']}: 引脚 {json.dumps(comp['pins'], ensure_ascii=False)}, 初始化代码: {comp.get('init_code', '')}\n"

        user_message = f"""
用户需求：{query}

{hardware_context}

请严格按照 JSON 格式返回，不要包含 markdown 格式标记：
{{
    "connection": "连接步骤说明...",
    "micropython_code": "完整的 MicroPython 代码...",
    "mixly_steps": "Mixly 操作步骤..."
}}
"""

        if not self.client:
            return self._mock_response(query, valid_modules)

        try:
            print(f"Calling Doubao API with model: {settings.DOUBAO_ENDPOINT_ID}")
            response = self.client.chat.completions.create(
                model=settings.DOUBAO_ENDPOINT_ID,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.1,
                top_p=0.3
            )
            
            content = response.choices[0].message.content
            # Clean up potential markdown formatting
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content.strip())
            
        except Exception as e:
            print(f"LLM API Error: {e}")
            return {
                "connection": "API 调用出错了，请检查配置。",
                "micropython_code": f"# Error: {str(e)}",
                "mixly_steps": "请检查后台日志。"
            }

    def _mock_response(self, query: str, valid_modules: List[dict]) -> dict:
        """Fallback mock response when API key is missing"""
        connection_str = "【演示模式】连接步骤：\n"
        init_code = ""
        for comp in valid_modules:
            connection_str += f"- {comp['name']}: {json.dumps(comp['pins'], ensure_ascii=False)}\n"
            init_code += f"# {comp['name']} 初始化\n{comp.get('init_code', '')}\n\n"
            
        micropython_code = f"""import time
from machine import Pin, PWM, ADC, SoftI2C

# 初始化代码
{init_code}

# 主循环
while True:
    # 这里是主逻辑，根据用户需求生成的
    # {query}
    print("Running in Mock Mode...")
    time.sleep(1)
"""
        return {
            "connection": connection_str,
            "micropython_code": micropython_code,
            "mixly_steps": "当前未配置 API Key，仅展示演示结果。"
        }

llm_service = LLMService()
