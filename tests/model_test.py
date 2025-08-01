import requests
import json
import os

# Ensure Sentence-BERT is used
os.environ["SCORING_METHOD"] = "sbert"

url = "http://0.0.0.0:8000/score_answers"
payload = {
    "id": [
        "devops:179",
        "devops:117",
        "devops:173",
        "devops:127",
        "devops:1",
        "devops:60",
        "devops:148",
        "devops:195"
    ],
    "answers": [
        "Monitoring and logging in DevOps ensure real-time visibility into system performance, enabling quick detection and resolution of issues. They track metrics like uptime and errors, supporting proactive maintenance and compliance.",
        "System design in DevOps helps create scalable and reliable infrastructure, optimizing automation and deployment processes.",
        "Cloud platforms provide scalable infrastructure and services, enabling faster deployments and cost efficiency in DevOps.",
        "Disaster recovery and backups ensure data integrity and system availability, minimizing downtime during failures.",
        "Cloud platforms in DevOps provide scalable infrastructure, managed services like AWS ECS, and automated deployment tools, enabling rapid, cost-efficient, and reliable software delivery.",
        "CI/CD in DevOps automates code integration, testing, and deployment, reducing errors and speeding up delivery cycles.",
        "System design in DevOps is vital for building scalable, fault-tolerant, and resilient systems that ensure high availability and efficient traffic management. It supports microservices, automates CI/CD pipelines, and integrates observability for monitoring system health and performance under varying loads.",
        "Load balancing distributes traffic across servers, improving performance, scalability, and reliability in DevOps environments."
    ]
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
    print("Score response:")
    print(json.dumps(data, indent=2))
    assert 0 <= data["score"] <= 10, f"Score {data['score']} is out of range"
    assert len(data["feedback"].split("\n")) == 8, f"Expected 8 feedback lines, got {len(data['feedback'].split('\n'))}"
    assert data["score"] > 7.39, f"Expected score > 7.39, got {data['score']}"
else:
    print(f"Error: {response.status_code}, {response.text}")