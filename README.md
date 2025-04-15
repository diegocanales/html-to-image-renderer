# HTML to Image Renderer

Convert HTML/CSS into PNG images via REST API. Template-driven image generator service built with FastAPI and Playwright. Ideal for dynamic content rendering, social cards, and automated image generation.

## Features

- Convert HTML/CSS to PNG images
- Template-based rendering with Jinja2
- Customizable image dimensions
- RESTful API interface
- Docker ready
- Content-agnostic rendering

## Description

The service exposes a REST API that accepts HTML and rendering parameters, returning a PNG image of the rendered content. It is content-agnostic and can be used to generate any type of HTML/CSS-based image.

## Quick Start

### Using Docker Compose

1. Clone the repository
2. Run the service:
```
docker-compose up
```

### Using Docker directly
```
docker run -p 8000:8000 -v $(pwd)/playwright:/app html-to-image-renderer
```

## API Reference

### Health Check
```
GET /health
Response: { "status": "ok" }
```

### Render Image
```
POST /render
Content-Type: application/json
```

Request body:
```json
{
    "html_content": string,    // HTML content to render
    "params": object,          // Template parameters
    "width": number,           // Image width (default: 1080)
    "height": number          // Image height (default: 1920)
}
```

## Usage Example

### Sample Request:

```json
POST /render
{
    "html_content": "
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin: 0; padding: 0; }
                #content-to-render {
                    background-color: {{background_color}};
                    padding: 20px;
                }
                h1 { color: {{text_color}}; }
            </style>
        </head>
        <body>
            <div id='content-to-render'>
                <h1>{{title}}</h1>
                <img src='{{image_url}}' />
            </div>
        </body>
        </html>
    ",
    "params": {
        "background_color": "#FF0000",
        "text_color": "#FFFFFF",
        "title": "My Title",
        "image_url": "https://example.com/image.jpg"
    },
    "width": 1080,
    "height": 1920
}
```

## Important Notes

1. The HTML must contain an element with id="content-to-render" that wraps all content to be rendered
2. Parameters in the HTML are defined using Jinja2 template syntax: {{parameter}}
3. The service will wait for the #content-to-render element to be visible before taking the screenshot
4. The resulting image is returned in PNG format

## Use Cases

- Generate social media cards
- Create dynamic certificates
- Produce automated reports
- Generate thumbnails
- Create dynamic badges
- Render email templates as images

## Requirements

- Docker
- Python 3.8+
- FastAPI
- Playwright
- Jinja2

## Docker Configuration

```yaml
version: '3.8'
services:
  image-renderer:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
```

## Development

To run the test script:
```bash
pip install requests
python test_endpoint.py
```

## License

MIT
