from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, ProfileSerializer, BuyCreditSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated





class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User registered successfully'})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

class BuyCreditView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = BuyCreditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        num_credits = serializer.validated_data['num_credits']


        # Send email to admin
        subject = f"Credit request from {user.email}"
        message = f"User {user.email} has requested to buy {num_credits} more credit."
        from_email = "noreply@example.com"
        recipient_list = ['raorehmat11@gmail.com']
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        message = 'Email sent successfully. The admin will reply soon.'
        return Response({'message': message}, status=status.HTTP_200_OK)


# class BuyCreditView(APIView):
#     def post(self, request, format=None):
#         serializer = BuyCreditSerializer(data=request.data)
#         if serializer.is_valid():
#             num_credits = serializer.validated_data['num_credits']
#             message = serializer.validated_data.get('message', '')
#             user = request.user
#             if user.is_authenticated:
#                 admin_email = settings.ADMIN_EMAIL
#                 send_mail(
#                     'Credit purchase request',
#                     f'A credit purchase request has been made by {user.email}. They would like to buy {num_credits} credits. Message: {message}',
#                     settings.EMAIL_HOST_USER,
#                     [admin_email],
#                     fail_silently=False,
#                 )
#                 return Response(status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ADMIN_EMAIL