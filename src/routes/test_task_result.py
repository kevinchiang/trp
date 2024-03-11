from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_create_taskresult():
    body = {
      "id": None,
      "serial_number": "string",
      "start_time": "2024-03-08T19:29:18.518Z",
      "duration": 0,
      "test_status": 0,
      "actor": "string",
      "task_parameters": [
        {
          "id": None,
          "task_id": None,
          "base_id": None,
          "name": "string",
          "type": "string",
          "start_time": "2024-03-08T19:29:18.518Z",
          "duration": 0,
          "value_numeric": 0,
          "value_string": "string",
          "comparator": "string",
          "lsl": 0,
          "usl": 0,
          "expected_value": "string",
          "status": "string"
        }
      ]
    }

    response = client.post("/task_result/", json=body)
    assert response.status_code == 200

    expected_response = {
      "id": None,
      "serial_number": "string",
      "start_time": "2024-03-08T19:29:18.518000Z",
      "duration": 0,
      "test_status": 0,
      "actor": "string",
      "task_parameters": [
        {
          "id": None,
          "task_id": None,
          "base_id": None,
          "name": "string",
          "type": "string",
          "start_time": "2024-03-08T19:29:18.518000Z",
          "duration": 0,
          "value_numeric": 0,
          "value_string": "string",
          "comparator": "string",
          "lsl": 0,
          "usl": 0,
          "expected_value": "string",
          "status": "string"
        }
      ]
    }

    assert response.json() == expected_response


def test_get_taskresult():
    response = client.get("/task_result/1")
    assert response.status_code == 200
