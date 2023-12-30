import io

from fastapi import FastAPI, UploadFile

from lib import solve_with_google_lens

app = FastAPI()


@app.post("/solve")
async def solve_captcha(file: UploadFile):
    result = None
    try:
        file_content = await file.read()
        result = solve_with_google_lens((file.filename, io.BytesIO(file_content), file.content_type))
    except Exception as error:
        print(error)
    return {"result": result}
