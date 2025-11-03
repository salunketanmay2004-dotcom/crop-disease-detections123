"""Pydantic models for structured output."""
from typing import List, Optional
from pydantic import BaseModel, Field


class CropBasicInfo(BaseModel):
    """Basic information about the crop."""

    crop_name: str = Field(
        ..., description="Name of the crop identified in the image"
    )
    crop_type: Optional[str] = Field(
        None, description="Type or category of the crop"
    )
    growth_stage: Optional[str] = Field(
        None, description="Current growth stage of the crop"
    )
    health_status: Optional[str] = Field(
        None, description="Overall health status of the crop"
    )


class DiseaseInfo(BaseModel):
    """Information about a detected disease."""

    disease_name: str = Field(
        ..., description="Name of the disease detected"
    )
    affected_areas: Optional[List[str]] = Field(
        None, description="Parts of the crop affected by the disease"
    )


class TreatmentRecommendation(BaseModel):
    """Treatment recommendations for crop disease."""

    immediate_actions: List[str] = Field(
        ..., description="Immediate actions to take"
    )
    preventive_measures: List[str] = Field(
        ..., description="Preventive measures to avoid further spread"
    )
    treatment_methods: List[str] = Field(
        ..., description="Treatment methods for the disease"
    )
    chemical_treatments: Optional[List[str]] = Field(
        None, description="Chemical treatment options if applicable"
    )
    organic_treatments: Optional[List[str]] = Field(
        None, description="Organic treatment options if applicable"
    )


class CropDetectionResponse(BaseModel):
    """Complete response model for crop detection API."""

    is_crop_image: bool = Field(
        ..., description="Whether the uploaded image contains a crop"
    )
    crop_info: Optional[CropBasicInfo] = Field(
        None, description="Basic information about the crop"
    )
    diseases: Optional[List[DiseaseInfo]] = Field(
        None, description="List of diseases detected on the crop"
    )
    recommendations: Optional[TreatmentRecommendation] = Field(
        None, description="Treatment recommendations"
    )
    analysis_summary: str = Field(
        ..., description="Summary of the analysis performed"
    )
