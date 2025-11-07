# tests/test_batch_calc.py
import json

def test_average_age_endpoints(client):
    for i in range(25):
        payload = {"name": f"P{i}", "age": 20 + i, "disease": "N/A"}
        res = client.post("/patients", data=json.dumps(payload),
                          content_type="application/json")
        assert res.status_code == 201

    
