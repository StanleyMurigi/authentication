# myapp/urls.py
from django.urls import path
from myapp.views import RegisterView, LoginView, UserDetailView, OrganisationListView, OrganisationDetailView, CreateOrganisationView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('users/<uuid:id>/', UserDetailView.as_view(), name='user-detail'),
    path('organisations/', OrganisationListView.as_view(), name='organisation-list'),
    path('organisations/<uuid:org_id>/', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('organisations/create/', CreateOrganisationView.as_view(), name='create-organisation'),
    path('organisations/<uuid:org_id>/users/', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]

