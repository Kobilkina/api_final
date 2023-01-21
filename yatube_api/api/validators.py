from rest_framework import serializers


class FollowValidator(object):
    requires_context = True

    def __call__(self, value, serializer):
        author = value
        user = serializer.context['request'].user
        if author == user:
            raise serializers.ValidationError('Подписка на самого себя!')
        if author.following.filter(user_id=user.id).exists():
            raise serializers.ValidationError('Подписка существует!')
        return value
