from models.job import Job

def test_job_creation():
    job_0 = Job(job_id=0, execution_time=2)
    job = Job(job_id=1, execution_time=5, dependencies=[job_0.job_id])
    assert job.job_id == 1
    assert job.execution_time == 5
    assert job.dependencies == [0]
    assert job.is_completed is False

def test_can_execute():
    job_0 = Job(job_id=0, execution_time=2)
    job_1 = Job(job_id=1, execution_time=1, dependencies=[job_0.job_id])
    completed_jobs = {0}
    assert job_1.can_execute(completed_jobs) is True

    completed_jobs = set()
    assert job_1.can_execute(completed_jobs) is False

def test_execute():
    job = Job(job_id=1, execution_time=0)
    job.execute()
    assert job.is_completed is True

