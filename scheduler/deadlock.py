from utils.logger import get_logger
from collections import deque
from collections import defaultdict
from models.job import Job


logger = get_logger(__name__)

class DeadlockHandler:
    """
    Handles deadlock detection and resolution for jobs with dependencies.
    """

    @staticmethod
    def detect_deadlock(jobs: list[Job]) -> set[Job]:
        """
        Detect if a deadlock exists in the job dependency graph.
        Uses a topological sort (Kahn's algorithm) to detect cycles.

        Args:
            - jobs: List of all jobs.

        Returns:
            - A set of jobs IDs involved in a deadlock cycle, or an empty set if no deadlock exists.
        """
        
        graph = defaultdict(list) 
        in_degree = defaultdict(int)
        queue = deque()
        sorted_order = []

        
        for job in jobs:
            for dep_id in job.dependencies:
                graph[dep_id].append(job)
                in_degree[job.job_id] += 1

        for job in jobs:
            if in_degree[job.job_id] == 0:
                queue.append(job)

        while queue:
            current_job = queue.popleft()
            sorted_order.append(current_job)

            for next_job in graph[current_job.job_id]:
                in_degree[next_job.job_id] -= 1
                if in_degree[next_job.job_id] == 0:
                    queue.append(next_job)

        if len(sorted_order) != len(jobs):
            deadlocked_jobs = {job.job_id for job in jobs if in_degree[job.job_id] > 0}
            logger.warning(f"Deadlock detected involving jobs: {deadlocked_jobs}")
            return deadlocked_jobs

        logger.info("No deadlock detected.")
        return set()

    @staticmethod
    def resolve_deadlock(deadlocked_jobs: set, jobs: list[Job]) -> list[Job] | None:
        """
        Resolve deadlocks by removing dependencies or cancelling jobs.

        Args:
            - deadlocked_jobs: Set of job IDs involved in a deadlock.
            - jobs: List of all jobs.

        Returns:
            - Updated list of jobs with deadlock resolved.
        """
        
        if not deadlocked_jobs:
            logger.info("No deadlocked jobs to resolve.")
            return jobs



        for job in jobs:
            if job.job_id in deadlocked_jobs:
                job.dependencies = []
                logger.info(f"Removed dependencies for job {job.job_id} to resolve deadlock.")
        
        return jobs

