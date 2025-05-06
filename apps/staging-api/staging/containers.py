from dependency_injector import containers, providers
from staging.handlers.staging_command_handler import StagingCommandHandler
from staging.handlers.staging_query_handler import StagingQueryHandler
from staging.services.staging_workflow_service import StagingWorkflowService
from staging.database import get_engine, get_session_factory
from staging.repositories.staging_repository import StagingRepository
from staging.services.projection_service import ProjectionService
from staging.handlers.projection_command_handler import ProjectionQueryHandler


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["staging.api.v1.staging.routes"]
    )

    # Database setup
    engine = providers.Singleton(get_engine)
    session_factory = providers.Singleton(get_session_factory, engine=engine)
    db_session = providers.Factory(lambda factory: factory(), session_factory)

    # Repository
    staging_repository = providers.Factory(
        StagingRepository,
        db=db_session,
    )

    # Services
    staging_workflow_service = providers.Factory(
        StagingWorkflowService,
    )

    projection_service = providers.Factory(
        ProjectionService,
        staging_repository=staging_repository,
    )

    # Handlers
    staging_command_handler = providers.Factory(
        StagingCommandHandler,
        db=db_session,
        workflow_service=staging_workflow_service,
    )

    staging_query_handler = providers.Factory(
        StagingQueryHandler,
        db=db_session,
    )

    projection_query_handler = providers.Factory(
        ProjectionQueryHandler,
        projection_service=projection_service,
    )