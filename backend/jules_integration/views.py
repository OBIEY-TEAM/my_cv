from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import JulesSession, JulesActivity
from .serializers import JulesSessionSerializer, JulesActivitySerializer
from .services import create_jules_session, sync_jules_activities, approve_jules_plan, send_jules_message

class JulesSessionViewSet(viewsets.ModelViewSet):
    queryset = JulesSession.objects.all().order_by('-created_at')
    serializer_class = JulesSessionSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        prompt = request.data.get('prompt', '')
        repo_name = request.data.get('repo_name', '')
        if not prompt:
            return Response({'error': 'prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        session_obj = create_jules_session(user=request.user, prompt=prompt, repo_name=repo_name)
        serializer = self.get_serializer(session_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def sync_activities(self, request, pk=None):
        session_obj = self.get_object()
        activities = sync_jules_activities(session_obj)
        serializer = JulesActivitySerializer(activities, many=True)
        return Response({'activities': serializer.data})

    @action(detail=True, methods=['post'])
    def approve_plan(self, request, pk=None):
        session_obj = self.get_object()
        activity_id = request.data.get('activity_id', '')
        if not activity_id:
            return Response({'error': 'activity_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        result = approve_jules_plan(session_obj, activity_id)
        return Response({'result': result})

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        session_obj = self.get_object()
        message = request.data.get('message', '')
        if not message:
            return Response({'error': 'message is required'}, status=status.HTTP_400_BAD_REQUEST)

        activity_obj = send_jules_message(session_obj, message)
        serializer = JulesActivitySerializer(activity_obj)
        return Response({'activity': serializer.data})
