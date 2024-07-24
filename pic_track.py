import tkinter as tk
from PIL import Image, ImageDraw

class DrawApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg='white', width=500, height=500)
        self.canvas.pack()

        self.drawing = False
        self.current_line = None
        self.current_line_points = []  # 用于存储当前线条的坐标点列表
        self.all_lines = []  # 用于存储所有线条的坐标点列表

        # 绑定鼠标事件
        self.canvas.bind('<Button-1>', self.start_paint)
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.stop_paint)

    def start_paint(self, event):
        self.drawing = True
        # 开始新线条时，重置当前线条的坐标点列表
        self.current_line = self.canvas.create_line(event.x, event.y, event.x, event.y, width=2)
        self.current_line_points = [(event.x, event.y)]

    def paint(self, event):
        if self.drawing:
            # 更新当前线条的坐标点列表
            self.current_line_points.append((event.x, event.y))
            self.canvas.coords(self.current_line, *self.current_line_points)
            # self.update_canvas()

    def update_canvas(self):
        # 如果当前有线条在画布上，先删除
        if self.current_line:
            self.canvas.delete(self.current_line)
        # 更新画布上的线条
        self.current_line = self.canvas.create_line(self.current_line_points, width=2)

    def stop_paint(self, event):
        if self.drawing:
            self.drawing = False
            # 将当前线条的坐标点列表添加到所有线条的列表
            self.all_lines.append(self.current_line_points)
            # 打印当前线条的所有坐标点
            print(f"原始线条上的所有坐标点（500x500画布）：")
            for point in self.current_line_points:
                print(point)
            print(f"图像已保存为 'line{len(self.all_lines)}.jpg'")

            # 保存所有线条为JPG图像
            self.save_all_lines_as_jpg()

    def save_all_lines_as_jpg(self):
        # 创建一个新的Pillow图像和绘图对象
        img = Image.new('RGB', (2000, 2000), 'white')
        draw = ImageDraw.Draw(img)

        # 计算缩放比例
        scale_x = 2000 / 500
        scale_y = 2000 / 500

        # 绘制所有线条
        for line_points in self.all_lines:
            # 存储放大后的坐标点
            scaled_points = [(int(x * scale_x), int(y * scale_y)) for x, y in line_points]
            # 在Pillow图像上绘制放大后的线条
            draw.line(scaled_points, fill='black', width=2)

        # 保存图像为JPG文件
        filename = f'line{len(self.all_lines)}.jpg'
        img.save(filename, format='JPEG')

# 创建主窗口
root = tk.Tk()
root.title("画线应用")

# 创建应用实例
app = DrawApp(root)

# 启动GUI主循环
root.mainloop()