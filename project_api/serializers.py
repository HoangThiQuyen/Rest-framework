from rest_framework import serializers

from project_api import models

class HelloSerializer(serializers.Serializer):
  """Seriallizers a name field for testing our APIView"""
  name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
  """Seriallizers a user profile object"""
  class Meta:
    model = models.UserProfile
    fields = ('id','email','name','password')
    # chứa những field muốn cấu hình thêm
    extra_kwargs ={
      'password': {
        'write_only':True,
        'style':{'input_type':'password'}
      }
    }

    


  