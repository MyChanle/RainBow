from rest_framework import viewsets
from rest_framework import filters
from django.http import Http404

from .models import Article, Category, Tag, Avatar
from .serializers import ArticleSerializer, AvatarSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, ArticleDetailSerializer
from .permissions import IsAdminUserOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    """ ArticleViewSet """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    filterset_fields = ['title']

    def perform_create(self, serializer):
        """ perform_create """
        serializer.save(author=self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return ArticleSerializer
        else:
            return ArticleDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ CategoryViewSet """
    queryset = Category.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class TagViewSet(viewsets.ModelViewSet):
    """ TagViewSet """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class AvatarViewSet(viewsets.ModelViewSet):
    """ AvatarViewSet """
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]
