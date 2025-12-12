from pydantic import RootModel, Field, EmailStr, field_validator

class Email(RootModel):
    root: EmailStr
    
    def __str__(self):
        return str(self.root)
    
    def __eq__(self, other):
        return self.root == getattr(other, "root", getattr(other, "value", other))

class FeasibilityScore(RootModel):
    root: int = Field(ge=0, le=100)
    
    def __int__(self):
        return self.root

class Password(RootModel):
    """Raw password value object with validation rules."""
    root: str = Field(min_length=8)
    
    def __str__(self):
        return "***"

class HashedPassword(RootModel):
    """Represents a password that has been securely hashed."""
    root: str
    
    def __str__(self):
        return self.root

class Content(RootModel):
    """Product idea content with validation logic."""
    root: str
    
    @field_validator('root')
    @classmethod
    def validate_length(cls, v: str):
        if len(v.strip()) < 10:
            raise ValueError("Product idea must be at least 10 characters long")
        return v
    
    def __str__(self):
        return self.root
