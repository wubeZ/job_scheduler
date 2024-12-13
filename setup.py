from setuptools import setup, find_packages

setup(
    name="job_scheduler",
    version="1.0.0",
    description="A multithreaded job scheduler implementing the Producer-Consumer pattern with deadlock handling.",
    author="Wubshet Zeleke",
    author_email="wubezeleke@gmail.com",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "job_scheduler=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
