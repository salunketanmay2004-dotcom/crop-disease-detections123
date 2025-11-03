"""Streamlit UI for Crop Disease Detection."""
import streamlit as st
import base64
from PIL import Image
import io
from typing import Optional
import os
from dotenv import load_dotenv
from crop_detection import CropDetectionService

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Crop Disease Detection",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
    .disease-box {
        background-color: #fff5f5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .recommendation-box {
        background-color: #f0fff0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E8B57;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #228B22;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize crop detection service
@st.cache_resource
def get_crop_service():
    """Initialize and cache the crop detection service."""
    return CropDetectionService()


def encode_image_to_base64(image_bytes: bytes) -> str:
    """
    Encode image bytes to base64 string.
    
    Args:
        image_bytes: Image file bytes.
        
    Returns:
        Base64 encoded string.
    """
    return base64.b64encode(image_bytes).decode("utf-8")


def display_crop_info(crop_info: dict) -> None:
    """Display crop basic information."""
    if crop_info:
        st.markdown("### 🌱 Crop Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Crop Name:** {crop_info.get('crop_name', 'N/A')}")
            st.markdown(f"**Crop Type:** {crop_info.get('crop_type', 'N/A')}")
        
        with col2:
            st.markdown(f"**Growth Stage:** {crop_info.get('growth_stage', 'N/A')}")
            st.markdown(f"**Health Status:** {crop_info.get('health_status', 'N/A')}")


def display_diseases(diseases: list) -> None:
    """Display detected diseases."""
    if diseases:
        st.markdown("### 🦠 Detected Diseases")
        
        for idx, disease in enumerate(diseases, 1):
            with st.container():
                disease_name = disease.get('disease_name', 'Unknown')
                severity = disease.get('severity', 'N/A')
                confidence = disease.get('confidence')
                affected_areas = disease.get('affected_areas', [])
                affected_areas_str = ', '.join(affected_areas) if affected_areas else 'N/A'
                
                severity_emoji = {
                    'mild': '🟡',
                    'moderate': '🟠',
                    'severe': '🔴'
                }.get(severity.lower(), '⚪')
                
                confidence_str = f" ({confidence:.0%})" if confidence else ""
                
                st.markdown(f"""
                <div class="disease-box">
                    <h4>{severity_emoji} Disease #{idx}: {disease_name}</h4>
                    <p><strong>Severity:</strong> {severity.title()}{confidence_str}</p>
                    <p><strong>Affected Areas:</strong> {affected_areas_str}</p>
                </div>
                """, unsafe_allow_html=True)


def display_recommendations(recommendations: dict) -> None:
    """Display treatment recommendations."""
    if recommendations:
        st.markdown("### 💊 Treatment Recommendations")
        
        # Immediate Actions
        if recommendations.get('immediate_actions'):
            st.markdown("**🚨 Immediate Actions:**")
            for action in recommendations['immediate_actions']:
                st.markdown(f"- {action}")
        
        # Preventive Measures
        if recommendations.get('preventive_measures'):
            st.markdown("**🛡️ Preventive Measures:**")
            for measure in recommendations['preventive_measures']:
                st.markdown(f"- {measure}")
        
        # Treatment Methods
        if recommendations.get('treatment_methods'):
            st.markdown("**🔧 Treatment Methods:**")
            for method in recommendations['treatment_methods']:
                st.markdown(f"- {method}")
        
        # Chemical Treatments
        if recommendations.get('chemical_treatments'):
            st.markdown("**🧪 Chemical Treatments:**")
            for treatment in recommendations['chemical_treatments']:
                st.markdown(f"- {treatment}")
        
        # Organic Treatments
        if recommendations.get('organic_treatments'):
            st.markdown("**🌿 Organic Treatments:**")
            for treatment in recommendations['organic_treatments']:
                st.markdown(f"- {treatment}")


def main():
    """Main Streamlit application."""
    # Header
    st.markdown('<h1 class="main-header">🌾 Crop Disease Detection</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload an image to detect crop diseases and get treatment recommendations</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("**Mode:** Direct Function Call")
        
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. Upload an image of a crop
        2. Click 'Detect Disease' button
        3. View the analysis results
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This application uses AI to:
        - Detect if image contains crops
        - Identify crop information
        - Detect diseases
        - Provide treatment recommendations
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Upload an image of a crop to analyze"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Analyze button
            analyze_button = st.button("🔍 Detect Disease", type="primary", use_container_width=True)
            
            if analyze_button:
                with st.spinner("Analyzing image... Please wait. This may take a moment."):
                    try:
                        # Get crop detection service
                        crop_service = get_crop_service()
                        
                        # Read image bytes
                        image_bytes = uploaded_file.getvalue()
                        
                        # Convert image to RGB if necessary and encode to base64
                        pil_image = Image.open(io.BytesIO(image_bytes))
                        if pil_image.mode != "RGB":
                            pil_image = pil_image.convert("RGB")
                        
                        # Save to bytes buffer as JPEG
                        buffer = io.BytesIO()
                        pil_image.save(buffer, format="JPEG", quality=85)
                        image_bytes = buffer.getvalue()
                        
                        # Encode to base64
                        image_base64 = encode_image_to_base64(image_bytes)
                        
                        # Call crop detection service directly
                        result = crop_service.detect_crop_disease(image_base64)
                        
                        # Convert Pydantic model to dict for display
                        result_dict = result.model_dump()
                        
                        # Store result in session state
                        st.session_state['analysis_result'] = result_dict
                        st.success("✅ Analysis completed successfully!")
                        
                        # Auto-scroll to results
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.exception(e)
    
    with col2:
        st.markdown("### 📊 Analysis Results")
        
        if 'analysis_result' in st.session_state:
            result = st.session_state['analysis_result']
            
            # Display analysis summary
            if result.get('analysis_summary'):
                st.markdown("### 📝 Analysis Summary")
                st.info(result['analysis_summary'])
            
            # Check if image is crop-related
            if not result.get('is_crop_image', False):
                st.warning("⚠️ This image does not appear to contain crop-related content.")
                if result.get('analysis_summary'):
                    st.info(result['analysis_summary'])
            else:
                st.success("✅ Crop detected in image!")
                
                # Display crop information
                if result.get('crop_info'):
                    display_crop_info(result['crop_info'])
                
                # Display diseases
                if result.get('diseases'):
                    display_diseases(result['diseases'])
                else:
                    st.success("🎉 No diseases detected! Your crop appears healthy.")
                
                # Display recommendations
                if result.get('recommendations'):
                    display_recommendations(result['recommendations'])
            
            # Option to clear results
            st.markdown("---")
            if st.button("🔄 Clear Results"):
                if 'analysis_result' in st.session_state:
                    del st.session_state['analysis_result']
                st.rerun()
        else:
            st.info("👈 Upload an image and click 'Detect Disease' to see results here.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Powered by OpenAI GPT-4o mini | Crop Disease Detection System</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

