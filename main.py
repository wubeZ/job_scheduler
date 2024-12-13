from scheduler.job_manager import JobManager
from cli.parser import parse_args
from utils.logger import set_log_level

def main():
    """
    Main entry point for the job scheduler.
    """
    args = parse_args()

    set_log_level(args.log_level)

    # Initialize the job manager with CLI arguments
    job_manager = JobManager(
        num_producers=args.producers,
        num_consumers=args.consumers,
        jobs_per_producer=args.jobs_per_producer,
        queue_size=args.queue_size,
        dependency_chance=args.dependency_chance,
    )

    # Start the job scheduler
    job_manager.start()

    # Retrieve and print completed jobs
    completed_jobs = job_manager.get_completed_jobs()
    print(f"\nCompleted jobs: {completed_jobs}")


if __name__ == "__main__":
    main()