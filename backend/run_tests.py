import unittest
import sys
import os
from fastapi.testclient import TestClient

# Adjust path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app

class TestOrbitOSAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["product"], "OrbitOS")
        self.assertIn("CEO Agent", data["agents"])

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("agents", data)

    def test_list_agents(self):
        response = self.client.get("/api/agents/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("agents", data)
        self.assertEqual(len(data["agents"]), 8)

    def test_get_individual_agent_status(self):
        response = self.client.get("/api/agents/ceo/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "CEO Agent")

    def test_list_projects(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("projects", data)

    def test_get_analytics(self):
        response = self.client.get("/api/analytics/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("kpis", data)
        self.assertGreater(len(data["kpis"]), 0)

    def test_submit_goal_validation(self):
        # Invalid short goal validation test
        response = self.client.post("/api/goals/submit", json={"goal_text": "abc"})
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
