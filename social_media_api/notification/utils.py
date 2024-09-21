from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(actor, verb, target):
    target_content_type = ContentType.objects.get_for_model(target.__class__)
    Notification.objects.create(
        recipient=target.author,  # assuming the Post or target object has an author field
        actor=actor,
        verb=verb,
        target_content_type=target_content_type,
        target_object_id=target.id
    )
