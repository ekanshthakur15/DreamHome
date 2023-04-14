from rest_framework import serializers
from .models import *

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = '__all__'

class ClientRentalSerializer(serializers.ModelSerializer):
    brno = serializers.PrimaryKeyRelatedField(queryset=Branches.objects.all())
    class Meta:
        model = Clientrental
        fields = '__all__'

class OwnerManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownermanage
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    brno = serializers.PrimaryKeyRelatedField(queryset = Branches.objects.all())
    class Meta:
        model = Staff
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    ownno = serializers.PrimaryKeyRelatedField(queryset = Ownermanage.objects.all())
    staffno = serializers.PrimaryKeyRelatedField(queryset = Staff.objects.all())
    brno = serializers.PrimaryKeyRelatedField(queryset=Branches.objects.all())
    class Meta:
        model = Property
        fields = '__all__'

class LeaseSerializer(serializers.ModelSerializer):
    pno = serializers.PrimaryKeyRelatedField(queryset = Property.objects.all())
    cno = serializers.PrimaryKeyRelatedField(queryset = Clientrental.objects.all())

    class Meta:
        model = Lease
        fields = '__all__'
        