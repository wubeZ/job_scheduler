import argparse

def parse_args():
    """
    Parse command-line arguments for the job scheduler.

    Returns:
        - Parsed arguments as a Namespace object.
    """
    parser = argparse.ArgumentParser(
        description="Job Scheduler CLI - Configure and run the producer-consumer job scheduler."
    )

    parser.add_argument(
        "--producers", type=int, default=2, help="Number of producer threads (default: 2)"
    )
    parser.add_argument(
        "--consumers", type=int, default=3, help="Number of consumer threads (default: 3)"
    )
    parser.add_argument(
        "--jobs-per-producer", type=int, default=5, help="Number of jobs each producer will generate (default: 5)"
    )
    parser.add_argument(
        "--queue-size", type=int, default=10, help="Maximum size of the job queue (default: 10)"
    )
    parser.add_argument(
        "--dependency-chance", type=float, default=0.3,
        help="Chance (0-1) of jobs having dependencies (default: 0.3)"
    )
    parser.add_argument(
        "--log-level", type=str, default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)"
    )

    return parser.parse_args()

