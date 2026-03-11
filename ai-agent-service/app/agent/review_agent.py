from app.config import get_settings
from app.logger_config import get_logger

logger = get_logger(__name__)


async def start_review(repo: str, pr_number: int):
    """
    Entry point for the AI code review pipeline.
    """

    settings = get_settings()

    logger.info(
        "Starting AI review",
        extra={
            "repository": repo,
            "pull_request": pr_number,
            "model": settings.llm_model,
        },
    )

    # Future pipeline
    # 1 fetch PR diff
    # 2 parse files
    # 3 chunk large diffs
    # 4 send to LLM
    # 5 parse feedback
    # 6 post comments

    logger.info(
        "Review pipeline initialized",
        extra={"repository": repo, "pull_request": pr_number},
    )
