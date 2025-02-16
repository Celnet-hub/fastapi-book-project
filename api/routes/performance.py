from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from api.routes.books import call_webhook

router = APIRouter()

@router.get("/performance.json", status_code=status.HTTP_200_OK, name="performance")
async def performance(request: Request):
    base_url = str(request.base_url).rstrip("/")
    payload = {
        "date": {
                "created_at": "2025-02-16",
                "updated_at": "2025-02-16"
            },
        "descriptions": {
                "app_name": "Book Inventory APP Performance Monitor", 
                "app_description": "Checks the impact of each API of the Book Inventory APP on the server",
                "app_logo": "https://i.imgur.com/bRoRB1Y.png",
                "app_url": f"{base_url}",
                "background_color": "#fff"
            },
        "is_active": True,
        "integration_type": "output",
        "key_features": [
                "- Monitor the performance of the Book Inventory APP",
                "- Check the impact of each API on the server",
            ],
        "integration_category": "Monitoring & Logging",
        "author": "Chidubem Nwabuisi",
        "website": f"{base_url}",
        "settings": [
            {
                "label": "Book_Inventory_API_URL",
                "type": "text",
                "required": True,
                "default": f"{base_url}/api/v1/books",
            }
            ],
        "target_url": f"{base_url}/api/v1/target_url",
    }
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"data": payload}
    )

@router.post("/target_url", status_code=status.HTTP_200_OK, name="target_url")
async def target_url(request: Request):
    # get post request body
    # post_data = await request.json()
    request_url = str(request.url)
    await call_webhook("Target URL", f"{request_url} Post endpoint was called", "success")
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Success"}
    )