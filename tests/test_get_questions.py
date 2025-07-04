import requests
import json

url = "http://0.0.0.0:8000/get_questions"
payload = {
    "role": "Devops",
    "level": "fresher",
    "company": "Microsoft",
    "resumeText": "",
    "include_coding_problems": True
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
    print("Questions retrieved:")
    print(json.dumps(data, indent=2))
    assert len(data["id"]) == 10, f"Expected 10 IDs (8 theory + 2 coding), got {len(data['id'])}"
    assert len(data["questions"]) == 8, f"Expected 8 theory questions, got {len(data['questions'])}"
    assert len(data["coding_problems"]) == 2, f"Expected 2 coding problems, got {len(data['coding_problems'])}"
    assert all(id.startswith("coding_problem:") for id in data["id"][8:]), "Last 2 IDs must be coding problems"
    for cp in data["coding_problems"]:
        assert all(key in cp for key in ["question", "problem_description", "tc1", "tc2", "tc3", "tc4", "tc5", "company", "difficulty", "category", "hint"]), "Coding problem missing required fields"
else:
    print(f"Error: {response.status_code}, {response.text}")