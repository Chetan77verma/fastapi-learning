import httpx
from fastapi import APIRouter
client = httpx.AsyncClient(verify=False)

router = APIRouter(tags=['Search'])

@router.get("/search")
async def search_elastic():
    headers = {
        "Authorization": "Basic ZWxhc3RpYzpTVVNIMTIzNC4=",
        "kbn-xsrf": "reporting"
    }
    response = await client.get('https://localhost:9200/news_headlines/_count',headers=headers)
    print(response)
    print(response.json())  
    return {"data":"success"}   
