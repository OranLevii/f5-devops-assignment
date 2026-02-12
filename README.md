## Project Overview

The goal was to create a containerized web server that handles different types of traffic safely and reliably.

* **HTTP (Port 8080):** Serves a custom "Solved" page.
* **HTTPS (Port 443):** Securely serves content using SSL certificates.
* **Error Handling (Port 8081):** Simulates a Server Error (500) for testing.

To ensure stability, I built a **Tester Container** that runs alongside the server and automatically validates connectivity and SSL handshakes.

---

## How to Build and Run

I designed this project to be secure by default. **Private keys are NOT included in the repository**, so you will generate them locally before running.

### Prerequisites
* Docker Desktop (or Docker Engine)
* OpenSSL (usually installed by default)
* Git

### Step-by-Step Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/OranLevii/f5-devops-assignment.git
    ```

2.  **Generate SSL Certificates:**
    Run this command to generate a temporary certificate for testing:
    ```bash
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx_server/nginx.key \
        -out nginx_server/nginx.crt \
        -subj "/C=US/ST=State/L=City/O=DevOps/OU=Internship/CN=localhost"
    ```

3.  **Run with Docker Compose:**
    Now that the keys exist, build and start the environment:
    ```bash
    docker compose up --build
    ```

4.  **Watch the Test:**
    You will see the logs in your terminal.
    * The **`nginx_server`** will start.
    * The **`tester`** container will wait for Nginx to initialize.
    * The tester will verify HTTP, HTTPS, and Error pages.
    * Finally, it will print **"Tests passed"** and exit successfully.

---

## Implementation Details

Here is how I solved the challenge:

### 1. Containerization (Docker)
I created two custom Docker images:
* **Nginx Server:** Built on `ubuntu:24.04`. It installs Nginx and copies the configuration and generated certificates into the correct folders.
* **Tester:** Built on `python:3.11-slim`. It acts as an automated client to verify the server's behavior.

### 2. Automation (`test_script.py`)
I wrote a Python script that:
* **Waits for Service:** Uses a retry loop to prevent the test from failing while Nginx is still starting up.
* **Verifies requests:** The expected behaviour (response code / response content).
* **Verifies SSL:** Connects to the HTTPS port (ignoring self-signed warnings) to ensure the SSL handshake works.

---

## Security & CI

**Why are there no keys in the repo?**
Committing private keys to a repository is a security vulnerability. 

* **Local Development:** The instructions above show how to generate them securely on your machine.
* **Continuous Integration (GitHub Actions):** My CI pipeline (`.github/workflows/ci.yml`) automatically creates a temporary "dummy" certificate just for the duration of the test. This ensures the code is tested on every push without leaking secrets!
