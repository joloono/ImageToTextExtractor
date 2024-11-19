from PIL import Image
import numpy as np
import re

def process_image(image):
    """
    Process image for better OCR results
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Convert to grayscale
    if len(img_array.shape) == 3:
        gray = np.dot(img_array[...,:3], [0.2989, 0.5870, 0.1140])
    else:
        gray = img_array
    
    # Normalize
    normalized = ((gray - gray.min()) / (gray.max() - gray.min()) * 255).astype(np.uint8)
    
    # Convert back to PIL Image
    processed = Image.fromarray(normalized)
    
    return processed

def convert_to_markdown(text):
    """
    Convert extracted text to markdown format
    """
    # Clean up text
    text = text.strip()
    
    # Split into lines
    lines = text.split('\n')
    
    # Process lines
    markdown_lines = []
    in_list = False
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            markdown_lines.append('')
            continue
        
        # Check for headings
        if re.match(r'^[A-Z\s]{3,}$', line.strip()):
            markdown_lines.append(f'## {line.strip()}')
        
        # Check for list items
        elif line.strip().startswith(('•', '-', '*', '○')):
            if not in_list:
                in_list = True
            line = re.sub(r'^[•\-*○]\s*', '- ', line.strip())
            markdown_lines.append(line)
        
        # Regular text
        else:
            if in_list:
                in_list = False
                markdown_lines.append('')
            markdown_lines.append(line)
    
    return '\n'.join(markdown_lines)
