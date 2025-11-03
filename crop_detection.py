"""Crop detection service logic."""
import json
from typing import Optional
from pydantic import ValidationError
from logger_config import setup_logger
from models import CropDetectionResponse, CropBasicInfo, DiseaseInfo, \
    TreatmentRecommendation
from openai_client import OpenAIClient

logger = setup_logger(__name__)


class CropDetectionService:
    """Service class for crop disease detection."""

    def __init__(self):
        """Initialize crop detection service."""
        self.openai_client = OpenAIClient()
        logger.info("CropDetectionService initialized")

    def _create_detection_prompt(self) -> str:
        """
        Create prompt for crop detection and analysis.

        Returns:
            Formatted prompt string.
        """
        prompt = """
        Analyze the uploaded image and determine the following:

        1. Is this image related to crops or agriculture?
        2. If yes, identify the basic information about the crop:
           - Crop name
           - Crop type
           - Growth stage (if visible)
           - Overall health status

        3. Detect any diseases present on the crop:
           - Disease name
           - Confidence level of detection

        4. Provide recommendations to save the crop:
           - Immediate actions needed
           - Preventive measures
           - Treatment methods (both chemical and organic)
           - Best practices

        Please provide a comprehensive analysis in JSON format with the
        following structure:
        {
            "is_crop_image": boolean,
            "crop_info": {
                "crop_name": string,
                "crop_type": string,
                "growth_stage": string,
                "health_status": string
            },
            "diseases": [
                {
                    "disease_name": string,
                    "affected_areas": [string]
                }
            ],
            "recommendations": {
                "immediate_actions": [string],
                "preventive_measures": [string],
                "treatment_methods": [string],
                "chemical_treatments": [string],
                "organic_treatments": [string]
            },
            "analysis_summary": string,
        }

        If the image is not crop-related, set "is_crop_image" to false and
        provide an explanation in "analysis_summary".
        """
        return prompt

    def _parse_openai_response(
        self, response_text: str
    ) -> Optional[dict]:
        """
        Parse OpenAI response text to extract JSON.

        Args:
            response_text: Raw response text from OpenAI.

        Returns:
            Parsed JSON dictionary or None if parsing fails.
        """
        try:
            # Try to extract JSON from markdown code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            else:
                json_str = response_text.strip()

            # Remove leading/trailing whitespace and newlines
            json_str = json_str.strip()

            parsed_data = json.loads(json_str)
            logger.info("Successfully parsed OpenAI response")
            return parsed_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from response: {str(e)}")
            logger.debug(f"Response text: {response_text[:500]}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {str(e)}")
            return None

    def _validate_and_parse_response(
        self, parsed_data: dict
    ) -> Optional[CropDetectionResponse]:
        """
        Validate and parse response data into Pydantic model.

        Args:
            parsed_data: Parsed JSON dictionary.

        Returns:
            Validated CropDetectionResponse model or None.
        """
        try:
            # Handle case when image is not crop-related
            if not parsed_data.get("is_crop_image", False):
                logger.info("Image is not crop-related")
                return CropDetectionResponse(
                    is_crop_image=False,
                    analysis_summary=parsed_data.get(
                        "analysis_summary",
                        "Image does not appear to contain crops."
                    ),
                    confidence_score=parsed_data.get("confidence_score")
                )

            # Parse crop info
            crop_info_data = parsed_data.get("crop_info", {})
            crop_info = None
            if crop_info_data:
                crop_info = CropBasicInfo(**crop_info_data)

            # Parse diseases
            diseases_data = parsed_data.get("diseases", [])
            diseases = None
            if diseases_data:
                diseases = [DiseaseInfo(**disease) for disease in diseases_data]

            # Parse recommendations
            recommendations_data = parsed_data.get("recommendations", {})
            recommendations = None
            if recommendations_data:
                recommendations = TreatmentRecommendation(
                    **recommendations_data
                )

            response = CropDetectionResponse(
                is_crop_image=True,
                crop_info=crop_info,
                diseases=diseases,
                recommendations=recommendations,
                analysis_summary=parsed_data.get(
                    "analysis_summary",
                    "Analysis completed successfully."
                ),
                confidence_score=parsed_data.get("confidence_score")
            )

            logger.info("Successfully validated response data")
            return response

        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            logger.debug(f"Validation errors: {e.errors()}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error validating response: {str(e)}")
            return None

    def detect_crop_disease(
        self, image_base64: str
    ) -> CropDetectionResponse:
        """
        Main method to detect crop disease from image.

        Args:
            image_base64: Base64 encoded image string.

        Returns:
            CropDetectionResponse model with analysis results.

        Raises:
            Exception: For analysis failures.
        """
        try:
            logger.info("Starting crop disease detection")

            if not image_base64:
                logger.error("Empty image data provided")
                raise ValueError("Image data cannot be empty")

            prompt = self._create_detection_prompt()

            # Get analysis from OpenAI
            response_text = self.openai_client.analyze_image(
                image_base64, prompt
            )

            if not response_text:
                logger.error("Empty response from OpenAI")
                raise ValueError("Failed to get response from OpenAI")

            # Parse response
            parsed_data = self._parse_openai_response(response_text)

            if not parsed_data:
                logger.error("Failed to parse OpenAI response")
                raise ValueError("Failed to parse analysis response")

            # Validate and create response model
            validated_response = self._validate_and_parse_response(
                parsed_data
            )

            if not validated_response:
                logger.error("Failed to validate response data")
                raise ValueError("Response validation failed")

            logger.info("Crop disease detection completed successfully")
            return validated_response

        except Exception as e:
            logger.error(f"Error in crop disease detection: {str(e)}")
            raise

