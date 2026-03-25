"""
API Serializers — DRF serializers for request/response validation.

Placeholder for Django REST Framework serializers that bridge
Pydantic DTOs with DRF's serialization layer.
"""

from rest_framework import serializers


class ProjectSerializer(serializers.Serializer):
    """Serializer for project CRUD operations."""

    project_id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, default="")


class PipelineRunSerializer(serializers.Serializer):
    """Serializer for pipeline run requests."""

    project_id = serializers.CharField()
    workflow_type = serializers.IntegerField(min_value=1, max_value=3)
    arlo_enabled = serializers.BooleanField(default=True)
    llm_mappings = serializers.DictField(child=serializers.ListField(child=serializers.CharField()))
    extraction_strategy = serializers.CharField(required=False, allow_null=True)
    target_framework = serializers.CharField(default="C4_Container")
