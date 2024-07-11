from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from myapp.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from myapp.serializers import UserSerializer, OrganisationSerializer
from myapp.models import User, Organisation

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(RefreshToken.for_user(user).access_token),
                    "user": {
                        "userId": user.user_id,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class OrganisationListView(generics.ListAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.organisations.all()
    
class OrganisationDetailView(APIView):
    def get(self, request, org_id):
        # Retrieve organisation detail logic here
        return Response({"message": "Organisation detail"}, status=status.HTTP_200_OK)

class CreateOrganisationView(APIView):
    def post(self, request):
        # Create organisation logic here
        return Response({"message": "Organisation created"}, status=status.HTTP_201_CREATED)

class AddUserToOrganisationView(APIView):
    def post(self, request, org_id):
        # Add user to organisation logic here
        return Response({"message": "User added to organisation"}, status=status.HTTP_200_OK)