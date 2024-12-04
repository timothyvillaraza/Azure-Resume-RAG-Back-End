from pydantic import BaseModel

class GetResumeInferenceRequest(BaseModel):
    query: str