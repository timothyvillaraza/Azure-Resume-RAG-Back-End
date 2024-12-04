from pydantic import BaseModel

class ResumeInferenceModel(BaseModel):
    llm_response: str
    context_sources: list[str]