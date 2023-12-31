from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """

    username = serializers.CharField(
        label = "username",
        write_only = True
        )

    password = serializers.CharField(
        label = "password",
        style = {"input_type": "password"},
        trim_whitespace = False,
        write_only = True
        )


    def validate(self, attrs):
        
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(self, username=username, password=password)

            if not user: # and not user.is_active:
                msg = "Access Denied: Wrong username and password"
                raise serializers.ValidationError(msg, code="authorization")
            
        else:
            msg = "Both username and password required"
            raise serializers.ValidationError(msg, code="authorization")
        
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        
        attrs['user'] = user
        return attrs