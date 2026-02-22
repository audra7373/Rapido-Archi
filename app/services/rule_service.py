from sqlmodel import select, Session
from app.database import engine
from app.models.rule import Rule
from app.models.department import Department

class RuleService:
    
    @staticmethod
    def create(extension: str | None,
               keyword: str | None,
               department_id: int):
        with Session(engine) as session:
            
            #Check the department exist
            department = session.get(Department, department_id)
            if not department:
                raise ValueError("Department not found")
            rule = Rule(
                extension=extension,
                keyword=keyword,
                department_id=department
            )
            
            session.add(rule)
            session.commit()
            session.refresh(rule)
            return rule
        