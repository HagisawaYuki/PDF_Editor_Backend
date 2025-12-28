# from pdf2image import convert_from_path
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.utils import ImageReader


# def make_division_pdf(input_pdf: str, output_pdf: str, dpi=120):
#     images = convert_from_path(input_pdf, dpi=dpi)

#     page_width, page_height = A4
#     c = canvas.Canvas(output_pdf, pagesize=A4)

#     for i in range(0, len(images), 4):
#         imgs = images[i:i + 4]

#         positions = [
#             (0, page_height / 2),               # 左上
#             (page_width / 2, page_height / 2),  # 右上
#             (0, 0),                             # 左下
#             (page_width / 2, 0),                # 右下
#         ]

#         for img, (x, y) in zip(imgs, positions):
#             img = img.convert("RGB")
#             img_reader = ImageReader(img)

#             c.drawImage(
#                 img_reader,
#                 x,
#                 y,
#                 width=page_width / 2,
#                 height=page_height / 2,
#                 preserveAspectRatio=True
#             )

#         c.showPage()

#     c.save()

from pdf2image import convert_from_path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader


def make_division_pdf(input_pdf: str, output_pdf: str, dpi=120):
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)

    page_width, page_height = A4
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # 4ページずつ処理
    for i in range(0, total_pages, 4):
        positions = [
            (0, page_height / 2),               # 左上
            (page_width / 2, page_height / 2),  # 右上
            (0, 0),                             # 左下
            (page_width / 2, 0),                # 右下
        ]

        for j in range(4):
            page_num = i + j + 1
            if page_num > total_pages:
                break

            # ★ 1ページだけ画像化（超重要）
            images = convert_from_path(
                input_pdf,
                dpi=dpi,
                first_page=page_num,
                last_page=page_num
            )

            img = images[0].convert("RGB")
            img_reader = ImageReader(img)

            x, y = positions[j]
            c.drawImage(
                img_reader,
                x,
                y,
                width=page_width / 2,
                height=page_height / 2,
                preserveAspectRatio=True
            )

        c.showPage()

    c.save()

