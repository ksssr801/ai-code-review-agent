from app.config import get_settings
from app.github.github_client import GitHubClient
from app.logger_config import get_logger
from app.services.chunking_service import ChunkingService
from app.services.diff_extractor import DiffExtractor

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

    client = GitHubClient()
    files = await client.get_pull_request_files(repo, pr_number)

    logger.info(
        "PR files fetched",
        extra={
            "repository": repo,
            "pull_request": pr_number,
            "files": len(files),
        },
    )

    diffs = DiffExtractor.extract(files)
    logger.info(
        "Diffs extracted",
        extra={
            "repository": repo,
            "pull_request": pr_number,
            "diffs": len(diffs),
        },
    )

    chunks = ChunkingService.chunk_diffs(diffs)
    logger.info(
        "Chunks created",
        extra={
            "repository": repo,
            "pull_request": pr_number,
            "chunks": len(chunks),
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
