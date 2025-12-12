# Backend Implementation Plan

## Overview
This document outlines the architectural refinment and implementation plan for the Story LLM backend, following Hexagonal Architecture (Ports and Adapters) and Domain-Driven Design principles. The goal is to ensure a scalable, testable, and maintainable codebase.

## 1. Domain Layer Refinements

### Current State
- **Value Objects**: Implemented (`Email`, `Password`, `Content`, `FeasibilityScore`) and integrated into Entities.
- **Domain Events**: Basic event system (`ResearchCompleted`) implemented.
- **Entities**: Refactored to use Value Objects and Pydantic `BaseModel`.

### Improvements
- **Rich Domain Models**: Continue moving business logic to Entities where appropriate.

### File Changes
- `src/domain/entities.py`: Refactored to use Value Objects.
- `src/domain/value_objects.py`: Created.
- `src/domain/events.py`: Created.

## 2. Application Layer Improvements

### Current State
- Use Cases use Repository interfaces.
- `AuthService` and `WorkflowService` implemented.
- **Missing**: Strict DTO separation and Unit of Work pattern.

### Improvements
- **Strict DTO Separation**: Ensure Use Cases accept strict Input/Output DTOs that are distinct from Domain Entities and Web DTOs.
- **Unit of Work**: Introduce a `UnitOfWork` port to manage transactions effectively.
- **Service Refactoring**: Ensure services purely orchestrate domain objects and ports.

### File Changes
- `src/application/dto.py`: Define application-layer DTOs.
- `src/application/ports/unit_of_work.py`: Define UoW interface.
- `src/application/use_cases/`: Update services to use UoW and DTOs.

## 3. Infrastructure Layer Implementation

### Current State
- MongoDB repositories using Motor.
- **Pydantic Agent Adapter**: Implemented with retry logic (3 attempts) for robustness against provider failures.
- **Testing**: mocked `motor` drivers used in tests.

### Improvements
- **Repository Implementation**: Ensure Mongo repositories handle database-specific errors (DuplicateKey, ConnectionError) and translate them into Domain Exceptions.
- **Logging & Monitoring**: Integrate structured logging (Logfire/Opentelemetry) deeply into adapters to trace external calls.

### File Changes
- `src/infrastructure/adapters/repositories/`: Add error translation.

## 4. Web Layer & Testing

### Current State
- **Tests**: Comprehensive unit test suite implemented (`tests/domain`, `tests/application`, `tests/infrastructure`, `tests/web`). All tests passing (51 passed).
- **FastAPI Routers**: `auth` and `research` routers active.
- **Dependencies**: Dependency injection configured.

### Improvements
- **Integration Tests**: Add true integration tests using `Testcontainers` (or a local Docker Mongo) instead of mocking everything.
- **Error Handling Middleware**: Implement a global exception handler that maps Domain Exceptions to HTTP Status Codes uniformly.

### Specific Test Fix (Immediate Priority)
- **Resolved**: All immediate test failures resolved. `test_workflow_service.py` fixed to satisfy domain constraints.

## 5. Security

### Current State
- JWT Auth.
- Argon2 Hashing.

### Improvements
- **Rate Limiting**: Add `slowapi` or similar to prevent brute force on `/login`.
- **Token Blacklisting**: Implement logout functionality by blacklisting tokens.

## Actionable Next Steps

1.  **[COMPLETED] Fix Tests**: Updated `conftest.py` regarding stateful mocks.
2.  **[COMPLETED] Verify**: Ran `poetry run pytest`, resolved initial failures.
3.  **[COMPLETED] Refactor Domain**: Implemented Value Objects and updated Entities.
    - Created `src/domain/value_objects.py`.
    - Updated `src/domain/entities.py`.
4.  **[COMPLETED] Robustness**: Implemented retry logic in `PydanticAgentAdapter`.
5.  **[COMPLETED] Comprehensive Testing**: Added full unit test coverage for Domain, Application, and Infrastructure layers.
    - Added `tests/domain/*.py`
    - Added `tests/application/use_cases/*.py`
    - Added `tests/infrastructure/*.py`
    - Verified all 51 tests passed.
6.  **Application Layer**: Introduce DTOs and Unit of Work.
    - Define `src/application/dto.py`.
    - Define `src/application/ports/unit_of_work.py`.
    - Refactor Use Cases to use them.
7.  **Integration Testing**: Set up `Testcontainers` for true DB testing.
