from rest_framework import serializers
from pennlabs.mixins import ManyToManySaveMixin
from models import Student

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("id", "name")

class UserSerializer(ManyToManySaveMixin, serializers.ModelSerializer):
    school = SchoolSerializer(many=True)

    class Meta:
        model = Student
        fields = ("major", "school", "graduation_year")

        save_related_fields = ["major", "school"]