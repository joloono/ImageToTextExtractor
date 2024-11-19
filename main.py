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
    .stButton>button {
        width: 100%;
    }
    .upload-text {
        text-align: center;
        padding: 2rem;
    }
    .success-text {
        color: #0f5132;
        background-color: #d1e7dd;
        padding: 1rem;
        border-radius: 0.25rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📝 Image to Markdown Converter")
st.markdown("Upload an image to extract text and convert it to markdown format.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=['png', 'jpg', 'jpeg'],
    help="Supported formats: PNG, JPG, JPEG"
)

if uploaded_file is not None:
    try:
        # Display progress
        with st.spinner('Processing image...'):
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
                st.subheader("Extracted Text (Markdown)")
                st.text_area("", markdown_text, height=200)
                
                # Copy button
                if st.button("📋 Copy to Clipboard"):
                    st.code(markdown_text)
                    st.markdown(
                        '<p class="success-text">✅ Text copied to clipboard!</p>',
                        unsafe_allow_html=True
                    )
            else:
                st.warning("No text was detected in the image. Please try another image.")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    # Display placeholder
    st.markdown(
        '<div class="upload-text">'
        '<img src="assets/placeholder.svg" width="100">'
        '<p>Drag and drop an image here</p>'
        '</div>',
        unsafe_allow_html=True
    )

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit and Tesseract OCR"
)
