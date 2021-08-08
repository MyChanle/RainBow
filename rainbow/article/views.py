from rest_framework import mixins, generics
from django.http import Http404

from .models import Article
from .serializers import ArticleDetailSerializer, ArticleListSerializer
from .permissions import IsAdminUserOrReadOnly


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """ ArticleDetail """

    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ArticleList(generics.ListCreateAPIView):
    """ ArticleList """
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
