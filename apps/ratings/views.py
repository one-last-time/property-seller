from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Rating
from apps.profiles.models import Profile


User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_agent_review(request, profile_id):
    agent_profile = Profile.objects.get(id=profile_id, agent=True)
    data = request.data
    profile_user = User.objects.get(pkid=agent_profile.user.pkid)
    if profile_user.email == request.user.email:
        formatted_response = {"message": "You can't rate yourself"}
        return Response(formatted_response, status=status.HTTP_403_FORBIDDEN)

    alreadyexists = agent_profile.agent_review.filter(agent__pkid=agent_profile.pkid).exists()

    if alreadyexists:
        formatted_response = {"message": "Agent already reviewed"}
        return Response(formatted_response, status=status.HTTP_403_FORBIDDEN)

    elif data.get('rating', 0) == 0:
        formatted_response = {"message": "Please Select a rating"}
        return Response(formatted_response, status=status.HTTP_403_FORBIDDEN)
    else:
        review = Rating.objects.create(
            rater=request.user,
            agent=agent_profile,
            rating=data.get('rating'),
            comment=data.get('comment', '')
        )
        reviews = agent_profile.agent_review.all()
        agent_profile.num_reviews = len(reviews)

        total = 0
        for i in reviews:
            total+=i.rating

        return Response('Review Added')





