import os
import requests

BASE_URL = 'http://127.0.0.1:8000'
IMAGE_PATH = 'test_food.jpg'

def test_photo_endpoint(tier: str):
    print(f"\n--- Testing Photo Endpoint ({tier.upper()}) ---")
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Please place a sample image named '{IMAGE_PATH}' in this folder first!")
        return

    with open(IMAGE_PATH, 'rb') as f:
        files = {'file': (IMAGE_PATH, f, 'image/jpeg')}
        data = {'user_tier': tier}
        res = requests.post(f"{BASE_URL}/recipe/photo", files=files, data=data)
        
        if res.status_code == 200:
            print(res.json()['recipe'])
        else:
            print(f"Error: {res.status_code} - {res.text}")

if __name__ == '__main__':
    test_photo_endpoint('premium')
