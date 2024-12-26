from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Products
from .serializers import ProductsSerializer
from rest_framework.exceptions import PermissionDenied
# Create your views here.
#---------------------------------------------------------------------------------------------------
class ProductListAPIView(APIView):
    def get(self, request):
        article = Products.objects.all()
        serializer = ProductsSerializer(article, many=True)
        data = serializer.data
        return Response(data)
    def post(self, request):
        data = request.data.copy()  
        data['author'] = request.user.id 
        
        serializer = ProductsSerializer(data=data)
        if serializer.is_valid():
            try:
                # 저장 후 생성된 객체 반환
                product = serializer.save()
                return Response(ProductsSerializer(product).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------------------------
class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, productId):
        return get_object_or_404(Products, pk = productId)
    
    def get(self, request, productId):
        article = self.get_object(productId)
        serializer = ProductsSerializer(article)
        data = serializer.data
        return Response(data)
    
    def delete(self, request, productId):
        product = self.get_object(productId)
        if request.user != product.author:
            raise PermissionDenied('작성자만 삭제할 수 있습니다.')  # 작성자만 삭제 가능
        product.delete()
        return Response({'message': '상품글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, productId):
        product = self.get_object(productId)
        if request.user != product.author:
            raise PermissionDenied('작성자만 수정할 수 있습니다.')  # 작성자만 수정 가능
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            