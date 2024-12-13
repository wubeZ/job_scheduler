from queue import Queue
from utils.logger import get_logger
from models.job import Job
logger = get_logger(__name__)

class JobQueue:
    """
    A thread-safe, bounded queue for managing jobs between producers and consumers.
    """

    def __init__(self, maxsize: int=0) -> None:
        """
        Initialize a JobQueue instance with a fixed maximum size.

        Args:
            - maxsize: Maximum number of jobs that can be stored in the queue.
        """
        self.queue = Queue(maxsize)
    
    def put(self, job: Job) -> None:
        """
        Add a job to the queue. Blocks if the queue is full.

        Args:
            - job: Job instance to be added to the queue.
        """
        logger.info(f"Adding job {job.job_id} to the queue.")
        self.queue.put(job)

    def get(self) -> Job:
        """
        Retrieve a job from the queue. Blocks if the queue is empty.

        Returns:
            - Job instance removed from the queue.
        """
        job = self.queue.get()
        logger.info(f"Fetching job {job.job_id} from the queue.")
        return job
    
    def task_done(self) -> None:
        """
        Indicate that a previously fetched job has been completed.
        """
        self.queue.task_done()
        logger.info("Job marked as completed in the queue.")

    def qsize(self):
        """
        Get the current size of the queue.
        
        Returns:
            - The number of jobs currently in the queue.
        """
        size = self.queue.qsize()
        logger.info(f"Queue size: {size}")
        return size