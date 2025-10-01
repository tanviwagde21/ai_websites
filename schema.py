from pydantic import BaseModel
from typing import List, Dict

class WebsiteBlueprint(BaseModel):
    project_name: str
    pages: List[str]
    components: Dict[str, List[str]]  # page -> list of components
    style: str = "modern"
