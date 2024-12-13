import threading
from scheduler.queue import JobQueue
from scheduler.producer import Producer
from scheduler.consumer import Consumer
from utils.logger import get_logger
from scheduler.deadlock import DeadlockHandler
import random


logger = get_logger(__name__)

class JobManager:
    """
    Orchestrates the job scheduling system, managing producers, consumers, and the job queue.
    """

    def __init__(self, num_producers: int, num_consumers: int, jobs_per_producer: int, queue_size: int, dependency_chance: float) -> None:
        """
        Initialize the JobManager with the required components.
        
        Args:
            - num_producers: Number of producer threads.
            - num_consumers: Number of consumer threads.
            - jobs_per_producer: Number of jobs each producer will generate.
            - queue_size: Maximum size of the job queue.
            - dependency_chance: Chance of jobs having dependencies.
        """

        self.queue = JobQueue(maxsize=queue_size)
        self.completed_jobs = set()
        self.completed_jobs_lock = threading.Lock()
        self.producers = [
            Producer(self.queue, jobs_per_producer, producer_id=i, max_execution_time=random.randint(1, 3), dependency_chance=dependency_chance)
            for i in range(num_producers)
        ]
        self.consumer = Consumer(
            self.queue, num_workers=num_consumers, completed_jobs=self.completed_jobs, completed_jobs_lock=self.completed_jobs_lock
        )
        self.all_jobs = []

    def start(self) -> None:
        """
        Start the producers and consumers.
        """
        logger.info("Starting job scheduler...")

        consumer_thread = threading.Thread(target=self.consumer.start, daemon=True)
        consumer_thread.start()
        logger.info("Consumer pool started.")
        
        for producer in self.producers:
            producer.start()
            logger.info(f"Producer-{producer.producer_id} started.")


        # Wait for all producers to finish
        for producer in self.producers:
            producer.join()
            logger.info(f"Producer-{producer.producer_id} finished.")
            self.all_jobs.extend(producer.generated_jobs)

        deadlocked_jobs = DeadlockHandler.detect_deadlock(self.all_jobs)
        if deadlocked_jobs:
            DeadlockHandler.resolve_deadlock(deadlocked_jobs, self.all_jobs)

        # Wait for all jobs in the queue to be processed
        self.queue.queue.join()

        self.consumer.shutdown()
        logger.info("Job scheduler completed.")

    def get_completed_jobs(self):
        """
        Get a list of all completed jobs.

        Returns:
            A sorted list of completed job IDs.
        """
        with self.completed_jobs_lock:
            return sorted(self.completed_jobs)

