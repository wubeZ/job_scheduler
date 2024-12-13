import threading
from scheduler.consumer import Consumer
from scheduler.queue import JobQueue
from models.job import Job

def test_consumer_processes_jobs():
    queue = JobQueue(maxsize=5)
    completed_jobs = set()
    completed_jobs_lock = threading.Lock()

    # Add jobs to the queue
    queue.put(Job(1, 1))
    queue.put(Job(2, 2))

    consumer = Consumer(queue, num_workers=1, completed_jobs=completed_jobs, completed_jobs_lock=completed_jobs_lock)
    consumer_thread = threading.Thread(target=consumer.start, daemon=True)
    consumer_thread.start()

    queue.queue.join()  # Wait for jobs to be processed
    consumer.shutdown()

    # Verify all jobs were completed
    assert len(completed_jobs) == 2
    assert 1 in completed_jobs
    assert 2 in completed_jobs
