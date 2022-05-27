from django.core.mail import send_mail
from real_estate.settings.development import DEFAULT_FROM_EMAIL
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Enquiry


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_enquiry_mail(request):
    data = request.data
    try:
        subject = data.get('subject')
        name = data.get('name')
        email = data.get('email')
        from_mail = data.get('email')
        message = data.get('message')
        recipient_list = [DEFAULT_FROM_EMAIL]
        send_mail(subject=subject, message=message, from_email=from_mail, recipient_list=recipient_list, fail_silently=True)
        enquiry = Enquiry.objects.create(name=name, email=email, subject=subject, message=message)
        return Response({"success": "Your Enquiry was sucessfully submitted"})

    except:
        return Response({"fail": "Your Enquiry was not send. try again"})
