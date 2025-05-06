from staging.services.projection_service import ProjectionService
from staging.commands.staging_commands import BuildProjectionCommand

class ProjectionQueryHandler:
    def __init__(self, projection_service: ProjectionService):
        self.projection_service = projection_service

    def handle(self, command: BuildProjectionCommand):
        return self.projection_service.build_projection(command.changeset_id, command.record_id)