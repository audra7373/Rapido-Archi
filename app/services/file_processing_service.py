import os
import shutil
from werkzeug.utils import secure_filename
from sqlmodel import select, Session
from app.database import engine
from app.models.rule import Rule
from app.models.department import Department
from app.models.file_log import FileLog

class FileProcessingService:
    
    @staticmethod
    def process_file(file, source_dir: str):
        """
        Saves the file temporarily, finds a matching rule,
        moves to target department folder, and logs the operation.
        """
        if not file or not file.filename:
            raise ValueError("No file provided")
            
        filename = secure_filename(file.filename)
        # Temp save
        temp_path = os.path.join(source_dir, filename)
        file.save(temp_path)
        
        file_ext = os.path.splitext(filename)[1].lower()
        
        with Session(engine) as session:
            try:
                # Find matching rule
                # Simple logic: First try to match by exact extension, or by keyword in filename
                statement = select(Rule)
                rules = session.exec(statement).all()
                
                matched_rule = None
                for rule in rules:
                    if rule.extension and rule.extension.lower() == file_ext:
                        matched_rule = rule
                        break
                    if rule.keyword and rule.keyword.lower() in filename.lower():
                        matched_rule = rule
                        break
                
                if not matched_rule:
                    # Log failure: No rule matched
                    log = FileLog(
                        filename=filename,
                        source_path=temp_path,
                        status="FAILED",
                        error_message="No matching rule found"
                    )
                    session.add(log)
                    session.commit()
                    return False, "No matching rule found"

                # Get department
                department = session.get(Department, matched_rule.department_id)
                if not department:
                    raise Exception("Rule associated with missing department")

                # Move file
                target_dir = department.target_path
                os.makedirs(target_dir, exist_ok=True)
                final_path = os.path.join(target_dir, filename)
                
                shutil.move(temp_path, final_path)
                
                # Log success
                log = FileLog(
                    filename=filename,
                    source_path=temp_path,
                    destination_path=final_path,
                    status="SUCCESS"
                )
                session.add(log)
                session.commit()
                return True, "File archived successfully"
                
            except Exception as e:
                # If something went wrong, try to log the failure
                log = FileLog(
                    filename=filename,
                    source_path=temp_path,
                    status="FAILED",
                    error_message=str(e)
                )
                session.add(log)
                session.commit()
                return False, str(e)
