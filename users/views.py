from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from common.custom_pagination import ListingPaginator
from .models import UserDetails
from .serializers import RegisterSerializer, UserDetailModelSerializer, UserTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterAPIView(APIView):

    def post(self, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


# class LoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email'].lower()
#             password = serializer.validated_data['password']
#             user = authenticate(email=email, password=password)
#             if user:
#                 return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#             return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """ This API returns user credentials for the Vendor logged-in user """

        result = super(LoginAPIView, self).post(request, *args, **kwargs)
        return result


# class SearchUserAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     pagination_class = PageNumberPagination
#
#     def get(self, request, *args, **kwargs):
#         keyword = request.query_params.get('search', '').lower()
#         users = UserDetails.objects.filter(email__iexact=keyword) | UserDetails.objects.filter(name__icontains=keyword)
#         paginator = self.pagination_class()
#         result_page = paginator.paginate_queryset(users, request)
#         serializer = UserDetailModelSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

class SearchUserAPIView(generics.ListAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ListingPaginator
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.query_params.get('search', '')
        if search_keyword:
            # Prioritize exact email match
            exact_email_match = queryset.filter(email__iexact=search_keyword)
            if exact_email_match.exists():
                return exact_email_match
        return queryset
