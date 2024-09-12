from pydantic import BaseModel

class ScriptUpload(BaseModel):
    script_content: str
