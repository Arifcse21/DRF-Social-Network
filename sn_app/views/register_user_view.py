from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from sn_app.serializers import UserSerializer
from sn_app.utils import GenerateJWTokensUtil
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import uuid


class RegisterUserView(ViewSet):

    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_summary="Register new user",
        operation_description="This api registers new user and return access jw token"
    )
    def create(self, request):
        user_uuid = str(uuid.uuid4())
        print(f"uuid: {user_uuid}")
        user_data = {
            "first_name": request.data["first_name"],
            "last_name": request.data["last_name"],
            "email": request.data["email"],
            "username": request.data["username"],
            "password": request.data["password"],
            "confirm_password": request.data["confirm_password"],

        }

        serializer = UserSerializer(data=user_data)

        # access_token = GenerateJWTokensUtil.access_token_generator(user_uuid)
        # refresh_token = GenerateJWTokensUtil.refresh_token_generator(user_uuid)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        api_response = {
            "status": "successful",
            "message": "New user registered",
            "user": serializer.data,
            # "access_token": str(access_token),
        }

        return Response(api_response, status=status.HTTP_201_CREATED)
        

