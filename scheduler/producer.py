
import threading
import random
import time
from models.job import Job
from utils.logger import get_logger
from queue import Queue


logger = get_logger(__name__)

class Producer(threading.Thread):
    """
    A producer thread that generates jobs and adds them to a shared queue.
    """

    def __init__(self, queue: Queue, job_count: int, producer_id: int, max_execution_time: int= 1, dependency_chance: float= 0.3) -> None:
        """
        Initialize the producer.

        Args:
            - queue: The shared job queue.
            - job_count: Number of jobs to produce.
            - producer_id: Unique identifier for this producer.
            - max_execution_time: Maximum simulated execution time for a job.
            - dependency_chance: Probability of a job having dependencies.
        """
        super().__init__()
        self.queue = queue
        self.job_count = job_count
        self.producer_id = producer_id
        self.max_execution_time = max_execution_time
        self.dependency_chance = dependency_chance
        self.created_jobs = []
        self.generated_jobs = []

    def run(self) -> None:
        """
        Generate jobs and add them to the queue.
        """
        for i in range(self.job_count):
            job_id = f"Producer-{self.producer_id}-Job-{i}"
            execution_time = random.randint(1, self.max_execution_time)

            # Randomly assign dependencies based on previous jobs
            dependencies = []
            if self.created_jobs and random.random() < self.dependency_chance:
                dependencies = random.sample(self.created_jobs, k=random.randint(1, len(self.created_jobs)))

            job = Job(job_id=job_id, execution_time=execution_time, dependencies=dependencies)
            self.queue.put(job)

            logger.info(f"Producer {self.producer_id} created {job}")
            self.created_jobs.append(job_id)
            self.generated_jobs.append(job)

            time.sleep(random.uniform(0.1, 0.5)) # Simulate time between job production
