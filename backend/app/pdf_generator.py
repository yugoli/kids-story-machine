from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
import os
import tempfile
import requests
from typing import Optional

def generate_pdf(story_text: str, image_url: Optional[str] = None):
    """Generates a PDF from the given story text and optional image URL."""
    print(f"generate_pdf called with story_text length: {len(story_text)}")
    # Create a temporary file to save the PDF
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    print(f"Temporary PDF file created at: {path}")

    doc = SimpleDocTemplate(path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add image if URL is provided
    if image_url:
        print(f"Image URL provided: {image_url}")
        try:
            response = requests.get(image_url)
            response.raise_for_status() # Raise an exception for bad status codes
            print(f"Image request status code: {response.status_code}")
            img_data = response.content
            img = ImageReader(img_data)
            print("ImageReader created successfully.")

            # Add image to story, scale it down if necessary
            # You might need to adjust width/height based on desired size and aspect ratio
            img_width, img_height = img.getSize()
            aspect = img_height / float(img_width)
            # Set image width to 80% of page width, maintain aspect ratio
            img_width = letter[0] * 0.8
            img_height = img_width * aspect

            story.append(Image(img, width=img_width, height=img_height))
            print("Image appended to story.")
            story.append(Spacer(1, 12)) # Add some space after the image
        except Exception as e:
            print(f"Error adding image to PDF: {e}")
            # Log the image URL that failed
            print(f"Failed image URL: {image_url}")
            # Continue generating PDF without the image if download fails

    # Add story text to the PDF
    # Split text into paragraphs if needed, for simplicity adding as one block
    story.append(Paragraph(story_text.replace('\n', '<br/>'), styles['Normal']))
    story.append(Spacer(1, 12)) # Add some space

    print(f"Number of elements in story: {len(story)}")
    # Build the PDF
    try:
        doc.build(story)
        print("PDF built successfully.")
    except Exception as e:
        print(f"Error during PDF build: {e}")
        return None # Return None if build fails

    # Check if the file exists and has content
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"Generated PDF file exists and has size: {os.path.getsize(path)} bytes")
    else:
        print("Generated PDF file does not exist or is empty.")
        return None # Return None if file is not valid


    # Return the path to the generated PDF
    return path

if __name__ == '__main__':
    # Example usage
    sample_story = """Once upon a time, in a cozy little forest, lived a brave rabbit named Barnaby and a clever fox named Finn.
Barnaby loved carrots, and Finn loved solving puzzles.
One sunny morning, they decided to go on an adventure to find the legendary Golden Carrot, hidden deep within the Whispering Woods.
They worked together, Barnaby using his speed to navigate tricky paths and Finn using his wit to figure out riddles left by ancient forest creatures.
After overcoming many challenges, they found the Golden Carrot, sparkling brightly.
They learned that working together made them stronger and their friendship even more valuable than any treasure.
And they lived happily ever after, sharing carrots and solving puzzles together."""
    # Example with a placeholder image URL (replace with a real one for testing)
    sample_image_url = "https://via.placeholder.com/500"
    pdf_file_path = generate_pdf(sample_story, sample_image_url)
    print(f"PDF generated at: {pdf_file_path}")
