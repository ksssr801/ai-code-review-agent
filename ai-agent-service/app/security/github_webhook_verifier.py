import hashlib
import hmac

from app.config import get_settings
from fastapi import HTTPException, Request

settings = get_settings()


def verify_github_signature(request: Request, body: bytes):
    """
    Verifies GitHub webhook signature using HMAC SHA256.
    """

    signature_header = request.headers.get("X-Hub-Signature-256")

    if not signature_header:
        raise HTTPException(status_code=401, detail="Missing signature")

    sha_name, signature = signature_header.split("=")

    if sha_name != "sha256":
        raise HTTPException(status_code=401, detail="Invalid signature type")

    mac = hmac.new(
        settings.github_webhook_secret.encode(),
        msg=body,
        digestmod=hashlib.sha256,
    )

    expected_signature = mac.hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
