from app.config import get_settings
from app.schemas.webhook_models import WebhookPayload

settings = get_settings()


def should_trigger_review(payload: WebhookPayload) -> bool:
    """
    Determines whether an AI review should run.
    """

    action = payload.action

    label_name = None
    if payload.label:
        label_name = payload.label.name

    if action == "opened":
        return True

    if action == "synchronize":
        return True

    if action == "labeled" and label_name == settings.ai_review_label:
        return True

    return False
