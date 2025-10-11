import os
import pathlib
from functools import lru_cache


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent

    DATABASE_URL: str = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/sqlite.db")
    DATABASE_CONNECT_DICT: dict = {}

    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
    result_backend: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")  

    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://redis:6379/0")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
