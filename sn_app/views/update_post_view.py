from sn_app.views import CreatePostView
from rest_framework.response import Response
from rest_framework import status
from sn_app.serializers import PostSerializer
from sn_app.models import Post, User
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from sn_app.utils import (SafeJWTAuthentication, decode_uuid_from_jwt)
# from sn_app.decorators import JWTRequired


class UpdatePostView(CreatePostView):
    # @JWTRequired
    @swagger_auto_schema(
        request_body=PostSerializer,
        operation_summary="Update an existing post",
        operation_description="This api let a valid user update his/her existing post",
        responses={
            "201": "Updated the post",
            "400": "Error in update the post"
        }
    )
    def update(self, request, slug=None):
        uuid = decode_uuid_from_jwt(request.headers["Authorization"])
        post_updated_data = request.data

        try:
            user = get_object_or_404(User, uuid=uuid)
            post = get_object_or_404(Post, slug=slug, user=user)

            serializer = PostSerializer(post, data=post_updated_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            api_response = {
                "status": "successful",
                "message": f"Post with {serializer.data['title']} title data updated",
                "data": serializer.data
            }
            return Response(api_response, status=status.HTTP_200_OK)

        except Exception as e:
            api_response = {
                "status": "successful",
                "message": str(e),
            }
            return Response(api_response, status=status.HTTP_400_BAD_REQUEST)
