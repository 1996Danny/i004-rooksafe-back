from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        token['experience_level'] = user.experience_level
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add additional response data
        data.update({
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'email': self.user.email,
                'experience_level': self.user.experience_level,
            }
        })
        return data



class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ['investment_amount', 'asset_type', 'status', 'performance_data']

    def validate_investment_amount(self, value):
        """Validar que el monto de inversión sea positivo."""
        if value <= 0:
            raise serializers.ValidationError("El monto de inversión debe ser mayor que cero.")
        return value

# User profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'experience_level', 'created_at', 'updated_at']
        read_only_fields = ['email', 'updated_at', 'created_at']
        

class UpdateExperienceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['experience_level']

    def validate_experience_level(self, value):
        if value not in ['básico', 'intermedio', 'avanzado']:
            raise serializers.ValidationError("Invalid experience level. Must be 'básico', 'intermedio', or 'avanzado'.")
        return value


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'name', 'asset_type', 'current_value', 'market_cap', 'volume']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'created_at']
