import os
import shutil
import requests
import cv2
import sys


def main():
    access_token: str = os.environ.get("ACCESS_TOKEN", "").strip()

    if access_token.strip() == "":
        print("Error: set ACCESS_TOKEN")
        sys.exit(1)

    challenge_url = f"https://hackattic.com/challenges/reading_qr/problem/?access_token={access_token}"
    challenge: requests.Response = requests.get(challenge_url)
    challenge.raise_for_status()
    response = challenge.json()
    print(response)
    image_url = response["image_url"]
    image_request = requests.get(image_url, stream=True)
    image_request.raise_for_status()
    with open("image.png", "wb") as f:
        image_request.raw.decode_content = True
        shutil.copyfileobj(image_request.raw, f)
    print("wrote image to image.png")
    image = cv2.imread("image.png")
    detector = cv2.QRCodeDetector()
    text, *_ = detector.detectAndDecode(image)
    print(text)

    solution_url = challenge_url.replace("problem/", "solve")
    response = requests.post(solution_url, json={"code": text})
    print(response.text)

    response.raise_for_status()


if __name__ == "__main__":
    main()
