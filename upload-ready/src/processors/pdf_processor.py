import fitz
from PIL import Image
import io

class PDFProcessor:
    def __init__(self, dpi=150):
        self.dpi = dpi
    
    def extract_pages(self, pdf_path):
        doc = fitz.open(pdf_path)
        pages = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            zoom = self.dpi / 72
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix)
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
            pages.append({"image": img, "page_num": page_num})
        doc.close()
        return pages
