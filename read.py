import fitz

def extract_text_from_pdf(pdf_path):
    # 打开PDF文件
    document = fitz.open(pdf_path)
    text = ""
 
    # 遍历每一页
    for page_num in range(len(document)):
        page = document[page_num]
        # 获取文本块
        for block in page.get_text("blocks"):
            text += block[4].strip()  # 获取文本内容
 
    document.close()
    return text

print(extract_text_from_pdf('data/resumes/1/resume.pdf'))