from rest_framework import serializers
from .models import Article, Category, Tag, Avatar
from user_info.serializers import UserDetailSerializer


class AvatarSerializer(serializers.ModelSerializer):
    content = serializers.ImageField(required=True)
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """ TagSerializer """
    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get("text")
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError(f"Tag with text {text} exists.")

    def create(self, validated_data):
        self.check_tag_obj_exists((validated_data))
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        self.check_tag_obj_exists((validated_data))
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """ CategorySerializer """
    url = serializers.HyperlinkedIdentityField(view_name="category-detail")

    class Meta:
        model = Category
        fields = "__all__"
        read_only = ['created']


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    """ ArticleSerializer """
    author = UserDetailSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text')
    category_id = serializers.IntegerField(
        write_only=True, allow_null=True, required=False)
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(
        write_only=True,
        allow_null=True,
        required=False
    )

    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here..'
    }

    def check_obj_exists_or_fail(self, model, value, message="default"):
        if not self.default_error_messages.get(message, None):
            message = 'default'

        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(
            model=Avatar,
            value=value,
            message='incorrect_avatar_id'
        )

        return value

    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(
            model=Category,
            value=value,
            message='incorrect_category_id'
        )

        return value

    def to_internal_value(self, data):
        tags_data = data.get("tags")

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)
        return super().to_internal_value(data)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """ ArticleCategoryDetailSerializer """
    url = serializers.HyperlinkedIdentityField(view_name="article-detail")

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """ CategoryDetailSerializer """
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles'
        ]


class ArticleSerializer(ArticleBaseSerializer):
    """ ArticleDetailSerializer """
    class Meta:
        model = Article
        fields = "__all__"
        extra_kwargs = {"body": {"write_only": True}}


class ArticleDetailSerializer(ArticleBaseSerializer):
    """ ArticleDetailSerializer """
    body_html = serializers.SerializerMethodField()
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self, obj):
        return obj.get_md()[0]
    
    def get_toc_html(self, obj):
        return obj.get_md()[1]
    
    class Meta:
        model = Article
        fields = "__all__"
