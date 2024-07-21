from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from analysis import process_main
from common.custom_exceptions import LLMException

app = FastAPI()

@app.post("/congnitiv-analysis")
async def congnitiv_analysis(advertisement_image: UploadFile = File(...), advertisement_heatmap_image: UploadFile = File(...)):
    advert_image = advertisement_image.file.read()
    advert_heatmap = advertisement_heatmap_image.file.read()
    try:
        result = process_main.run(advert_image, advert_heatmap)
    except LLMException as e:
        return JSONResponse(content={"temporary error with llm: ": str(e)}, status_code=503)
    return JSONResponse(content=result, status_code=200)
