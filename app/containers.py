import os
from dotenv import load_dotenv
from dependency_injector import containers, providers

from app.config import ApplicationSettings
from app.databases import Database

from app.repository.user import UserRepository
from app.repository.quiz import QuizRepository

from app.service.user import UserService
from app.service.auth import AuthService
from app.service.quiz import QuizService

load_dotenv()

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.user",
            "app.api.auth",
            "app.api.quiz",
        ]
    )

    config = providers.Configuration()
    config.from_pydantic(ApplicationSettings())

    db = providers.Singleton(Database, db_url=config.db.db_url, echo=config.echo)

    auth_service = providers.Singleton(
        AuthService,
        secret_key=config.SECRET_KEY,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        auth_service=auth_service,
    )

    quiz_repository = providers.Factory(
        QuizRepository,
        session_factory=db.provided.session,
    )

    quiz_service = providers.Factory(
        QuizService,
        quiz_repository=quiz_repository,
    )

