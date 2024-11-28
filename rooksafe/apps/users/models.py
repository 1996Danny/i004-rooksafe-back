from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings

from rest_framework import serializers


class UserManager(BaseUserManager):
    def _create_user(self, name, email, password, experience_level, is_staff, is_superuser, **extra_fields):
        user = self.model(
            name=name,
            email=email,
            experience_level=experience_level,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, name, email, password=None, experience_level='básico', **extra_fields):
        return self._create_user(name, email, password, experience_level, False, False, **extra_fields)

    def create_superuser(self, name, email, password=None, experience_level='básico', **extra_fields):
        return self._create_user(name, email, password, experience_level, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    experience_level = models.CharField(max_length=12, choices=[('básico', 'Básico'),('intermedio', 'Intermedio'),('avanzado','Avanzado')], default="básico")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'name'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.name


class Simulation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usa AUTH_USER_MODEL
    investment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    asset_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='active')
    performance_data = models.JSONField(default=dict)

    def __str__(self):
        return f"Simulation {self.id} for {self.user.username}"

class UpdateExperienceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['experience_level']

    def validate_experience_level(self, value):
        if value not in ['básico', 'intermedio', 'avanzado']:
            raise serializers.ValidationError("Invalid experience level. Must be 'básico', 'intermedio', or 'avanzado'.")
        return value


class Asset(models.Model):

    TYPE_CHOICES = [
        ('stock', 'Acción'),
        ('crypto', 'Criptomoneda'),
        ('commodity', 'Comodidad'),
        ('forex', 'Forex'),
    ]

    name = models.CharField(max_length=200)  # Nombre del activo, por ejemplo "Bitcoin", "AAPL"
    asset_type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # Tipo de activo (acción, cripto, etc.)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)  # Valor actual del activo
    previous_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Valor anterior para comparaciones
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)  # Capitalización de mercado
    volume = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Volumen de negociación
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del registro
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización
    is_active = models.BooleanField(default=True)  # Si el activo está activo o no en la plataforma

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
