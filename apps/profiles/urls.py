from django.urls import path

from .views import AgentAPIListView, TopAgentAPIListView, GetProfileAPIView, UpdateProfileAPIView

urlpatterns = [
    path("me/", GetProfileAPIView.as_view(), name='get_profile'),
    path("update/<str:username>/", UpdateProfileAPIView.as_view(), name='update_profile'),
    path('agents/all/', AgentAPIListView.as_view(), name='all_agents'),
    path('top-agents/all/', TopAgentAPIListView.as_view(), name='top_agents'),
]
