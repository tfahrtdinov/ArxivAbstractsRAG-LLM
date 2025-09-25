from typing import Annotated

from fastapi import Depends, APIRouter

from src.schemas.schemas import AskRequestSchema, AskResponseSchema
from src.rag_service.rag_service import RAGService
from src.dependencies import get_rag_service

router = APIRouter()


@router.post("/")
def ask_llm(
    body: AskRequestSchema, rag_service: Annotated[RAGService, Depends(get_rag_service)]
) -> AskResponseSchema:
    return AskResponseSchema(answer=rag_service.get_llm_response(body.query))
