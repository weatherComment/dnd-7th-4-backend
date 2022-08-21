from django.shortcuts import render, redirect, get_object_or_404
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from dnd_7th_4_backend.settings.base import env
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model

from .models import Profile
from .serializers import *
from main.serializers import *

# JWT 발급 함수
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),  # access_token 호출
        'refresh': str(refresh)
    }


# 프론트 요청부분
@api_view(['GET'])
@permission_classes([AllowAny])
def front(request):
    client_id = env('kakao_client_id')
    redirect_uri = env('kakao_redirect_uri')
    response_type = "code"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}"
    )



# 백엔드 처리부분
@api_view(['GET'])
@permission_classes([AllowAny])
def back(request):

    code = request.GET.get('code', None)

    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': env('kakao_client_id'),
        'redirect_uri': env('kakao_redirect_uri'),
        'code': code
    }

    url = 'https://kauth.kakao.com/oauth/token'

    token_req = requests.post(url, headers=headers, data=data)
    token_req_json = token_req.json()

    kakao_access_token = token_req_json.get("access_token")
    print(kakao_access_token)
    kakao_api_response = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Authorization": f"Bearer {kakao_access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        },
    )
    kakao_api_response = kakao_api_response.json()
    kakao_id = kakao_api_response["id"]
    nickname = kakao_api_response["properties"]["nickname"]
    profile_image = kakao_api_response["properties"]["profile_image"]

    profile = Profile.objects.filter(kakao_id=str(kakao_id))

    if profile.exists():
        print("기존 유저")
        user = User.objects.get(username=str(kakao_id))
    else:
        print("새로운 유저")
        user = User.objects.create(username=str(kakao_id))  # unique 값으로 username 넣어야함
        user.save()
        profile = Profile.objects.create(user=user, kakao_id=str(kakao_id), nickname=nickname, profile_image=str(profile_image))
        profile.save()

    return Response({"nickname": nickname, "kakao_access_token": kakao_access_token, "django_token": get_tokens_for_user(user)})


# 연결 끊기 -> 로컬 테스트용
def logout(request):
    kakao_access_token = "EcW8_CTN85mbXlR38Nru2qujG0RSfLniZa9-AP5LCisMpwAAAYKu3xw5"  # kakao access token
    data = requests.post("https://kapi.kakao.com/v1/user/unlink",
                         headers={"Authorization": f"Bearer {kakao_access_token}"},
                         )
    print(data.json())
    return Response({"data": "연결 끊기 완료"})


# 백엔드 테스트용
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)

        if not Profile.objects.filter(user=user).exists():
            profile = Profile.objects.create(user=user, nickname=user.username, kakao_id=user.id)
            profile.save()

        if check_password(password, user.password):
            user = authenticate(username=username, password=password)
            data = {'username': username, 'django_token': get_tokens_for_user(user)}
            return Response(data, status=status.HTTP_200_OK)
    except:
        return Response({"message": "로그인 오류"}, status=status.HTTP_400_BAD_REQUEST)


# 카카오톡 알림 설정
class KakaoAlarmView(APIView):
    permission_classes = (AllowAny,)

    # 만약 사용자의 alarm이 on -> off로 off 였으면 on으로 변경
    def post(self, request):
        print('/accout/kakao_alarm : GET -----------------------------')
        # 받은 데이터
        user = request.user.profile
        
        # 카카오톡 알림 설정하기
        if user.kakao_alarm:
            user.kakao_alarm = False
        else:
            user.kakao_alarm = True
        user.save()

        return Response({"data": ProfileKakaoAlarmSerializers(user).data}, status=status.HTTP_200_OK)


# 카카오톡 지역 설정
class KakaoRegionView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        print('account/alarm/region : POST ——————————————')

        # 받은 데이터
        city = request.data["city"]  # 시
        district = request.data["district"]  # 군, 구
        user = request.user.profile # 사용자
        region = get_object_or_404(Region, city=city, district=district)

        if user.kakao_region == region:
            return Response({"text": "이미 설정된 지역입니다."}, status=status.HTTP_409_CONFLICT)
        else:
            # 알림 지역 갱신하기
            user.kakao_region = region
            user.save()

            data = {}
            data['사용자id'] = user.id
            data['등록된지역'] = RegionSeriallizer(user.kakao_region).data
            return Response({"data": data}, status=status.HTTP_200_OK)


# 사용자 지역 생성 및 삭제
class RegionView(APIView):
    permission_classes = (AllowAny,)

    # 도착한 city, district를 사용자 지역으로 생성
    def post(self, request):
        print('account/region : POST ——————————————')
        # 받은 데이터
        city = request.data["city"]  # 시
        district = request.data["district"]  # 군, 구
        user = request.user.profile
        region = get_object_or_404(Region, city=city, district=district)

        try:
            # 이미 user와 region에 대한 데이터가 존재하는 경우
            user_region = User_Region.objects.get(region=region, user=user)
            return Response({"error": "user와 region에 대해 데이터가 이미 존재합니다."}, status=status.HTTP_409_CONFLICT)
        except User_Region.DoesNotExist:

            # user_region 데이터 생성
            user_region = User_Region(user=user, region=region)
            user_region.save()

            data = {}
            data['사용자id'] = user.id
            data['지역'] = RegionSeriallizer(region).data
            return Response({"data": data}, status=status.HTTP_200_OK)


    # 도착한 city, district를 사용자 지역 목록에서 삭제
    def delete(self, request):
        print('/region : DELETE ——————————————')
        # 받은 데이터
        city = request.GET.get('city', '')  # 시
        district = request.GET.get('district', '')  # 군, 구

        user = request.user.profile
        region = get_object_or_404(Region, city=city, district=district)

        try:
            # 지역 목록에서 삭제
            user_region = User_Region.objects.get(region=region, user=user)
            user_region.delete()
            return Response({"text": "지역이 지역 목록에서 삭제되었습니다."}, status=status.HTTP_200_OK)
        except User_Region.DoesNotExist:
            # 요청한 데이터가 사용자에게 등록이 되어 있지 않았던 경우
            return Response({"error": "해당은 지역은 사용자에게 등록되어 있지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

