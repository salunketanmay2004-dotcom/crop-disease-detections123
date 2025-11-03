"""OpenAI client wrapper for image analysis."""
from typing import Optional
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError
from logger_config import setup_logger
from variables import OPENAI_API_KEY, OPENAI_MODEL

logger = setup_logger(__name__)


class OpenAIClient:
    """Wrapper class for OpenAI API interactions."""

    def __init__(self):
        """Initialize OpenAI client with API key."""
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model = OPENAI_MODEL
            logger.info(f"OpenAI client initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise

    def analyze_image(
        self, image_base64: str, prompt: str
    ) -> Optional[str]:
        """
        Analyze image using OpenAI Vision API.

        Args:
            image_base64: Base64 encoded image string.
            prompt: Prompt for image analysis.

        Returns:
            Response text from OpenAI API.

        Raises:
            APIError: For OpenAI API errors.
            APIConnectionError: For connection errors.
            RateLimitError: For rate limit errors.
            ValueError: For invalid input.
        """
        try:
            logger.info("Starting image analysis with OpenAI")
            logger.debug(f"Prompt: {prompt[:100]}...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )

            response_text = response.choices[0].message.content
            logger.info("Image analysis completed successfully")
            logger.debug(f"Response length: {len(response_text)} characters")

            return response_text

        except RateLimitError as e:
            logger.error(f"OpenAI rate limit exceeded: {str(e)}")
            raise
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error: {str(e)}")
            raise
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during image analysis: {str(e)}")
            raise

    def analyze_with_structured_output(
        self, image_base64: str, system_prompt: str,
        response_format: dict
    ) -> Optional[str]:
        """
        Analyze image with structured output format.

        Args:
            image_base64: Base64 encoded image string.
            system_prompt: System prompt for analysis.
            response_format: Structured output format specification.

        Returns:
            JSON response string.

        Raises:
            APIError: For OpenAI API errors.
            Exception: For other errors.
        """
        try:
            logger.info("Starting structured output image analysis")

            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Please analyze this image and provide "
                                    "a detailed crop disease analysis."
                                )
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": (
                                        f"data:image/jpeg;base64,{image_base64}"
                                    )
                                }
                            }
                        ]
                    }
                ],
                response_format=response_format,
                max_tokens=2000,
                temperature=0.3
            )

            result = response.choices[0].message.content
            logger.info("Structured output analysis completed")
            return result

        except Exception as e:
            logger.error(
                f"Error in structured output analysis: {str(e)}"
            )
            raise

