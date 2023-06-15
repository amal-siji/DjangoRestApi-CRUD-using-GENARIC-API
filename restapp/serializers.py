from rest_framework import serializers
from .models import restmodel


class restseri(serializers.ModelSerializer):
    class Meta:
        model = restmodel
        fields = '__all__'
        