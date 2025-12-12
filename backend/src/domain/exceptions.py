class DomainException(Exception):
    pass

class UserAlreadyExistsException(DomainException):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists")

class InvalidCredentialsException(DomainException):
    def __init__(self):
        super().__init__("Invalid email or password")

class ProductIdeaNotFoundException(DomainException):
    def __init__(self, idea_id: str):
        super().__init__(f"Product idea {idea_id} not found")

class ResearchResultNotFoundException(DomainException):
    def __init__(self, result_id: str):
        super().__init__(f"Research result {result_id} not found")
