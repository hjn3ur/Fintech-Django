from rest_framework import serializers
from .models import Report, Picture
from django.contrib.auth.models import User


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('report_id', 'public', 'private', 'company_time', 'company_update', 'company_name', 'company_ceo',
                  'company_email', 'company_phone', 'company_state', 'company_country', 'company_sector',
                  'company_industry', 'company_project', 'company_file')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return User.objects.get(username=validated_data)
        # return Report.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.report_id = validated_data.get('report_id', instance.report_id)
        instance.public = validated_data.get('public', instance.public)
        instance.company_time = validated_data.get('company_time', instance.company_time)

        instance.save()
        return instance


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('files_id', 'picfile', 'timestamp', 'owner', 'investor')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return User.objects.get(username=validated_data)
        # return Report.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.files_id = validated_data.get('files_id', instance.files_id)
        instance.picfile = validated_data.get('picfile', instance.picfile)
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)

        instance.save()
        return instance
