# Job Scheduler

## Overview

The **Job Scheduler** is a multithreaded Python application that implements the **Producer-Consumer** pattern. It allows producers to generate jobs with optional dependencies, which are processed by consumers. The system handles dependency resolution, detects and resolves deadlocks, and supports customizable configurations via a Command-Line Interface (CLI).

## Features

- Multithreaded **Producer-Consumer** implementation using `threading` and `ThreadPoolExecutor`.
- Dependency management:
  - Jobs may have dependencies on other jobs.
  - Consumers process jobs only when their dependencies are resolved.
- Deadlock detection and resolution:
  - Circular dependencies are identified and resolved dynamically.
- CLI support for flexible configuration.
- Logging for detailed execution tracking.

## Requirements

- Python 3.8 or higher
- Dependencies (install via `setup.py` or manually):
  - None by default (adjust if additional libraries are used)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wubeZ/job_scheduler.git
   cd job_scheduler
    ```
2. Install the package:
    ```bash
    pip install .
    ```

## Usage

The **Job Scheduler** can be used via the CLI. Run the following command to see the available options:

```bash
job_scheduler --help
```

The CLI supports the following options:

| Option                   | Type    | Default  | Description                                                                                   |
|--------------------------|---------|----------|-----------------------------------------------------------------------------------------------|
| `--producers`            | Integer | `2`      | Number of producer threads to run.                                                           |
| `--consumers`            | Integer | `3`      | Number of consumer threads to run.                                                           |
| `--jobs-per-producer`    | Integer | `5`      | Number of jobs each producer will generate.                                                  |
| `--queue-size`           | Integer | `10`     | Maximum size of the shared job queue.                                                        |
| `--dependency-chance`    | Float   | `0.3`    | Probability (0-1) of each job having dependencies on other jobs.                             |
| `--log-level`            | String  | `INFO`   | Logging verbosity level. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.           |
| `-h, --help`             | Flag    | None     | Display the help message and list all available options.                                      |

---

To run the **Job Scheduler** with the default configuration, use the following command:

```bash
job_scheduler
```


## How It Works

1. **Producers**:
   - Producers generate a specified number of jobs.
   - Each job may depend on other jobs based on the `--dependency-chance` parameter.
   - Jobs are added to a shared, thread-safe queue.

2. **Queue**:
   - The queue acts as a central buffer between producers and consumers.
   - It has a fixed size (`--queue-size`), ensuring producers block when it’s full.

3. **Consumers**:
   - Consumers fetch jobs from the queue and process them.
   - Jobs are executed only when all their dependencies are resolved.

4. **Deadlock Handling**:
   - The system detects deadlocks caused by circular dependencies.
   - Deadlocked jobs have their dependencies removed to break the cycle.

5. **Logging**:
   - Logs provide detailed information about the system’s behavior.
   - Use `--log-level` to adjust the verbosity.

## Example Output

#### Command:
```bash
job_scheduler --producers 1 --consumers 1 --jobs-per-producer 3 --queue-size 5 --dependency-chance 0.3 --log-level INFO
```
#### Output:
```
2024-12-13 18:19:09,871 [INFO] MainThread: Starting job scheduler...
2024-12-13 18:19:09,871 [INFO] MainThread: Consumer pool started.
2024-12-13 18:19:09,871 [INFO] Thread-1: Adding job Producer-0-Job-0 to the queue.
2024-12-13 18:19:09,871 [INFO] MainThread: Producer-0 started.
2024-12-13 18:19:09,871 [INFO] Thread-1: Producer 0 created <Job id=Producer-0-Job-0, completed=False, dependencies=[]>
2024-12-13 18:19:09,871 [INFO] Thread-2 (start): Fetching job Producer-0-Job-0 from the queue.
2024-12-13 18:19:09,872 [INFO] ThreadPoolExecutor-0_0: Executing job Producer-0-Job-0 (Estimated time: 2s)
2024-12-13 18:19:10,095 [INFO] Thread-1: Adding job Producer-0-Job-1 to the queue.
2024-12-13 18:19:10,095 [INFO] Thread-1: Producer 0 created <Job id=Producer-0-Job-1, completed=False, dependencies=[]>
2024-12-13 18:19:10,095 [INFO] Thread-2 (start): Fetching job Producer-0-Job-1 from the queue.
2024-12-13 18:19:10,523 [INFO] Thread-1: Adding job Producer-0-Job-2 to the queue.
2024-12-13 18:19:10,523 [INFO] Thread-1: Producer 0 created <Job id=Producer-0-Job-2, completed=False, dependencies=[]>
2024-12-13 18:19:10,523 [INFO] Thread-2 (start): Fetching job Producer-0-Job-2 from the queue.
2024-12-13 18:19:10,694 [INFO] MainThread: Producer-0 finished.
2024-12-13 18:19:10,694 [INFO] MainThread: No deadlock detected.
2024-12-13 18:19:11,877 [INFO] ThreadPoolExecutor-0_0: Job Producer-0-Job-0 completed.
2024-12-13 18:19:11,877 [INFO] ThreadPoolExecutor-0_0: Job marked as completed in the queue.
2024-12-13 18:19:11,878 [INFO] ThreadPoolExecutor-0_0: Executing job Producer-0-Job-1 (Estimated time: 3s)
2024-12-13 18:19:14,883 [INFO] ThreadPoolExecutor-0_0: Job Producer-0-Job-1 completed.
2024-12-13 18:19:14,883 [INFO] ThreadPoolExecutor-0_0: Job marked as completed in the queue.
2024-12-13 18:19:14,883 [INFO] ThreadPoolExecutor-0_0: Executing job Producer-0-Job-2 (Estimated time: 3s)
2024-12-13 18:19:17,884 [INFO] ThreadPoolExecutor-0_0: Job Producer-0-Job-2 completed.
2024-12-13 18:19:17,884 [INFO] ThreadPoolExecutor-0_0: Job marked as completed in the queue.
2024-12-13 18:19:17,884 [INFO] MainThread: Consumer pool has been shut down.
2024-12-13 18:19:17,885 [INFO] MainThread: Job scheduler completed.

Completed jobs: ['Producer-0-Job-0', 'Producer-0-Job-1', 'Producer-0-Job-2']
```

## Testing

To run the tests, use the following command:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! 

1. Fork the repository.
2. Create a branch for your changes.
3. Commit and push your changes.
4. Open a pull request.

Please ensure all tests pass before submitting:
```bash
pytest tests/
```

## Future Enhancements

Here are some ideas for improving the Job Scheduler:

- **Priority Scheduling**: Allow jobs to have priorities so high-priority jobs are processed first.
- **Retry Mechanism**: Retry failed jobs a configurable number of times.
- **Real-Time Monitoring**: Add a dashboard or CLI updates to display queue and job statuses.
- **File-Based Job Definitions**: Support defining jobs and dependencies in a configuration file (e.g., JSON or YAML).
- **Distributed System**: Extend the scheduler to work across multiple nodes using tools like RabbitMQ or Celery.

Feel free to contribute if you'd like to work on any of these features!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, feedback, or collaboration, feel free to reach out:

- **Name**: Wubshet Zeleke
- **Email**: wubezelek@gmail.com
- **GitHub**: [wubeZ](https://github.com/wubeZ)


