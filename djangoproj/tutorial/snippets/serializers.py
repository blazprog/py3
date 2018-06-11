from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet

class SnippetSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
                    view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url','highlight', 'title', 'code', 
                'linenos', 'language', 'style','owner')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    #dodamo vse snippete, ki pripadajo dolocenemu avtorju
    snippets = serializers.PrimaryKeyRelatedField(many=True, 
                                        queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('url', 'username', 'snippets')
