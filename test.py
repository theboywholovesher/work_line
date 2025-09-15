import qrcode
from PIL import Image, ImageDraw


def create_multi_qr_image(data_list, output_path, cols=3, size=200, spacing=20):
    """
    创建包含多个二维码的图片

    参数:
        data_list: 二维码内容列表
        output_path: 输出图片路径
        cols: 每行显示的二维码数量
        size: 每个二维码的大小（像素）
        spacing: 二维码之间的间距
    """
    # 计算画布大小
    rows = (len(data_list) + cols - 1) // cols
    img_width = cols * (size + spacing) - spacing
    img_height = rows * (size + spacing) - spacing

    # 创建空白画布
    canvas = Image.new('RGB', (img_width, img_height), 'white')

    # 生成并放置二维码
    for i, data in enumerate(data_list):
        # 创建二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr_img = qr.make_image(fill_color="black", back_color="white").resize((size, size))

        # 计算位置
        row = i // cols
        col = i % cols
        x = col * (size + spacing)
        y = row * (size + spacing)

        # 将二维码粘贴到画布上
        canvas.paste(qr_img, (x, y))

    # 保存图片
    canvas.save(output_path)
    print(f"已生成包含 {len(data_list)} 个二维码的图片: {output_path}")


# 使用示例
if __name__ == "__main__":
    # 二维码内容列表
    qr_data = [
        "https://www.example.com/product1",
        "https://www.example.com/product2",
        "https://www.example.com/product3",
        "PRODUCT-2023-001",
        "PRODUCT-2023-002",
        "PRODUCT-2023-003",
        "扫码获取更多信息",
        "技术支持: 400-123-4567",
        "微信公众号: ExampleTech"
    ]

    # 生成图片
    create_multi_qr_image(qr_data, "pic_s/multi_qr_codes.png", cols=3, size=300, spacing=30)