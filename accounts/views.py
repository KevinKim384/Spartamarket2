from django.shortcuts import get_object_or_404, render 
from django.http import JsonResponse
from .serializers import AccountSerializer, ProfileSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# from .serializers import SignupSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from .models import Users
from rest_framework.permissions import IsAuthenticated

#---------------------------------------------------------------------------------------------------
# Create your views here.
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def signup(request):
    print(request.data)
    serializer = AccountSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '회원가입에 성공하셨습니다.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------------------------
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        if user is not None:
            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': '로그인에 성공했습니다.'
            }, status=200)
        else:
            return JsonResponse({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------------------------
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny]) 
@login_required
def logout(request):
    if request.user.is_authenticated:
        try:
            ref_token = request.data.get("refresh")
            token = RefreshToken(ref_token)
            token.blacklist()
            return Response({"message": "로그아웃"})
        except Exception:
            return Response({"error": "다시 시도해 주세요"}, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------------------------
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 접근 가능
def user_profile(request, username):
    user = Users.objects.filter(username = username)
    # user = get_object_or_404(Users, username = username)
    if request.method in ('PUT', 'PATCH'):
        serializer = ProfileSerializer(instance = request.user, data = request.data, partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "회원정보가 수정되었습니다.","user": serializer.data}, status = status.HTTP_202_ACCEPTED)
    if request.method == 'GET':
        serializer = ProfileSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "다시 시도해 주세요"}, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------------------------