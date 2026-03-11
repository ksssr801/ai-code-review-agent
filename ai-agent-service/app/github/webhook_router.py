from app.agent.review_agent import start_review
from app.github.event_parser import should_trigger_review
from app.logger_config import get_logger
from app.schemas.webhook_models import WebhookPayload
from app.security.github_webhook_verifier import verify_github_signature
from fastapi import APIRouter, Request

logger = get_logger(__name__)

router = APIRouter(prefix="/github", tags=["GitHub"])


@router.post("/webhook")
async def github_webhook(request: Request):

    body = await request.body()

    verify_github_signature(request, body)

    payload = WebhookPayload.model_validate_json(body)

    logger.info(
        f"Webhook received: action={payload.action}, repo={payload.repository.full_name}"
    )

    if should_trigger_review(payload):

        await start_review(
            repo=payload.repository.full_name,
            pr_number=payload.pull_request.number,
        )

    return {"status": "received"}
