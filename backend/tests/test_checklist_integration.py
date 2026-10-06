from uuid import uuid4


def test_checklist_lifecycle(app):
    # Verify the checklist lifecycle against a real database.
    client = app
    base = "/api/checklists"
    title = f"Integration Test {uuid4()}"

    response = client.post(
        base,
        json={"title": title, "description": "Automated Test"},
    )
    assert response.status_code == 201, response.get_data(as_text=True)
    checklist_id = response.get_json()["id"]

    try:
        # Add an item.
        response = client.post(
            f"{base}/{checklist_id}/items",
            json={"title": "Test task", "order_index": 1},
        )
        assert response.status_code == 201, response.get_data(as_text=True)
        item_id = response.get_json()["id"]

        # Mark it as completed.
        response = client.put(
            f"{base}/items/{item_id}",
            json={
                "title": "Test task",
                "completed": True,
                "order_index": 1,
            },
        )
        assert response.status_code == 200, response.get_data(as_text=True)

        # A separate request must read the saved values.
        response = client.get(f"{base}/{checklist_id}")
        assert response.status_code == 200
        checklist = response.get_json()
        assert checklist["title"] == title
        assert len(checklist["items"]) == 1
        item = checklist["items"][0]
        assert item["id"] == item_id
        assert item["title"] == "Test task"
        assert item["completed"] is True

        # Deleting the checklist must also remove its item.
        response = client.delete(f"{base}/{checklist_id}")
        assert response.status_code == 200
        assert client.get(f"{base}/{checklist_id}").status_code == 404
        assert client.delete(f"{base}/items/{item_id}").status_code == 404
    finally:
        # Clean up this test's checklist even after a failed assertion.
        client.delete(f"{base}/{checklist_id}")
