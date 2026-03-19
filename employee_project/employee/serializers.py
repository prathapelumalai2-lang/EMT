from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = '__all__'


class EmployeeDataSerializer(serializers.ModelSerializer):
    field_label = serializers.CharField(source='field.label', read_only=True)
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all())

    class Meta:
        model = EmployeeData
        fields = ['field', 'field_label', 'value']


class EmployeeSerializer(serializers.ModelSerializer):
    data = EmployeeDataSerializer(many=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'data']

    def create(self, validated_data):
        data = validated_data.pop('data')
        employee = Employee.objects.create(**validated_data)

        for item in data:
            EmployeeData.objects.create(
                employee=employee,
                field=item['field'],
                value=item['value']
            )

        return employee

    def update(self, instance, validated_data):
        data = validated_data.pop('data')

        instance.name = validated_data.get('name', instance.name)
        instance.save()

        instance.data.all().delete()

        for item in data:
            EmployeeData.objects.create(
                employee=instance,
                field=item['field'],
                value=item['value']
            )

        return instance