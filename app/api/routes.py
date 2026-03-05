from fastapi import APIRouter, HTTPException
from app.models.schemas import GenerateCodeRequest, GenerateCodeResponse
from app.services.llm import llm_service
from app.services.hardware_mgr import hardware_mgr

router = APIRouter()

@router.get("/esp32/components")
async def get_components():
    """
    Get all available hardware components.
    """
    return hardware_mgr.get_all_components()

@router.post("/esp32/generate-code", response_model=GenerateCodeResponse)
async def generate_code(request: GenerateCodeRequest):
    """
    Generate ESP32-S3 MicroPython code and wiring instructions.
    """
    try:
        result = llm_service.generate_code(request.user_query, request.selected_modules)
        return GenerateCodeResponse(
            connection=result["connection"],
            micropython_code=result["micropython_code"],
            mixly_steps=result["mixly_steps"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
