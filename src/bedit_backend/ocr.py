from paddleocr import PaddleOCR

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# need to run only once to download and load model into memory
paddle_ocr = PaddleOCR(use_angle_cls=True)


def get_img_text(img_file: bytes):
    result = paddle_ocr.ocr(img_file, cls=True)

    for res in result:
        for line in res:
            yield line[1][0]
