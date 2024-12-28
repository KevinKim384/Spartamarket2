# 1. 개요
## 1.1 프로젝트 정보
**프로젝트명**: SpartaMarket-DRF
간단한 로그인과, 로그인을 통해 상품과 여러가지 아이템을 올려, 다른 유저들도 볼 수 있게 해주는 간단한 Django Rest Framework를 이용한 웹입니다.
**개발 기간**: 24.12.24.(목)~24.12.26(월), 3일 간
#프로젝트 일정
| 날짜              | 목표                                                           | 비고  |
|-------------------|--------------------------------------------------------------|-------|
| **12/24(화)**     | 기본  코드 프로젝트 및 app 파일 추가, 및 전체적 흐름 구성 | 1일   |
| **12/25(수)** | - 코드 디버깅 작업, 및 추가                                      | 1일   |
| **12/26(목)**       | - 최종 점검 및 회고<br>- ERD, README 작성                          | 1일   |

개발인원 1명
| 이름(구분)          | 역할 및 기여도                |
|---------------------|------------------------------|
| **김준기(개인)**     | - 개인 코드 작성 및 디버깅 처리

# 1.2 프로젝트 목적
Django Rest Framework에 대한 실력을 쌓고, Django의 개념을 이용해 DRF 문법과 디버깅 해결 능력 향상을 위한 개인 프로젝트

# 2. 주요 기능
### MVP(Minimum Viable Product)
 - 회원가입 / 로그인 / 프로필 조회
### 상품 관련 기능 및 조건
 - 상품 등록 / 상품 목록 조회 / 상품 수정 / 상품 삭제
대표적인 코드의 흐름(ERD)
ERD
![DRF - ERD](https://github.com/user-attachments/assets/81dea294-04bf-47b0-929e-6f1811171abe)

# 1. MVP(Minimum Viable Product)
```
#---------------------------------------------------------------------------------------------------
# 회원가입
# Create your views here.
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def signup(request):
    print(request.data)
    serializer = AccountSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '회원가입에 성공하셨습니다.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
![회원가입](https://github.com/user-attachments/assets/1bd0fee4-3a22-4997-8d1c-11a5fb36c91f)
```
#---------------------------------------------------------------------------------------------------
# 로그인
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        if user is not None:
            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': '로그인에 성공했습니다.'
            }, status=200)
        else:
            return JsonResponse({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
```
![로그인](https://github.com/user-attachments/assets/979ac1d2-b0cf-4e7c-9337-72cc8deed9b9)
```
#---------------------------------------------------------------------------------------------------
# 로그아웃 
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny]) 
@login_required
def logout(request):
    if request.user.is_authenticated:
        try:
            ref_token = request.data.get("refresh")
            token = RefreshToken(ref_token)
            token.blacklist()
            return Response({"message": "로그아웃"})
        except Exception:
            return Response({"error": "다시 시도해 주세요"}, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------------------------
# 사용자 기본 프로필
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated]) 
def user_profile(request, username):
    user = Users.objects.filter(username = username)
    # user = get_object_or_404(Users, username = username)
    if request.method in ('PUT', 'PATCH'):
        serializer = ProfileSerializer(instance = request.user, data = request.data, partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "회원정보가 수정되었습니다.","user": serializer.data}, status = status.HTTP_202_ACCEPTED)
    if request.method == 'GET':
        serializer = ProfileSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "다시 시도해 주세요"}, status=status.HTTP_400_BAD_REQUEST)
```
![프로필 조회](https://github.com/user-attachments/assets/6186ce7e-b59b-4e6e-a693-9631cb35bd7e)

# 2. 상품 관련 기능 및 조건
```
#---------------------------------------------------------------------------------------------------
# 전체 상품 조회 및 생성
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
                product = serializer.save()
                return Response(ProductsSerializer(product).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
![상품 조회](https://github.com/user-attachments/assets/3ceccee3-6091-4da9-bb5f-94bc9c3e10a7)
```
#---------------------------------------------------------------------------------------------------
# 작성자 상품 목록 조회 / 수정 / 삭제
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
        return Response({'message': '상품 글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, productId):
        product = self.get_object(productId)
        if request.user != product.author:
            raise PermissionDenied('작성자만 수정할 수 있습니다.')  # 작성자만 수정 가능
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
```
조회 및 조작, 삭제
![스크린샷 2024-12-25 174134](https://github.com/user-attachments/assets/6f07cf73-1e62-4e1e-89b7-dc8ff9674b8d)

![스크린샷 2024-12-26 184330](https://github.com/user-attachments/assets/f7d38bb7-a506-4890-b236-3888bf558285)

# 3. 기술 스텍
- 언어: Python 3.10+
- 프레임워크: Django Rest Framework

- Backend:DRF
- 저장소: SQLite
- 협업도구: GitHub, Slack, Notion


# 4. 트러블 슈팅
- 1. 모델
     -모델의 author에 값이 들어가지 않아 발견한 문제
     -확인 후 data = request.data.copy()추가 및 복사된 값으로 fields에 정상적으로 값이 들어간 것을 확인 및 해결
- 2. views
     -views에서 사용자 관련 문제 발견(작성자만 사용할 수 있는 권한 부여 에러)
     -모델에서 발견한 문제 if request.user != product.author:에서 author에 값이 없는 것을 확인
     -Models에 author를 추가하여 사용자 권한 부여 및 해결
     
# 5. 향후 개선 계획
- 1. 향후 개별 페이지네이션 및 필터링(검색기능), 카테고리 기능 구현
