from queue import Queue
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from models.job import Job
from utils.logger import get_logger

logger = get_logger(__name__)

class Consumer:
    """
    A consumer pool that fetches and processes jobs from the shared queue.
    """

    def __init__(self, queue: Queue, num_workers: int, completed_jobs: set, completed_jobs_lock: Lock) -> None:
        """
        Initialize the consumer pool.

        Args:
            - queue: The shared job queue.
            - num_workers: Number of worker threads.
            - completed_jobs: Shared set of completed job IDs.
            - completed_jobs_lock: Lock for accessing the completed jobs set.
        """
        self.queue = queue
        self.num_workers = num_workers
        self.completed_jobs = completed_jobs
        self.completed_jobs_lock = completed_jobs_lock
        self.executor = ThreadPoolExecutor(max_workers=num_workers)

    def process_job(self, job: Job) -> None:
        """
        Process a single job. This function is run by worker threads.
        
        Args:
            - job: The job to process.
        """
        try:
            if not job.can_execute(self.completed_jobs):
                logger.warning(f"Job {job.job_id} skipped due to unmet dependencies.")
                self.queue.put(job)  # Re-queue the job for later processing
                return

            job.execute()

            with self.completed_jobs_lock:
                self.completed_jobs.add(job.job_id)

        except Exception as e:
            logger.error(f"Error processing job {job.job_id}: {e}")

        finally:
            self.queue.task_done()

    def start(self) -> None:
        """
        Start consuming jobs from the queue.
        """
        while True:
            try:
                job = self.queue.get()
                self.executor.submit(self.process_job, job)
            except Exception as e:
                logger.error(f"Error fetching job: {e}")
                break

    def shutdown(self) -> None:
        """
        Shutdown the consumer pool gracefully.
        """
        self.executor.shutdown(wait=True)
        logger.info("Consumer pool has been shut down.")
