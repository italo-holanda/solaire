from backend.core.common.domain.entities.entity import Entity


class ApplicationException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.entity = Entity()  # or whatever initialization is needed
        self.code = code
        self.message = message

    def to_json(self):
        return {"code": self.code, "message": self.message}
