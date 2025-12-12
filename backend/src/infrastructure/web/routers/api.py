from fastapi import APIRouter, Depends, HTTPException
from src.infrastructure.web.dtos.schemas import ResearchRequest, ResearchResponse
from src.application.use_cases.workflow_service import WorkflowService
from src.infrastructure.web.dependencies import get_workflow_service, get_current_user
from src.domain.entities import User

router = APIRouter(prefix="/research", tags=["research"])

@router.post("/", response_model=ResearchResponse)
async def create_research(
    request: ResearchRequest,
    current_user: User = Depends(get_current_user),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    # Depending on agent speed, this might be slow for a synchronous HTTP request.
    # In production, use background tasks or Celery. For this task, async await is okay.
    return await workflow_service.execute_research(current_user.id, request.content, request.target_audience)

@router.get("/{idea_id}", response_model=ResearchResponse)
async def get_research(
    idea_id: str,
    current_user: User = Depends(get_current_user),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    result = await workflow_service.get_result(idea_id) # assuming get_result takes idea_id
    if not result:
        raise HTTPException(status_code=404, detail="Research not found")
    return result
