from .models import Products
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Users

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"
        
# class ArtticleDetailSerializer(ProductsSerializer):
#     comments = CommentSerializer(many = True, read_only = True)
#     comments_count = serializers.IntegerField(source = "comments.count", read_only = True)

    