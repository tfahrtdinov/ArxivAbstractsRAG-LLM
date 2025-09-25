from pydantic import BaseModel, Field


class AskRequestSchema(BaseModel):
    query: str = Field(examples=["List me three examples of papers about RL"])


class AskResponseSchema(BaseModel):
    answer: str
