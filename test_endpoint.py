import requests

from pathlib import Path

def test_image_renderer():
    # API endpoint
    url = "http://localhost:8000/render"

    # HTML template with a simple design
    html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin: 0; padding: 0; }
                #content-to-render {
                    background-color: {{background_color}};
                    width: 100%;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                    box-sizing: border-box;
                }
                h1 {
                    color: {{text_color}};
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                .test-image {
                    max-width: 80%;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div id="content-to-render">
                <h1>{{title}}</h1>
                <img class="test-image" src="{{image_url}}" />
            </div>
        </body>
        </html>
    """

    # Request payload
    payload = {
        "html_content": html_content,
        "params": {
            "background_color": "#1a1a1a",
            "text_color": "#ffffff",
            "title": "Test Image Generation",
            "image_url": "https://picsum.photos/800/600"  # Random image from Lorem Picsum
        },
        "width": 1080,
        "height": 1920
    }

    try:
        # Make the request
        print("Sending request to image renderer...")
        response = requests.post(url, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            # Save the image
            output_path = Path("test_output.png")
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Image successfully generated and saved to: {output_path.absolute()}")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_image_renderer()
