from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications = request.user.notifications.filter(read=False).order_by('-timestamp')
    data = [{"actor": n.actor.username, "verb": n.verb, "target": str(n.target), "timestamp": n.timestamp} for n in notifications]
    return Response({"notifications": data})
