"""Helper script to check if environment variables are loaded correctly"""
from src.config.settings import settings
import os

print("=" * 60)
print("Environment Variables Check")
print("=" * 60)
print(f"OPENAI_API_KEY: {'✓ Set' if settings.OPENAI_API_KEY else '✗ NOT SET'}")
print(f"OPENAI_BASE_URL: {settings.OPENAI_BASE_URL}")
print(f"MONGODB_URL: {settings.MONGODB_URL}")
print(f"MONGODB_DB: {settings.MONGODB_DB}")
print("=" * 60)

if not settings.OPENAI_API_KEY:
    print("\n⚠️  WARNING: OPENAI_API_KEY is not set!")
    print("Please add it to your .env file in the project root:")
    print("OPENAI_API_KEY=your_api_key_here")
else:
    print("\n✓ All required environment variables are set!")
