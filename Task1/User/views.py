from django.shortcuts import render
from .serializers import LoginSerializer , UserRegisterSerializer, FriendRequestSerializer
from rest_framework.views import APIView
from .models import user, FriendRequest
from rest_framework import status
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.conf import settings
from .utils import authenticate_user
from django_ratelimit.decorators import ratelimit
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
     
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        User = user.objects.filter(email=email).first()

        if User is None:
            raise AuthenticationFailed("Invalid email")

        if not User.check_password(password):

            raise AuthenticationFailed("invalid password")

        payload = {
            "id": User.id,
            "email": User.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }


        secret_key = settings.HASH_KEY 
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        response = Response()
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=False,
            samesite="None",
            secure=True,
            path="/",
        )
        response.data = {"jwt": token, "user": payload}
        return response
    
class SearchView(APIView):
    def get(self,request,keyword):
        token = request.COOKIES.get('jwt')
        try:
            User = authenticate_user(token)
            User_id = User.id
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
    #keyword = request.GET.get('keyword')
        if not keyword:
            return Response({'error':'Provide any key word'}, status=status.HTTP_204_NO_CONTENT)
    
        if '@' in keyword:

            User = user.objects.filter(email=keyword).first()

            if User:
                return Response({'id':User.id,'name':User.name}, status=status.HTTP_200_OK)
            else:
                return Response({'No user found with this email'}, status=status.HTTP_404_NOT_FOUND)
        
    
        users = user.objects.filter(name__icontains=keyword).values('id', 'name')[:10]

        if users:
            return Response(users,status=status.HTTP_200_OK)
        else:
            return Response({'No user found with this email'},status=status.HTTP_404_NOT_FOUND)
    

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ratelimit(key='user_or_ip', rate='3/m', method='POST', block=True), name='dispatch')
class SendFriendRequestView(APIView):
    def post(self,request,to_user_id_sent):
        token = request.COOKIES.get('jwt')
        try:
            User = authenticate_user(token)
            User_id = User.id
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
        from_user_id = User_id
        if not to_user_id_sent:
            return Response({'error':'Provide any key word'}, status=status.HTTP_204_NO_CONTENT)
    
        to_user_id = to_user_id_sent

        from_user = get_object_or_404(user, id= from_user_id)
        to_user = get_object_or_404(user, id= to_user_id)

        existing_request = FriendRequest.objects.filter(from_user=from_user,to_user=to_user).exists()
        if existing_request:
            return Response({'message':'The friend request is already send'},status=400)
    
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user, status ='pending')
        return Response({'message':'The friend request was send'},status=201)


#accept the pending request of a user, where the pending requests to specific user will be displayed by the function pending_request
class AcceptsRequstView(APIView):
    def put(self,request,request_id):
        token = request.COOKIES.get('jwt')
        try:
            User = authenticate_user(token)
            User_id = User.id
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request_id:
            return Response({'error':'Provide any request_id'}, status=status.HTTP_204_NO_CONTENT)

        friend_request = get_object_or_404(FriendRequest, id=request_id, from_user=User_id, status='pending')
        friend_request.status = 'accepted'
        friend_request.save()
        return Response({'message':'The Friend request was accepted'})
    
    
class RejectRequstView(APIView):
    def put(self,request,request_id):
        token = request.COOKIES.get('jwt')
        try:
            User = authenticate_user(token)
            User_id = User.id
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request_id:
            return Response({'error':'Provide any request_id'}, status=status.HTTP_204_NO_CONTENT)

        friend_request = get_object_or_404(FriendRequest, id=request_id, from_user=User_id, status='pending')
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'message':'The Friend request was Rejected'})


class PendingRequestsView(APIView):
    def pending_request(self,request):
        token = request.COOKIES.get('jwt')
        try:
            User = authenticate_user(token)
            User_id = User.id
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
        pending_requests = FriendRequest.objects.filter(to_user=User_id, status='pending')

        serializer = FriendRequestSerializer(pending_requests,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class FriendListView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        try:
            User = authenticate_user(token)
            User_id = User.id
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
        to_user_accepted_requests = FriendRequest.objects.filter(to_user=User_id, status='accepted')

        from_user_accepted_requests = FriendRequest.objects.filter(from_user=User_id, status='accepted')

        pending_requests = list(to_user_accepted_requests)+list(from_user_accepted_requests)

        serializer = FriendRequestSerializer(pending_requests,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

    