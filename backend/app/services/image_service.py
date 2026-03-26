import httpx
from app.core.config import settings
import json

class CloudImageService:
    """Cloud Image Generation Service (using SiliconFlow/OpenAI compatible API)"""

    def __init__(self):
        self.api_key = settings.IMAGE_API_KEY
        self.api_url = settings.IMAGE_API_URL
        self.model = settings.IMAGE_MODEL

    async def generate_image(self, prompt: str) -> str:
        """
        Call Cloud Image API to generate an image based on the prompt.
        
        Args:
            prompt: The text prompt for image generation
            
        Returns:
            The URL of the generated image
        """
        if not self.api_key:
            raise ValueError("IMAGE_API_KEY is not configured in .env file.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Compatible payload for SiliconFlow / OpenAI
        payload = {
            "model": self.model,
            "prompt": prompt,
            "image_size": "1024x1024"
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    print(f"Image generation failed: {response.text}")
                    raise Exception(f"API Error {response.status_code}: {response.text}")

                data = response.json()
                
                # Handle different return structures (SiliconFlow vs standard OpenAI)
                if "images" in data and len(data["images"]) > 0:
                    return data["images"][0]["url"]
                elif "data" in data and len(data["data"]) > 0:
                    return data["data"][0]["url"]
                else:
                    raise Exception("Unexpected response format from Image API")

        except Exception as e:
            print(f"Error calling Image API: {e}")
            raise e

cloud_image_service = CloudImageService()
