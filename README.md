# Crop Disease Detection API

A RESTful API service for detecting crop diseases from images using OpenAI's GPT-4o mini model. The service can identify crops, detect diseases, and provide treatment recommendations.

## Features

- **Crop Detection**: Determines if an uploaded image contains crop-related content
- **Crop Information**: Extracts basic information about the crop (name, type, growth stage, health status)
- **Disease Detection**: Identifies diseases present on the crop with severity assessment
- **Treatment Recommendations**: Provides actionable recommendations to save the crop
- **Structured Output**: Uses Pydantic models for type-safe, validated responses
- **Comprehensive Logging**: Detailed logging throughout the application
- **Error Handling**: Robust exception handling and validation

## Project Structure

```
crop_detection_with_openai/
├── main.py                 # FastAPI application entry point
├── variables.py            # Environment variable loading
├── models.py              # Pydantic models for structured output
├── crop_detection.py       # Main crop detection service logic
├── openai_client.py        # OpenAI API client wrapper
├── logger_config.py        # Logger configuration
├── requirements.txt        # Python dependencies
├── env.example            # Example environment variables file
├── README.md              # This file
└── logs/                  # Log files directory (created automatically)
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key with access to GPT-4o mini model
- pip package manager

## Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd crop_detection_with_openai
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `env.example` to `.env`:
     ```bash
     # On Windows
     copy env.example .env
     
     # On Linux/Mac
     cp env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-actual-api-key-here
     ```

## Configuration

Edit the `.env` file to configure the following settings:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: `gpt-4o-mini`)
- `API_HOST`: Host address for the API (default: `0.0.0.0`)
- `API_PORT`: Port number for the API (default: `8000`)
- `MAX_FILE_SIZE_MB`: Maximum image file size in MB (default: `10`)
- `ALLOWED_EXTENSIONS`: Comma-separated list of allowed image extensions (default: `jpg,jpeg,png,webp`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Usage

### Starting the Server

Run the FastAPI application:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. Health Check

```bash
GET /health
```

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "crop_disease_detection"
}
```

#### 2. Root Endpoint

```bash
GET /
```

Returns API information and status.

#### 3. Detect Crop Disease

```bash
POST /detect
```

Upload an image to detect crop diseases.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with `file` field containing the image

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/crop_image.jpg"
```

**Example using Python requests:**
```python
import requests

url = "http://localhost:8000/detect"
with open("crop_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)
    print(response.json())
```

**Response Structure:**
```json
{
  "is_crop_image": true,
  "crop_info": {
    "crop_name": "Tomato",
    "crop_type": "Solanaceae",
    "growth_stage": "Fruiting",
    "health_status": "Affected"
  },
  "diseases": [
    {
      "disease_name": "Early Blight",
      "severity": "moderate",
      "confidence": 0.85,
      "affected_areas": ["leaves", "stems"]
    }
  ],
  "recommendations": {
    "immediate_actions": [
      "Remove affected leaves",
      "Improve air circulation"
    ],
    "preventive_measures": [
      "Water at base of plant",
      "Avoid overhead watering"
    ],
    "treatment_methods": [
      "Apply fungicide",
      "Use organic treatments"
    ],
    "chemical_treatments": [
      "Chlorothalonil",
      "Mancozeb"
    ],
    "organic_treatments": [
      "Neem oil",
      "Copper-based fungicides"
    ]
  },
  "analysis_summary": "Analysis completed successfully.",
  "confidence_score": 0.85
}
```

### API Documentation

Once the server is running, you can access interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Code Standards

This project adheres to:

- **PEP 8**: Python code style guidelines
- **Type Hints**: Comprehensive type annotations
- **Pydantic Models**: Structured data validation
- **Error Handling**: Comprehensive exception handling
- **Logging**: Detailed logging throughout the application

## Logging

Logs are written to:
- **File**: `logs/crop_detection.log` (rotating, max 10MB, 5 backups)
- **Console**: Standard output with configurable log level

Log levels can be configured via the `LOG_LEVEL` environment variable:
- `DEBUG`: Detailed debugging information
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid file format, empty file, or validation errors
- **500 Internal Server Error**: Unexpected server errors
- **OpenAI API Errors**: Properly handled with appropriate error messages

## Testing

You can test the API using the interactive Swagger documentation at `/docs` or use curl/Postman.

**Test with a sample image:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -F "file=@sample_crop_image.jpg"
```

## Limitations

- Image size limit: Configurable (default 10MB)
- Supported formats: JPG, JPEG, PNG, WEBP
- Model dependency: Requires OpenAI API access and credits
- Response time: Depends on OpenAI API response time

## Troubleshooting

1. **Import Errors**: Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **OpenAI API Errors**: Verify your API key is correct and has sufficient credits.

3. **File Upload Errors**: Check file size and format restrictions.

4. **Port Already in Use**: Change the `API_PORT` in `.env` file.

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, please check the logs in `logs/crop_detection.log` for detailed error messages.

