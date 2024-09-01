from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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


class LoginAPIView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """ This API returns user credentials for the Vendor logged-in user """

        result = super(LoginAPIView, self).post(request, *args, **kwargs)
        return result


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
