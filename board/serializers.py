from .models import Blog
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    views = serializers.IntegerField(read_only=True)
    class Meta:
        model = Blog
        fields = ('id','user','title','created_at','updated_at','body','views')

