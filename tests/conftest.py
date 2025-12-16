import pytest
from urllib.parse import urlparse
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

_pg = None
_redis = None

@pytest.fixture(scope="session")
def postgres_container():
    global _pg
    if _pg is None:
        _pg = (
            PostgresContainer("postgres:16-alpine")
            .with_env("POSTGRES_DB", "test_db")
            .with_env("POSTGRES_USER", "test_user")
            .with_env("POSTGRES_PASSWORD", "test_pass")
        )
        _pg.start()
    return _pg


@pytest.fixture(scope="session")
def redis_container():
    global _redis
    if _redis is None:
        _redis = RedisContainer("redis:7-alpine")
        _redis.start()
    return _redis

def pytest_unconfigure(config):
    global _pg
    if _pg is not None:
        _pg.stop()
        _pg = None
    
    global _redis
    if _redis is not None:
        _redis.stop()
        _redis = None
