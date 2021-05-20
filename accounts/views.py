from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST 
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse

@api_view(['POST'])
def signup(request):
	#1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
    email = request.data.get('email')

	#1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	#2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	#3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # print(user.password)
    # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다.
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def follow(request, user_pk):

    person = get_object_or_404(get_user_model(), pk=user_pk)
    user = request.user
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
            follow = False
        else:
            person.followers.add(user)
            follow = True
        follow_status ={
            'follow':follow,
            'count':person.followers.count(),
        }
        return JsonResponse(follow_status)
    return redirect('accounts:profile', person.username)
