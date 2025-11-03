"""Main FastAPI application for crop disease detection."""
import base64
from io import BytesIO
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from logger_config import setup_logger
from variables import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    API_HOST,
    API_PORT
)
from crop_detection import CropDetectionService
from models import CropDetectionResponse

# Initialize logger
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Crop Disease Detection API",
    description="API for detecting crop diseases using OpenAI GPT-4o mini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
crop_service = CropDetectionService()


def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file.

    Args:
        file: Uploaded file object.

    Raises:
        HTTPException: If validation fails.
    """
    try:
        # Check file extension
        file_extension = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        if file_extension not in ALLOWED_EXTENSIONS:
            logger.warning(
                f"Invalid file extension: {file_extension}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid file type. Allowed extensions: "
                    f"{', '.join(ALLOWED_EXTENSIONS)}"
                )
            )

        # Check file size (will be validated after reading)
        logger.info(f"Validating image file: {file.filename}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File validation error: {str(e)}"
        )


def encode_image_to_base64(image_bytes: bytes) -> str:
    """
    Encode image bytes to base64 string.

    Args:
        image_bytes: Image file bytes.

    Returns:
        Base64 encoded string.

    Raises:
        HTTPException: If encoding fails.
    """
    try:
        # Validate and process image
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Save to bytes buffer
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        image_bytes = buffer.getvalue()

        # Check file size
        size_mb = len(image_bytes) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            logger.warning(f"Image size {size_mb:.2f}MB exceeds limit")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Image size ({size_mb:.2f}MB) exceeds maximum "
                    f"allowed size ({MAX_FILE_SIZE_MB}MB)"
                )
            )

        # Encode to base64
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        logger.info(f"Image encoded successfully, size: {size_mb:.2f}MB")
        return encoded

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error encoding image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image processing error: {str(e)}"
        )


@app.post(
    "/detect",
    response_model=CropDetectionResponse,
    status_code=status.HTTP_200_OK
)
async def detect_crop_disease(file: UploadFile = File(...)):
    """
    Detect crop disease from uploaded image.

    Args:
        file: Image file to analyze.

    Returns:
        CropDetectionResponse with analysis results.

    Raises:
        HTTPException: For validation or processing errors.
    """
    try:
        logger.info(f"Received image upload request: {file.filename}")

        # Validate file
        validate_image_file(file)

        # Read file content
        file_content = await file.read()
        if not file_content:
            logger.error("Empty file received")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )

        # Encode image to base64
        image_base64 = encode_image_to_base64(file_content)

        # Perform crop disease detection
        result = crop_service.detect_crop_disease(image_base64)

        logger.info("Crop disease detection completed successfully")
        return result

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.

    Args:
        request: Request object.
        exc: Exception object.

    Returns:
        JSON error response.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "error": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Crop Disease Detection API server")
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )

