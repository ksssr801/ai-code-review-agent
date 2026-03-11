from app.agent.llm import generate_response
from app.config import Settings, get_settings
from app.logger_config import get_logger
from app.schemas.chat_models import ChatRequest, ChatResponse
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/chat", tags=["Chat"])

logger = get_logger(__name__)


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    settings: Settings = Depends(get_settings),
):
    """
    Endpoint for interacting with the general AI chat agent.
    """

    logger.info(
        "Received chat request",
        session_id=request.session_id,
        request_length=len(request.message),
    )

    try:
        response = await generate_response(request.message, settings)

    except Exception as e:

        logger.error(
            "Failed to generate response",
            error=str(e),
        )

        response = "Sorry, I couldn't generate a response."

    return ChatResponse(
        reply=response,
        session_id=request.session_id,
    )
