from rest_framework.routers import DefaultRouter


class OptionalSlashDefaultRouter(DefaultRouter):

    def __init__(self):
        super().__init__()
        # Set the trailing slash to be optional
        self.trailing_slash = '/?'