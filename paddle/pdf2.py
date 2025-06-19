from pathlib import Path
from paddleocr import PPStructureV3
from pdf2image import convert_from_path
import tempfile
import os

# 配置输入输出
input_pdf = "/home/lirongyao0916/Downloads/tel1.pdf"  # 替换为你的PDF文件路径
output_dir = Path("/home/lirongyao0916/Downloads/tel1")  # 输出目录

# 确保输出目录存在
output_dir.mkdir(parents=True, exist_ok=True)

# 初始化文档分析模型
pipeline = PPStructureV3()

# 存储所有页面的Markdown信息和图片
all_markdown_info = []
all_markdown_images = []

# 创建临时目录用于存储转换后的图片
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # 将PDF转换为图片列表
    print(f"正在将PDF转换为图片: {input_pdf}")
    images = convert_from_path(input_pdf, dpi=300)

    # 处理每一页
    for page_num, image in enumerate(images, start=1):
        # 保存临时图片文件
        temp_img_path = temp_path / f"page_{page_num}.png"
        image.save(temp_img_path, "PNG")

        print(f"正在处理第 {page_num}/{len(images)} 页...")

        # 分析当前页面
        try:
            page_result = pipeline.predict(str(temp_img_path))

            # 收集当前页面的Markdown信息
            for res in page_result:
                md_info = res.markdown
                all_markdown_info.append(md_info)
                all_markdown_images.append(md_info.get("markdown_images", {}))

        except Exception as e:
            print(f"处理第 {page_num} 页时出错: {str(e)}")
            # 创建空条目以保持页面顺序
            all_markdown_info.append({"markdown": f"# Page {page_num} (处理失败)\n\n"})
            all_markdown_images.append({})

# 合并所有页面的Markdown内容
print("正在合并Markdown内容...")
combined_markdown = pipeline.concatenate_markdown_pages(all_markdown_info)

# 保存Markdown文件
output_md = output_dir / f"{Path(input_pdf).stem}.md"
print(f"保存Markdown文件: {output_md}")
with open(output_md, "w", encoding="utf-8") as md_file:
    md_file.write(combined_markdown)

# 保存文档中的图片
image_count = 0
for page_images in all_markdown_images:
    if page_images:
        for rel_path, img in page_images.items():
            # 创建绝对路径
            img_path = output_dir / rel_path

            # 确保目录存在
            img_path.parent.mkdir(parents=True, exist_ok=True)

            # 保存图片
            img.save(img_path)
            image_count += 1

print(f"处理完成! 共处理 {len(images)} 页, 提取 {image_count} 张图片")
print(f"Markdown文件已保存至: {output_md}")