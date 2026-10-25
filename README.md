# AdShield — Malvertising Detection and Defense Lab

## 1. Project Overview
AdShield is an educational security lab that simulates malvertising detection and defense. It demonstrates how a security system can allow normal advertisements, block suspicious advertisements, log security events, and reject invalid requests.

**This project uses safe simulations only. No real malware is downloaded or executed.**

## 2. Objectives
- Simulate normal and suspicious advertisements.
- Detect suspicious behavior using predefined rules.
- Allow normal advertisements and block suspicious ones.
- Record security events and timestamps.
- Apply HTTP security headers.
- Test security behavior automatically.
- Run the application in Docker.

## 3. Technologies
- Python
- Flask
- HTML, CSS, and JavaScript
- Docker and Docker Compose
- Ubuntu on WSL
- Git and GitHub

## 4. System Architecture
1. The user opens the AdShield web interface.
2. The user selects a normal or suspicious advertisement test.
3. JavaScript sends a request to the Flask backend.
4. The backend validates the request and applies a predefined detection rule.
5. The application returns ALLOW or BLOCK.
6. The dashboard displays event statistics and recent events.
7. Flask logs security events for investigation.

## 5. Detection Rules

| Test Scenario | Expected Decision | Purpose |
|---|---|---|
| Normal advertisement | ALLOW | Demonstrates permitted behavior |
| Suspicious advertisement | BLOCK | Demonstrates detection and blocking |
| Unknown scenario | HTTP 400 | Rejects invalid input |
| Missing JSON | HTTP 400 | Rejects malformed requests |

The suspicious scenario is a controlled simulation, not a real malware detection engine.

## 6. Security Defenses
The application implements:
- **Input validation:** Only recognized test scenarios are accepted.
- **Content Security Policy (CSP):** Restricts permitted content sources.
- **X-Content-Type-Options:** Prevents MIME-type sniffing.
- **X-Frame-Options:** Prevents framing by other websites.
- **Referrer-Policy:** Limits referrer information.
- **Security logging:** Records allowed, blocked, and rejected events.
- **Containerization:** Runs the application in Docker.

## 7. Installation and Execution

### Requirements
Install Docker Desktop and enable its Ubuntu/WSL integration.

### Start the application
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd adshield
docker compose up --build -d
```

Open `http://localhost:5000` in your browser.

### View logs
```bash
docker compose logs --tail=50
```

### Stop the application
```bash
docker compose down
```

## 8. Dashboard API
The `/dashboard` endpoint returns:
- Total events
- Number of allowed events
- Number of blocked events
- The ten most recent events

Example:
```bash
curl http://localhost:5000/dashboard
```

## 9. Automated Testing
Run tests in a Python virtual environment:

```bash
source .venv/bin/activate
python -m unittest test_app.py -v
```

The test suite verifies normal advertisements, suspicious advertisements, invalid scenarios, missing JSON, and dashboard availability.

**Test result:** 5 tests passed.

## 10. Limitations
- Detection uses predefined scenarios rather than analyzing real advertisements.
- Event history is stored in memory and resets when the application restarts.
- The Flask development server is intended for local educational use, not production deployment.
- This lab does not download, execute, or distribute malware.

## 11. Conclusion
AdShield demonstrates fundamental security concepts: input validation, suspicious-event handling, security logging, HTTP security headers, containerization, and automated testing. It provides a safe foundation for learning about malvertising defense.
