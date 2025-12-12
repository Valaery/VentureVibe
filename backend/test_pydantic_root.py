from pydantic import BaseModel, RootModel, EmailStr
import json

class Email(RootModel):
    root: EmailStr

class User(BaseModel):
    email: Email

try:
    print("Trying init from string...")
    u2 = User(email="test@example.com") 
    print(f"Init from str: {u2.model_dump()}")
except Exception as e:
    print(f"Error init from str: {e}")
