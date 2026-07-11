from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import status, views, permissions
from rest_framework.response import Response
from apps.core.serializers import UserSerializer

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Django authenticates by username by default, but we mapped email as USERNAME_FIELD
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if not user.is_active:
                return Response({'error': 'Account is inactive.'}, status=status.HTTP_400_BAD_REQUEST)
            if not user.is_approved:
                return Response({'error': 'Account is pending administrator approval.'}, status=status.HTTP_400_BAD_REQUEST)

            login(request, user)
            
            # Fetch CSRF token for subsequent requests
            csrf_token = get_token(request)
            
            response = Response({
                'user': UserSerializer(user).data,
                'message': 'Logged in successfully.'
            })
            # Include CSRF token in header
            response['X-CSRFToken'] = csrf_token
            return response
            
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully.'})


class MeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
