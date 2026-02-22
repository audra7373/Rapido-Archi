from sqlmodel import select,Session
from app.models.department import Department
from app.database import engine


class DepartmentService:
    
    @staticmethod
    def create(name:str, target_path: str):
        with Session(engine) as session:
            department = Department(name=name,target_path=target_path)
            session.add(department)
            session.commit()
            session.refresh(department)
            return department
    
    @staticmethod
    def get_all():
        with Session(engine) as session:
            statement = select(Department)
            return session.exec(statement).all()

    @staticmethod
    def get_by_id(dept_id: int):
        with Session(engine) as session:
            return session.get(Department, dept_id)
        
    @staticmethod
    def delete(dept_id: int):
        with Session(engine) as session:
            department = session.get(department, dept_id)
            if not department:
                return False
            session.delete(department)
            session.commit()
            return True