from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from playwright.async_api import async_playwright
from pydantic import BaseModel
from jinja2 import Environment, BaseLoader


app = FastAPI()

class RenderRequest(BaseModel):
    html_content: str
    params: dict
    width: int = 1080
    height: int = 1920

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/render")
async def render_image(render_data: RenderRequest):
    try:
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
