from scheduler.queue import JobQueue
from models.job import Job

def test_job_queue_operations():
    queue = JobQueue(maxsize=3)
    job1 = Job(1, 2)
    job2 = Job(2, 3)

    queue.put(job1)
    queue.put(job2)

    # Verify queue size
    assert queue.queue.qsize() == 2

    # Fetch jobs and validate
    fetched_job1 = queue.get()
    assert fetched_job1.job_id == 1
    fetched_job2 = queue.get()
    assert fetched_job2.job_id == 2

    # Verify queue is empty
    assert queue.queue.empty()

