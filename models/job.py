import time
import threading
from utils.logger import get_logger

logger = get_logger(__name__)

class Job:
    """
    Represents a single unit of work (job) to be scheduled and executed.
    """
    def __init__(self, job_id: int, execution_time: int, dependencies : list | None =None) -> None:
        """
        Initialize a Job instance.

        Args:
            - job_id: Unique identifier for the job.
            - execution_time: Estimated time to complete the job.
            - dependencies: List of job IDs that this job depends on
        """
        self.job_id = job_id
        self.execution_time = execution_time
        self.dependencies = dependencies if dependencies else []
        self.is_completed = False
        self.lock = threading.Lock()

    def execute(self) -> None:
        """
        Simulate the execution of the job.
        This method sleeps for `execution_time` seconds to mimic work.
        """
        with self.lock:
            logger.info(f"Executing job {self.job_id} (Estimated time: {self.execution_time}s)")
            time.sleep(self.execution_time)
            self.is_completed = True
            logger.info(f"Job {self.job_id} completed.")
    

    def mark_complete(self) -> None:
        """
        Mark the job as completed in a thread-safe manner.
        """
        with self.lock:
            self.is_completed = True
            logger.info(f"Job {self.job_id} marked as complete.")

    
    def can_execute(self, completed_jobs: set) -> bool:
        """
        Check if the job can be executed based on its dependencies.
        
        Args: 
            - completed_jobs: Set of job IDs that have already completed
        
        Returns: 
            - True if the job can be executed, False otherwise
        """
        with self.lock:
            unmet_dependencies = [dep for dep in self.dependencies if dep not in completed_jobs]
            if unmet_dependencies:
                logger.warning(
                    f"Job {self.job_id} cannot execute due to unmet dependencies: {unmet_dependencies}"
                )
            return not unmet_dependencies
            
    def __repr__(self) -> str:
        return f"<Job id={self.job_id}, completed={self.is_completed}, dependencies={self.dependencies}>"

