from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from playwright.async_api import async_playwright
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader, BaseLoader
import os

app = FastAPI()

# Definir el modelo de datos esperado
class RenderRequest(BaseModel):
    html_content: str  # El HTML completo a renderizar
    params: dict  # Parámetros para renderizar el template
    width: int = 1080  # valor por defecto
    height: int = 1920  # valor por defecto

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/render")
async def render_image(render_data: RenderRequest):
    try:
        # Renderizar el HTML con los parámetros proporcionados
        template = Environment(loader=BaseLoader()).from_string(render_data.html_content)
        rendered_html = template.render(**render_data.params)

        async with async_playwright() as p:
            browser = await p.chromium.launch(args=['--no-sandbox'])
            page = await browser.new_page(viewport={'width': render_data.width, 'height': render_data.height})
            
            await page.set_content(rendered_html, wait_until='networkidle')
            await page.wait_for_selector('#content-to-render', state='visible', timeout=5000)
            await page.screenshot(path='output.png')
            await browser.close()
        
        return FileResponse("output.png", media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
