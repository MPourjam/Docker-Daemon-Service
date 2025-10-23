# Modular Web Service with Remote Docker Daemon
A modular and secure architecture for running tool-specific Docker images (e.g., TACTIC, PICRUSt2) inside a web service using Celery and a remote Docker daemon.

## Overview

This setup enables dynamic use of multiple Docker images as independent modules.
A remote Docker daemon (running as its own Docker service) manages and executes tool images.
Meanwhile, Celery interacts with this daemon using the Docker SDK for Python, allowing flexible and secure task orchestration.

### Key Advantages
#### Improved Security

- _No need_ to expose the local _Docker socket_ to containers.

- The Docker daemon can run in _rootless_ mode, minimizing privilege risks.

#### Simplified Integration
- No need to create APIs for each new tool or service.
- Tools execute directly via Docker SDK calls — no complex or risky API layers.

#### Real-Time Job Management
- Celery can monitor and display the status and logs of user jobs in real time.

#### Flexibility and Robustness
- Supports pulling images from private registries and running them by digest for immutability.
- Enables maintaining a modular repository of tools and versions.
- The remote Docker daemon can run on any host, accessible via the network.

## ⚙️ Quick Start
1. Clone the repository
```
git clone https://github.com/MPourjam/Docker-Daemon-Service.git
cd Remote-Daemon-Service
```

3. Build and start the services
```bash
docker compose up -d --build
```

Edit `tasks.py` or trigger a Celery task to run a Docker container remotely through the daemon.

🧪 Test Setup
File	Description
`docker-compose.yml`:	Defines the full Docker service setup → docker service and celery service
`start-celery.sh`:	Entrypoint script to start Celery and the Beat scheduler (as separate processes)
`tasks.py`:	Example Celery task running a remote Docker container and monitoring its status
`Dockerfile.picrust2`:	Example Dockerfile to build and register the picrust2 image (__optional__)

Note:
The Beat scheduler must be run as a separate process, not as part of the Celery worker (`celery -A tasks worker -l info -B`).
The provided script already follows this best practice.

✅ Status

This solution has been tested and verified to work seamlessly for orchestrating and monitoring modular tool containers via a secure, remote Docker environment.

