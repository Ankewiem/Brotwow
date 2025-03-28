from PIL import Image, ImageDraw

def create_gradient(width, height, color1, color2):
    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)

    for i in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * (i / height))
        g = int(color1[1] + (color2[1] - color1[1]) * (i / height))
        b = int(color1[2] + (color2[2] - color1[2]) * (i / height))
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    return image

# Tạo gradient từ màu xanh dương sang hồng
gradient_image = create_gradient(800, 600, (83, 97, 134), (222, 187, 216))
gradient_image.show()
gradient_image.save("gradient_bg.png")  # Lưu ảnh nếu cần
