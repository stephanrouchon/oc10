from rest_framework.serializers import ModelSerializer, ValidationError
from django.utils.timezone import now
from datetime import timedelta

from authentication.models import User, AGE_MIN


class UserSerializer(ModelSerializer):

    class Meta:
        model= User
        fields = ['id','username','first_name','last_name','can_data_be_shared','can_be_contacted']
        

class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'date_joined'
                  ]

class UserCreationSerializer(ModelSerializer):

    class Meta:
        model= User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'can_be_contacted',
                  'can_data_be_shared',
                  'birthdate',
                  'password']
        extra_kwargs = {'password': {'write_only':True}}
        

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_birthdate(self, value):
        
        today = now().date()
        
        # on calcule la date à laquelle un utilisateur n'a pas l'âge requis 
        min_birth_date = today - timedelta(days=AGE_MIN * 365)
        # on la compare avec la date de naissance 
        # si la date de naissance est supérieure à la date maximum
        # on retourne une erreur
        if value > min_birth_date:
            raise ValidationError("L'utilisateur doit avoir au moins 15 ans.")
        return value
