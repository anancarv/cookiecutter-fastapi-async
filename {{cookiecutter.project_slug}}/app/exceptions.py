from app.schemas import ErrorModel


class ModelNotFoundException(Exception):
    def __init__(self, error: ErrorModel):
        super().__init__(f"{error.class_name} {error.value} not found")
