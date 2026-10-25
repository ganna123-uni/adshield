import unittest
import json
from app import app


class AdShieldTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_normal_ad_allowed(self):
        response = self.client.post(
            "/simulate",
            json={"scenario": "normal"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["decision"], "ALLOW")

    def test_suspicious_ad_blocked(self):
        response = self.client.post(
            "/simulate",
            json={"scenario": "suspicious"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["decision"], "BLOCK")

    def test_invalid_scenario_rejected(self):
        response = self.client.post(
            "/simulate",
            json={"scenario": "unknown"}
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_json_rejected(self):
        response = self.client.post("/simulate")
        self.assertEqual(response.status_code, 400)

    def test_dashboard_available(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_events", response.json)


if __name__ == "__main__":
    unittest.main()

