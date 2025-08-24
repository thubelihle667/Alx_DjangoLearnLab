from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from .models import Comment  

@receiver(post_save, sender=Comment)
def notify_post_commented(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    actor = instance.author
    recipient = post.author
    if recipient == actor:
        return
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb="commented on your post",
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.id,
        metadata={"comment_id": instance.id}
    )
