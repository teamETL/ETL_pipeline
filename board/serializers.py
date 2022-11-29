from .models import Blog
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
    views = serializers.IntegerField(read_only=True)
    class Meta:
        model = Blog
        fields = ('id','title','created_at','updated_at','user','body','views')

class UsernameSerializer(serializers.Serializer):
    user = serializers.CharField(required=True)

    class Meta:
        Model = Blog
        fileds =('user')