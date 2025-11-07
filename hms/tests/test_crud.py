import json

def test_create_list_get_update_delete(client):
    # create
    payload = {"name": "Test", "age": 30, "disease": "Flu"}
    r = client.post("/patients", data=json.dumps(payload),
                    content_type="application/json")
    assert r.status_code == 201
    created = r.get_json()
    assert created["name"] == "Test"
    pid = created["id"]

    # list
    r = client.get("/patients")
    assert r.status_code == 200
    all_p = r.get_json()
    assert any(p["id"] == pid for p in all_p)

    # get
    r = client.get(f"/patients/{pid}")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Test"

    # update
    r = client.put(f"/patients/{pid}", data=json.dumps({"age": 35}),
                   content_type="application/json")
    assert r.status_code == 200
    assert r.get_json()["age"] == 35

    # delete
    r = client.delete(f"/patients/{pid}")
    assert r.status_code == 200

    # confirm deletion
    r = client.get(f"/patients/{pid}")
    assert r.status_code == 404
