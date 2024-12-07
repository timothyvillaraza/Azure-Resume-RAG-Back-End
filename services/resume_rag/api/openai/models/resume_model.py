from typing import List, Optional
from pydantic import BaseModel, Field


class ResponsibilityModel(BaseModel):
    skills: List[str] = Field(..., description="The tech stack and skills involved with the description of the task. The more, the better.")
    description: str = Field(..., description="The word for word description of the responsibility.")
    ai_extended_description: str = Field(..., description="The description extended with as many releveant technical descriptions and keywords related to the tech stack of length 300 <= number of words <= 400 to enhance vector search.")


class ProfessionalExperienceModel(BaseModel):
    company: str
    location: str
    role: str
    team: Optional[str]
    duration: str
    responsibilities: List[ResponsibilityModel]


class ProjectModel(BaseModel):
    name: str
    date: str
    description: str
    achievement: Optional[str] = None


class EducationModel(BaseModel):
    institution: str
    degree: str
    concentration: Optional[str]
    honors: Optional[str]
    graduation_date: str


class CertificationModel(BaseModel):
    name: str
    date: str


class SkillsModel(BaseModel):
    programming_languages: List[str]
    frameworks: List[str]
    cloud: List[str]
    proficiencies: List[str]


class PersonalInfoModel(BaseModel):
    name: str
    linkedin: str
    github: str
    note: Optional[str]


class ResumeModel(BaseModel):
    personal_info: PersonalInfoModel
    skills: SkillsModel
    professional_experience: List[ProfessionalExperienceModel]
    projects: List[ProjectModel]
    education: EducationModel
    certifications: List[CertificationModel]