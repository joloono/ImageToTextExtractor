import streamlit as st
from PIL import Image
import pytesseract
from utils import process_image, convert_to_markdown
import io

# Page configuration
st.set_page_config(
    page_title="Image to Markdown",
    page_icon="📝",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        color: #FFFFFF;
    }
    
    h1, h2, h3 {
        color: #FFD700;
        font-weight: 600;
    }
    
    /* Upload Area Styles */
    .upload-area {
        border: 2px dashed #A3B18A;
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
        background-color: #2D2D2D;
        transition: all 0.3s ease;
        cursor: pointer;
        margin: 2rem 0;
    }
    
    .upload-area:hover {
        border-color: #D68A59;
        background-color: #363636;
    }
    
    .upload-icon {
        color: #A3B18A;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Text Area Styles */
    .stTextArea textarea {
        background-color: #2D2D2D;
        border: 1px solid #404040;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Inter', monospace;
        cursor: text;
    }

    .stTextArea textarea:hover {
        border-color: #A3B18A;
    }
    
    /* Footer Styles */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #A3B18A;
        font-size: 0.9rem;
    }
    
    .footer a {
        color: #D68A59;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .footer a:hover {
        color: #B97348;
    }

    /* Warning and Error Messages */
    .stAlert {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #404040;
    }

    .stSpinner {
        color: #A3B18A;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📝 Convert your Image to Text")
st.markdown("Transform to text with ease.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=['png', 'jpg', 'jpeg'],
    help="Supported formats: PNG, JPG, JPEG"
)

if uploaded_file is not None:
    try:
        # Display progress
        with st.spinner('Processing your image...'):
            # Read image
            image_bytes = uploaded_file.read()
            image = Image.open(io.BytesIO(image_bytes))
            
            # Display image
            st.image(image, caption='Uploaded Image', use_container_width=True)
            
            # Process image
            processed_image = process_image(image)
            
            # Extract text
            text = pytesseract.image_to_string(processed_image)
            
            if text.strip():
                # Convert to markdown
                markdown_text = convert_to_markdown(text)
                
                # Display markdown
                st.subheader("📄 Extracted Text (Markdown)")
                st.text_area(
                    "Extracted Text",
                    value=markdown_text,
                    height=200,
                    label_visibility="collapsed",
                    key="copyable_text"
                )
            else:
                st.warning("🔍 No text was detected in the image. Please try another image.")
                
    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")
else:
    # Display placeholder
    st.markdown(
        '<div class="upload-area">'
        '<div class="upload-icon">📤</div>'
        '<p>Drag and drop your image here<br>'
        '<small>or click to browse files</small></p>'
        '</div>',
        unsafe_allow_html=True
    )
