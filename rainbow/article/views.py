from rest_framework import viewsets
from django.http import Http404

from .models import Article
from .serializers import ArticleSerializer
from .permissions import IsAdminUserOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    """ ArticleViewSet """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        """ perform_create """
        serializer.save(author=self.request.user)
