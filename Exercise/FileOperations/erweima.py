import qrcode
from qrcode.image.svg import SvgPathImage
from PIL import Image
import io
import base64


def generate_svg_qr_with_logo(url, logo_path, output_file, qr_color="#000000", bg_color="#FFFFFF"):
    """
    完全修正版 - 确保Logo和颜色生效
    """
    # 1. 创建QRCode对象
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 2. 生成基础SVG（强制颜色生效的关键）
    factory = SvgPathImage
    img = qr.make_image(image_factory=factory)

    # 3. 手动添加颜色（覆盖默认值）
    svg_bytes = io.BytesIO()
    img.save(svg_bytes)
    svg_str = svg_bytes.getvalue().decode('utf-8')

    # 强制替换填充色和背景色
    svg_str = svg_str.replace('fill="black"', f'fill="{qr_color}"')
    svg_str = svg_str.replace('fill="white"', f'fill="{bg_color}"')

    # 4. 嵌入Logo（确保可见性）
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = min(qr.modules_count * 10 // 4, 150)  # 动态计算大小

        # 调整Logo尺寸
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

        # 转换为base64（修正编码方式）
        logo_bytes = io.BytesIO()
        logo.save(logo_bytes, format='PNG')
        logo_b64 = base64.b64encode(logo_bytes.getvalue()).decode('utf-8')

        # 计算居中位置
        center_pos = qr.modules_count * 10 // 2

        # 插入Logo（使用现代SVG语法）
        logo_tag = f'''
        <g transform="translate({center_pos},{center_pos})">
            <image href="data:image/png;base64,{logo_b64}"
                   width="{logo_size}" height="{logo_size}"
                   transform="translate(-{logo_size // 2},-{logo_size // 2})"/>
        </g>
        '''
        svg_str = svg_str.replace('</svg>', f'{logo_tag}</svg>')

    # 5. 保存文件（确保UTF-8编码）
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(svg_str)

if __name__ =="__main__":
    # 使用示例
    generate_svg_qr_with_logo(
        url="https://lirongyaoper.com",
        logo_path="/home/lirongyao0916/Downloads/ryxkj.png",  # 替换为你的Logo路径
        output_file="/home/lirongyao0916/Downloads/lirongyaoper_qr.svg",
        qr_color="#060270",  # 自定义二维码颜色
        bg_color="#FFFFFF"  # 透明背景
    )



alias githp='cd /home/lirongyao0916/Projects/Python01/ &&  git add . && git commit -m "update data at $(date +%Y%m%d%H%M%S)" && git push'
alias gitlp='cd /home/lirongyao0916/Projects/Python01/ &&  git pull'
alias gitcp='cd /home/lirongyao0916/Projects && rm -rf ./Python01 &&  git clone git@github.com:lirongyaoper/Python01.git'


alias githl='cd /home/lirongyao0916/Projects/Linux/ &&  git add . && git commit -m "update data at $(date +%Y%m%d%H%M%S)" && git push'
alias gitll='cd /home/lirongyao0916/Projects/Linux/ &&  git pull'
alias gitcl='cd /home/lirongyao0916/Projects && rm -rf ./Linux &&  git clone git@github.com:lirongyaoper/Linux.git'

alias githc='cd /home/lirongyao0916/Projects/CProjects/ &&  git add . && git commit -m "update data at $(date +%Y%m%d%H%M%S)" && git push'
alias gitlc='cd /home/lirongyao0916/Projects/CProjects/ &&  git pull'
alias gitcc='cd /home/lirongyao0916/Projects && rm -rf ./CProjects &&  git clone git@github.com:lirongyaoper/CProjects.git'

