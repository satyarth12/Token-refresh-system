from rest_framework import serializers
from django.contrib.auth import get_user_model

USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'password']
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True},
                        }

    def create(self, validated_data):
        user = USER.objects.create_user(**validated_data)
        return user
