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
    }
    
    h1, h2, h3 {
        color: #2C3E50;
        font-weight: 600;
    }
    
    /* Button Styles */
    .stButton>button {
        width: 100%;
        background-color: #A3B18A !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #8B9B76 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Upload Area Styles */
    .upload-area {
        border: 2px dashed #A3B18A;
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
        background-color: #F8F9FA;
        transition: all 0.3s ease;
        cursor: pointer;
        margin: 2rem 0;
    }
    
    .upload-area:hover {
        border-color: #D68A59;
        background-color: #FAFBFC;
    }
    
    .upload-icon {
        color: #A3B18A;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Success Message Styles */
    .success-text {
        color: #2C3E50;
        background-color: #E8F0E3;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #A3B18A;
        margin: 1rem 0;
    }
    
    /* Text Area Styles */
    .stTextArea textarea {
        border-radius: 8px;
        border-color: #E2E8F0;
        padding: 1rem;
        font-family: 'Inter', monospace;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #A3B18A;
        box-shadow: 0 0 0 2px rgba(163, 177, 138, 0.2);
    }
    
    /* Footer Styles */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6B7280;
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
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📝 Image to Markdown Converter")
st.markdown("Transform your images into beautifully formatted markdown text with ease.")

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
            st.image(image, caption='Uploaded Image', use_column_width=True)
            
            # Process image
            processed_image = process_image(image)
            
            # Extract text
            text = pytesseract.image_to_string(processed_image)
            
            if text.strip():
                # Convert to markdown
                markdown_text = convert_to_markdown(text)
                
                # Display markdown
                st.subheader("📄 Extracted Text (Markdown)")
                st.text_area("", markdown_text, height=200)
                
                # Copy button
                if st.button("📋 Copy to Clipboard"):
                    st.code(markdown_text)
                    st.markdown(
                        '<p class="success-text">✨ Text copied to clipboard!</p>',
                        unsafe_allow_html=True
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

# Footer
st.markdown(
    '<div class="footer">'
    'Made with ❤️ using Streamlit and Tesseract OCR<br>'
    '<a href="#">View Documentation</a>'
    '</div>',
    unsafe_allow_html=True
)
