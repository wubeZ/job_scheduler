from scheduler.deadlock import DeadlockHandler
from models.job import Job

def test_deadlock_detection():
    jobs = [
        Job(1, 2, dependencies=[2]),
        Job(2, 3, dependencies=[3]),
        Job(3, 1, dependencies=[1]),  # Circular dependency
    ]
    deadlocked_jobs = DeadlockHandler.detect_deadlock(jobs)
    assert len(deadlocked_jobs) == 3
    assert 1 in {job_id for job_id in deadlocked_jobs}
    assert 2 in {job_id for job_id in deadlocked_jobs}
    assert 3 in {job_id for job_id in deadlocked_jobs}

def test_deadlock_resolution():
    jobs = [
        Job(1, 2, dependencies=[2]),
        Job(2, 3, dependencies=[3]),
        Job(3, 1, dependencies=[1]),  # Circular dependency
    ]
    deadlocked_jobs = DeadlockHandler.detect_deadlock(jobs)
    
    DeadlockHandler.resolve_deadlock(deadlocked_jobs, jobs)

    # Verify dependencies were removed
    check_deadlock = DeadlockHandler.detect_deadlock(jobs)
    
    assert len(check_deadlock) == 0

