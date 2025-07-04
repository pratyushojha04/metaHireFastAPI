import requests
import json
import os
import subprocess

os.environ["SCORING_METHOD"] = "sbert"
url = "http://0.0.0.0:8000/score_answers"

# Common payload components
base_payload = {
    "id": [
        "devops:179",
        "devops:117",
        "devops:173",
        "devops:127",
        "devops:1",
        "devops:60",
        "devops:148",
        "devops:195",
        "coding_problem:1",
        "coding_problem:2"
    ],
    "answers": [
        "Monitoring and logging in DevOps ensure real-time visibility into system performance, enabling quick detection and resolution of issues. They track metrics like uptime and errors, supporting proactive maintenance and compliance.",
        "System design in DevOps helps create scalable and reliable infrastructure, optimizing automation and deployment processes.",
        "Cloud platforms provide scalable infrastructure and services, enabling faster deployments and cost efficiency in DevOps.",
        "Disaster recovery and backups ensure data integrity and system availability, minimizing downtime during failures.",
        "Cloud platforms in DevOps provide scalable infrastructure, managed services like AWS ECS, and automated deployment tools, enabling rapid, cost-efficient, and reliable software delivery.",
        "CI/CD in DevOps automates code integration, testing, and deployment, reducing errors and speeding up delivery cycles.",
        "System design in DevOps is critical for building fault-tolerant, scalable systems that ensure high availability and efficient traffic distribution. It supports microservices architecture, automates CI/CD pipelines, and integrates observability for performance monitoring.",
        "Load balancing distributes traffic across servers, improving performance, scalability, and reliability in DevOps environments."
    ]
}

# Language-specific code submissions
language_submissions = {
    "python": {
        "language": "python",
        "code_submissions": [
            """
def sum_array(arr):
    return sum(arr)
            """,
            """
def max_element(arr):
    return max(arr) if arr else 0
            """
        ]
    },
    "java": {
        "language": "java",
        "code_submissions": [
            """
public class Solution {
    public int sumArray(int[] arr) {
        int sum = 0;
        for (int num : arr) {
            sum += num;
        }
        return sum;
    }
}
            """,
            """
public class Solution {
    public int maxElement(int[] arr) {
        if (arr.length == 0) return 0;
        int max = arr[0];
        for (int num : arr) {
            if (num > max) {
                max = num;
            }
        }
        return max;
    }
}
            """
        ]
    },
    "javascript": {
        "language": "javascript",
        "code_submissions": [
            """
function sumArray(arr) {
    return arr.reduce((sum, num) => sum + num, 0);
}
            """,
            """
function maxElement(arr) {
    return arr.length ? Math.max(...arr) : 0;
}
            """
        ]
    },
    "cpp": {
        "language": "cpp",
        "code_submissions": [
            """
#include <vector>
int sumArray(std::vector<int> arr) {
    int sum = 0;
    for (int num : arr) {
        sum += num;
    }
    return sum;
}
            """,
            """
#include <vector>
int maxElement(std::vector<int> arr) {
    if (arr.empty()) return 0;
    int max = arr[0];
    for (int num : arr) {
        if (num > max) {
            max = num;
        }
    }
    return max;
}
            """
        ]
    }
}

# Test each language
for language, config in language_submissions.items():
    print(f"\nTesting language: {language}")
    payload = base_payload.copy()
    payload.update(config)
    
    # Run the server in a subprocess to capture stderr
    server_process = subprocess.Popen(['python', 'main.py'], stderr=subprocess.PIPE, text=True)
    try:
        response = requests.post(url, json=payload, timeout=10)
        server_process.terminate()
        stderr_output, _ = server_process.communicate()
        if stderr_output:
            print(f"Server stderr output for {language}:\n{stderr_output}")
        
        if response.status_code == 200:
            data = response.json()
            print("Score response:")
            print(json.dumps(data, indent=2))
            feedback_lines = len(data["feedback"].split("\n"))
            print(f"Feedback lines: {feedback_lines}")
            print(f"Total score: {data['score']}")
            assert 0 <= data["score"] <= 15, f"Score {data['score']} is out of range for {language}"
            assert feedback_lines == 10, f"Expected 10 feedback lines, got {feedback_lines} for {language}"
            if data["score"] <= 10:
                print(f"Warning: Low score for {language}. Check coding_problem test cases in MongoDB collection.")
        else:
            print(f"Error for {language}: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error for {language}: {str(e)}")
        server_process.terminate()
        stderr_output, _ = server_process.communicate()
        if stderr_output:
            print(f"Server stderr output for {language}:\n{stderr_output}")