import os
import pytest
from app.services.chain import EMBEDDING


@pytest.fixture(scope="session")
def require_env():
    missing = [
        v for v in [
            "ASTRA_DB_API_ENDPOINT",
            "ASTRA_DB_APPLICATION_TOKEN",
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
        ]
        if not os.getenv(v)
    ]
    if missing:
        pytest.skip(f"Missing env vars: {', '.join(missing)}")


@pytest.fixture(scope="session")
def embedding(require_env):
    return EMBEDDING
