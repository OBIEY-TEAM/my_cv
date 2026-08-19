from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import JulesSession, JulesActivity
from .clients import GoogleJulesClient
from .services import create_jules_session, sync_jules_activities, approve_jules_plan, send_jules_message

User = get_user_model()

class JulesIntegrationTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin_test",
            email="admin@test.com",
            password="adminpassword"
        )
        self.normal_user = User.objects.create_user(
            username="normal_test",
            email="normal@test.com",
            password="normalpassword"
        )
        self.client = APIClient()

    def test_google_jules_client_mock_mode(self):
        jules_client = GoogleJulesClient(mock_mode=True)
        session_res = jules_client.create_session("Test prompt")
        self.assertIn("name", session_res)
        self.assertEqual(session_res["prompt"], "Test prompt")

        activities_res = jules_client.list_activities(session_res["name"])
        self.assertIn("activities", activities_res)
        self.assertTrue(len(activities_res["activities"]) > 0)

    def test_services(self):
        session_obj = create_jules_session(user=self.admin_user, prompt="Generate application package")
        self.assertIsNotNone(session_obj.id)
        self.assertEqual(session_obj.user, self.admin_user)

        activities = sync_jules_activities(session_obj)
        self.assertTrue(len(activities) > 0)

        act_id = activities[0].activity_id
        approve_res = approve_jules_plan(session_obj, act_id)
        self.assertEqual(approve_res.get("status"), "approved")

        msg_act = send_jules_message(session_obj, "Hello Jules")
        self.assertEqual(msg_act.session, session_obj)

    def test_api_permissions(self):
        # Unauthenticated request should return 401
        res = self.client.get("/api/jules/sessions/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # Normal non-admin user should return 403
        self.client.force_authenticate(user=self.normal_user)
        res = self.client.get("/api/jules/sessions/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user should return 200
        self.client.force_authenticate(user=self.admin_user)
        res = self.client.get("/api/jules/sessions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_session_create_and_actions_via_api(self):
        self.client.force_authenticate(user=self.admin_user)

        # Create Session
        create_res = self.client.post("/api/jules/sessions/", {"prompt": "API test prompt"}, format="json")
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        session_id = create_res.data["id"]

        # Sync activities
        sync_res = self.client.post(f"/api/jules/sessions/{session_id}/sync_activities/")
        self.assertEqual(sync_res.status_code, status.HTTP_200_OK)
        self.assertIn("activities", sync_res.data)

        # Approve plan
        act_id = sync_res.data["activities"][0]["activity_id"]
        app_res = self.client.post(f"/api/jules/sessions/{session_id}/approve_plan/", {"activity_id": act_id}, format="json")
        self.assertEqual(app_res.status_code, status.HTTP_200_OK)

        # Send message
        msg_res = self.client.post(f"/api/jules/sessions/{session_id}/send_message/", {"message": "Test msg"}, format="json")
        self.assertEqual(msg_res.status_code, status.HTTP_200_OK)
