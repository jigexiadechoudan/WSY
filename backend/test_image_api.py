import asyncio
import os
import json
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def test_siliconflow_api():
    api_key = os.getenv("IMAGE_API_KEY")
    api_url = os.getenv("IMAGE_API_URL", "https://api.siliconflow.cn/v1/images/generations")
    model = os.getenv("IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")

    # Use an explicitly known free model from SiliconFlow
    model = "black-forest-labs/FLUX.1-schnell"

    if not api_key or "your-siliconflow-api-key-here" in api_key:
        print("❌ Error: IMAGE_API_KEY is not properly set in .env")
        return

    print(f"🔍 Testing API Key: {api_key[:8]}...{api_key[-4:]}")
    print(f"🔗 API URL: {api_url}")
    print(f"🤖 Model: {model}")
    print("-" * 50)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Check user account info
    print("\n� Checking Account Balance...")
    try:
        user_info_url = "https://api.siliconflow.cn/v1/user/info"
        async with httpx.AsyncClient() as client:
            user_response = await client.get(user_info_url, headers=headers)
            if user_response.status_code == 200:
                user_data = user_response.json()
                print(f"User Info: {json.dumps(user_data, indent=2)}")
            else:
                print(f"Failed to get user info: {user_response.text}")
    except Exception as e:
        print(f"Failed to check user info: {e}")

    payload = {
        "model": "Kwai-Kolors/Kolors",
        "prompt": "a beautiful chinese traditional porcelain vase, high quality, 8k resolution",
        "image_size": "1024x1024"
    }

    try:
        print("⏳ Sending request to SiliconFlow API...")
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                api_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API Request Successful!")
                
                # Try to extract the image URL
                image_url = None
                if "images" in data and len(data["images"]) > 0:
                    image_url = data["images"][0].get("url")
                elif "data" in data and len(data["data"]) > 0:
                    image_url = data["data"][0].get("url")
                    
                if image_url:
                    print(f"🎉 Successfully generated image URL:\n{image_url}")
                else:
                    print("⚠️ Response format unexpected, but request succeeded.")
                    print(json.dumps(data, indent=2))
            else:
                print(f"❌ API Request Failed with status code: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"Error details: {response.text}")

    except Exception as e:
        print(f"❌ An error occurred while calling the API: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_siliconflow_api())