from scheduler.producer import Producer
from scheduler.queue import JobQueue

def test_producer_generates_jobs():
    queue = JobQueue(maxsize=10)
    producer = Producer(queue, job_count=3, producer_id=1)
    producer.start()
    producer.join()

    # Ensure 3 jobs were added to the queue
    assert queue.queue.qsize() == 3

    # Validate job details
    while not queue.queue.empty():
        job = queue.queue.get()
        assert job.job_id.startswith("Producer-1-Job-")
        assert isinstance(job.execution_time, int)
