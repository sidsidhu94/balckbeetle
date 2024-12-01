from rest_framework import serializers
from .models import Institute, Batch

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ['id', 'name', 'code']

    def validate_name(self, value):
        """
        Check if the institute with the same name already exists.
        """
        if Institute.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Institute with this name already exists.")
        return value

    def validate_code(self, value):
        """
        Check if the institute with the same code already exists.
        """
        if Institute.objects.filter(code__iexact=value).exists():
            raise serializers.ValidationError("Institute with this code already exists.")
        return value

class BatchSerializer(serializers.ModelSerializer):
    # institute = InstituteSerializer()
    institute = serializers.PrimaryKeyRelatedField(queryset=Institute.objects.all())

    class Meta:
        model = Batch
        fields = ['id', 'institute', 'batch_name', 'referral_code']

    def validate(self, data):
        """
        Validate that the combination of institute and batch_name is unique.
        """
        institute = data.get('institute')
        batch_name = data.get('batch_name')

        # Check if a batch with the same name exists under the same institute
        if Batch.objects.filter(institute=institute, batch_name__iexact=batch_name).exists():
            raise serializers.ValidationError(
                {"batch_name": "A batch with this name already exists under the same institute."}
            )
            

        return data

    def create(self, validated_data):
        """
        Custom create method to handle batch creation and referral code generation.
        """
        # Extract the validated institute and batch_name
        institute = validated_data.get('institute')
        batch_name = validated_data.get('batch_name')

        # Create the Batch instance (this triggers referral code generation)
        batch = Batch.objects.create(
            institute=institute,
            batch_name=batch_name
        )

        # Save and return the batch instance
        return batch

    
    
