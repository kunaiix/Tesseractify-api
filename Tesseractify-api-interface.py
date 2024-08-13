import requests
import json
import base64
import os


def encode_image_to_base64(image_path: str) -> str:
    # encoding image to base64
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image


def save_json_to_file(data: dict, output_file: str):
    # saves ocr results as json file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"Results saved to {output_file}")


def process_image(image_path: str):
    if not os.path.exists(image_path):
        # checks for image existence
        print(f"Error: File '{image_path}' does not exist.")
        return

    # image payload in base64 to send to api
    base64_image = encode_image_to_base64(image_path)
    payload = {'image': base64_image}

    try:
        # receives ocr results and outputs to json file
        response = requests.post('http://localhost:8000/ocr', json=payload)
        response.raise_for_status()
        result = response.json()

        # Create a unique filename for each output file
        output_file = os.path.splitext(os.path.basename(image_path))[0] + '_ocr_results.json'
        save_json_to_file(result, output_file)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing '{image_path}': {e}")


def main():
    while True:
        image_path = input("Enter image directory (or type 'exit' to quit): ")
        if image_path.lower() == 'exit':
            print("Exiting...")
            break

        process_image(image_path)


if __name__ == "__main__":
    main()
