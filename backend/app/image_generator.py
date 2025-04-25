import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
# Assumes OPENAI_API_KEY is set in the environment or a .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt: str):
    """Generates an image based on the given prompt using OpenAI's DALL-E."""
    try:
        response = client.images.generate(
            model="dall-e-2",  # or "dall-e-3" if preferred and available
            prompt=prompt,
            size="512x512", # or "1024x1024"
            quality="standard", # or "hd" for dall-e-3
            n=1, # number of images to generate
        )
        # The URL of the generated image
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    sample_prompt = "A whimsical illustration of a brave rabbit and a clever fox exploring a magical forest."
    image_url = generate_image(sample_prompt)
    if image_url:
        print(f"Generated image URL: {image_url}")
    else:
        print("Failed to generate image.")
