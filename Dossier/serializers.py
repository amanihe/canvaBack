from Dossier.models import *
from dataclasses import field
from rest_framework import serializers




class S_Dossier(serializers.ModelSerializer):
    class Meta:
        model=T_Dossier
        fields='__all__'

class S_Rect(serializers.ModelSerializer):
    class Meta:
        model=T_Rect
        fields='__all__'

class S_Field(serializers.ModelSerializer):
    class Meta:
        model=T_Field
        fields='__all__'
class S_Link(serializers.ModelSerializer):
    class Meta:
        model=T_Link
        fields='__all__'
        