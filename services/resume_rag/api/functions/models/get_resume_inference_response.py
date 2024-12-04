from pydantic import BaseModel

class GetResumeInferenceResponse(BaseModel):
    llm_response: str
    context_sources: list[str]
