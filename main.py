from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
import tempfile
# import os
import io
from pdf_division import make_division_pdf
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pypdf import PdfReader, PdfWriter
import pikepdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/pdf/division")
async def pdf_division(file: UploadFile = File(...)):
    # 一時保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        input_path = tmp.name

    output_path = input_path.replace(".pdf", "_division.pdf")

    # ここで後ほど4-up処理を呼ぶ
    make_division_pdf(input_path, output_path)

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename="division.pdf"
    )

class PageRequest(BaseModel):
    pages: list[int]

# @app.post("/pdf/delete")
# async def delete_pdf(
#     file: UploadFile = File(...),
#     pages: str = Form(...)
# ):
#     pages_list = json.loads(pages)

#     # 確認
#     print("filename:", file.filename)
#     print("pages:", pages_list)

#     pdf_bytes = await file.read()

#     # ここで PDF 処理（削除など）
#     return {"status": "ok"}

# @app.post("/pdf/delete")
# async def delete_pdf(
#     file: UploadFile = File(...),
#     pages: str = Form(...)
# ):
#     # JSON文字列 → list[int]
#     pages_list: list[int] = json.loads(pages)

#     # 1始まり → 0始まりに変換
#     delete_pages = {p - 1 for p in pages_list}

#     # PDF 読み込み
#     pdf_bytes = await file.read()
#     reader = PdfReader(io.BytesIO(pdf_bytes))
#     writer = PdfWriter()

#     # ページを追加（削除対象以外）
#     for i, page in enumerate(reader.pages):
#         if i not in delete_pages:
#             writer.add_page(page)

#     # メモリ上に書き出し
#     output_pdf = io.BytesIO()
#     writer.write(output_pdf)
#     output_pdf.seek(0)

#     # PDF をレスポンスとして返す
#     return StreamingResponse(
#         output_pdf,
#         media_type="application/pdf",
#         headers={
#             "Content-Disposition": f"attachment; filename=deleted_{file.filename}"
#         },
#     )

# @app.post("/pdf/delete")
# async def delete_pdf(
#     file: UploadFile = File(...),
#     pages: str = Form(...)
# ):
#     pages_list: list[int] = json.loads(pages)
#     delete_pages = {p - 1 for p in pages_list}

#     pdf_bytes = await file.read()

#     with pikepdf.open(io.BytesIO(pdf_bytes)) as pdf:
#         new_pdf = pikepdf.Pdf.new()

#         for i, page in enumerate(pdf.pages):
#             if i not in delete_pages:
#                 new_pdf.pages.append(page)

#         output_pdf = io.BytesIO()
#         new_pdf.save(
#             output_pdf,
#             optimize_streams=True,   # ★ 重要
#             compress_streams=True    # ★ 重要
#         )
#         output_pdf.seek(0)

#     return StreamingResponse(
#         output_pdf,
#         media_type="application/pdf",
#         headers={
#             "Content-Disposition": f"attachment; filename=deleted_{file.filename}"
#         },
#     )




@app.post("/pdf/delete")
async def delete_pdf(
    file: UploadFile = File(...),
    pages: str = Form(...)
):
    pages_list: list[int] = json.loads(pages)
    delete_pages = {p - 1 for p in pages_list}

    pdf_bytes = await file.read()

    with pikepdf.open(io.BytesIO(pdf_bytes)) as pdf:
        new_pdf = pikepdf.Pdf.new()

        for i, page in enumerate(pdf.pages):
            if i not in delete_pages:
                new_pdf.pages.append(page)

        output_pdf = io.BytesIO()
        new_pdf.save(output_pdf)  # ← ここ重要
        output_pdf.seek(0)

    return StreamingResponse(
        output_pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=deleted_{file.filename}"
        },
    )