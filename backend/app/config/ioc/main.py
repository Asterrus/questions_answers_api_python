from app.config.ioc.providers.db_mapper import db_mapper_provider
from app.config.ioc.providers.mapper import mapper_provider
from app.config.ioc.providers.repository import repository_provider
from app.config.ioc.providers.request_mapper import request_mapper_provider
from app.config.ioc.providers.session import SessionProvider
from app.config.ioc.providers.use_case import use_case_provider


def get_providers():
    return [
        SessionProvider(),
        repository_provider,
        use_case_provider,
        mapper_provider,
        db_mapper_provider,
        request_mapper_provider,
    ]
