from pydantic import BaseModel


class PullRequest(BaseModel):
    number: int


class Repository(BaseModel):
    full_name: str


class Label(BaseModel):
    name: str


class WebhookPayload(BaseModel):
    action: str
    repository: Repository
    pull_request: PullRequest
    label: Label | None = None
