import threading
from scheduler.job_manager import JobManager
from scheduler.queue import JobQueue
from scheduler.deadlock import DeadlockHandler
from models.job import Job

def test_scheduler():
    """
    Integration test for the entire job scheduler.
    """
    
    num_producers = 2
    num_consumers = 2
    jobs_per_producer = 3
    queue_size = 10

    job_manager = JobManager(
        num_producers=num_producers,
        num_consumers=num_consumers,
        jobs_per_producer=jobs_per_producer,
        queue_size=queue_size,
        dependency_chance=0.3
    )

    job_manager.start()

    completed_jobs = job_manager.get_completed_jobs()
    
    assert len(completed_jobs) == num_producers * jobs_per_producer

    assert len(completed_jobs) == len(set(completed_jobs))

