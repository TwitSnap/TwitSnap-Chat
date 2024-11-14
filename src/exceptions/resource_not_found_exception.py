class ResourceNotFoundException(RuntimeError):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)
