from .clients import GoogleJulesClient
from .models import JulesSession, JulesActivity

def create_jules_session(user, prompt, repo_name=""):
    client = GoogleJulesClient()
    session_data = client.create_session(prompt=prompt, repo_name=repo_name)
    session_id = session_data.get("name") or session_data.get("id", "session-unknown")

    session_obj, created = JulesSession.objects.get_or_create(
        session_id=session_id,
        defaults={
            "user": user if (user and user.is_authenticated) else None,
            "prompt_used": prompt,
            "status": session_data.get("status", "active")
        }
    )
    return session_obj

def sync_jules_activities(session_obj):
    client = GoogleJulesClient()
    res = client.list_activities(session_obj.session_id)
    activities = res.get("activities", [])

    created_activities = []
    for act in activities:
        act_id = act.get("id") or act.get("name", "")
        act_type = act.get("type", "message")
        content = act.get("content", {})
        plan_approved = act.get("plan_approved", False)

        activity_obj, created = JulesActivity.objects.get_or_create(
            session=session_obj,
            activity_id=act_id,
            defaults={
                "activity_type": act_type,
                "content": content,
                "plan_approved": plan_approved,
            }
        )
        created_activities.append(activity_obj)

    return created_activities

def approve_jules_plan(session_obj, activity_id):
    client = GoogleJulesClient()
    res = client.approve_plan(session_obj.session_id, activity_id)
    JulesActivity.objects.filter(session=session_obj, activity_id=activity_id).update(plan_approved=True)
    return res

def send_jules_message(session_obj, message):
    client = GoogleJulesClient()
    res = client.send_message(session_obj.session_id, message)
    act_id = res.get("id") or res.get("name", "msg-sent")
    activity_obj = JulesActivity.objects.create(
        session=session_obj,
        activity_id=act_id,
        activity_type=res.get("type", "message"),
        content=res.get("content", {"text": message}),
    )
    return activity_obj
