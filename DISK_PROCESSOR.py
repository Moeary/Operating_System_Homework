import tkinter as tk
from tkinter import ttk
import random

# 定义磁盘请求队列
disk_requests = [53, 98, 183, 37, 122, 14, 124, 65, 67]
# 磁头初始位置
initial_head_position = 53

# 计算柱面的数量
cylinder_count = 200


class DiskSchedulingApp:
    def __init__(self, master):
        self.master = master
        master.title("磁盘调度可视化")

        self.start_label = tk.Label(
            master, text="请输入磁头的初始位置（0-200之间）："
        )
        self.start_label.grid(row=0, column=0)

        self.start_entry = tk.Entry(master)
        self.start_entry.insert(0, str(initial_head_position))
        self.start_entry.grid(row=0, column=1)

        self.generate_button = tk.Button(
            master, text="生成随机磁道序列", command=self.generate_sequence
        )
        self.generate_button.grid(row=1, column=0, columnspan=2)

        self.sequence_label = tk.Label(master, text="磁道序列：")
        self.sequence_label.grid(row=2, column=0)

        self.sequence_var = tk.StringVar(master)
        self.sequence_var.set(str(disk_requests))
        self.sequence_display = tk.Label(
            master, textvariable=self.sequence_var
        )
        self.sequence_display.grid(row=2, column=1)

        self.algorithm_label = tk.Label(master, text="选择算法：")
        self.algorithm_label.grid(row=3, column=0)

        self.algorithm_var = tk.StringVar(master)
        self.algorithm_var.set("FCFS")  # 默认选择FCFS算法

        self.algorithm_options = ["FCFS", "SSTF", "SCAN", "CSCAN"]
        self.algorithm_dropdown = ttk.Combobox(
            master, textvariable=self.algorithm_var, values=self.algorithm_options
        )
        self.algorithm_dropdown.grid(row=3, column=1)

        self.run_button = tk.Button(
            master, text="运行", command=self.run_algorithm
        )
        self.run_button.grid(row=4, column=0, columnspan=2)

        self.canvas = tk.Canvas(
            master, width=800, height=400, bg="white"
        )
        self.canvas.grid(row=5, column=0, columnspan=2)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=6, column=0, columnspan=2)

        self.sequence = disk_requests.copy()
        self.start = initial_head_position

    def generate_sequence(self):
        self.sequence = random.sample(range(1, 200), 10)
        self.sequence_var.set(str(self.sequence))

    def run_algorithm(self):
        try:
            self.start = int(self.start_entry.get())
            if self.start < 0 or self.start > 200:
                raise ValueError
        except ValueError:
            self.result_label.config(text="请输入有效的初始位置！")
            return

        algorithm = self.algorithm_var.get()
        if algorithm == "FCFS":
            sequence, total_distance = self.fcfs(
                self.sequence.copy(), self.start
            )
        elif algorithm == "SSTF":
            sequence, total_distance = self.sstf(
                self.sequence.copy(), self.start
            )
        elif algorithm == "SCAN":
            sequence, total_distance = self.scan(
                self.sequence.copy(), self.start
            )
        elif algorithm == "CSCAN":
            sequence, total_distance = self.cscan(
                self.sequence.copy(), self.start
            )
        else:
            self.result_label.config(text="请选择有效的算法！")
            return

        self.draw_graph(sequence, total_distance)

    def fcfs(self, requests, head):
        """
        先来先服务算法 (FCFS)
        """
        seek_sequence = [head] + requests
        total_head_movement = sum(
            abs(seek_sequence[i] - seek_sequence[i + 1])
            for i in range(len(seek_sequence) - 1)
        )
        return seek_sequence, total_head_movement

    def sstf(self, requests, head):
        """
        最短寻道时间优先算法 (SSTF)
        """
        seek_sequence = [head]
        total_head_movement = 0
        remaining_requests = set(requests)

        while remaining_requests:
            current_head = seek_sequence[-1]
            next_request = min(
                remaining_requests, key=lambda req: abs(req - current_head)
            )
            seek_sequence.append(next_request)
            total_head_movement += abs(next_request - current_head)
            remaining_requests.remove(next_request)

        return seek_sequence, total_head_movement

    def scan(self, requests, head, direction="right"):
        """
        电梯调度算法 (SCAN)
        """
        seek_sequence = [head]
        total_head_movement = 0
        remaining_requests = sorted(requests)

        if direction == "right":
            # 向右移动
            for req in remaining_requests:
                if req > head:
                    seek_sequence.append(req)
                    total_head_movement += abs(req - seek_sequence[-2])
            seek_sequence.append(cylinder_count - 1)
            total_head_movement += abs(
                cylinder_count - 1 - seek_sequence[-2]
            )
            # 向左移动
            for req in reversed(remaining_requests):
                if req < seek_sequence[-1]:
                    seek_sequence.append(req)
                    total_head_movement += abs(req - seek_sequence[-2])
        else:  # direction == "left"
            # 向左移动
            for req in reversed(remaining_requests):
                if req < head:
                    seek_sequence.append(req)
                    total_head_movement += abs(req - seek_sequence[-2])
            seek_sequence.append(0)
            total_head_movement += abs(seek_sequence[-2])
            # 向右移动
            for req in remaining_requests:
                if req > seek_sequence[-1]:
                    seek_sequence.append(req)
                    total_head_movement += abs(req - seek_sequence[-2])

        return seek_sequence, total_head_movement

    def cscan(self, requests, head):
        """
        循环扫描算法 (C-SCAN)
        """
        seek_sequence = [head]
        total_head_movement = 0
        remaining_requests = sorted(requests)

        # 向右移动到最右边
        for req in remaining_requests:
            if req >= head:
                seek_sequence.append(req)
                total_head_movement += abs(req - seek_sequence[-2])

        # 从最左边开始继续向右移动
        seek_sequence.append(cylinder_count - 1)
        total_head_movement += abs(cylinder_count - 1 - seek_sequence[-2])
        seek_sequence.append(0)
        total_head_movement += abs(seek_sequence[-2])

        for req in remaining_requests:
            if req < head:
                seek_sequence.append(req)
                total_head_movement += abs(req - seek_sequence[-2])

        return seek_sequence, total_head_movement

    def draw_graph(self, sequence, total_distance):
        self.canvas.delete("all")

        # 绘制坐标轴
        self.canvas.create_line(50, 350, 750, 350, width=2)  # x轴
        self.canvas.create_line(50, 350, 50, 50, width=2)  # y轴

        # 绘制刻度
        for i in range(0, 201, 20):
            x = 50 + i * 4
            self.canvas.create_line(x, 350, x, 345, width=1)
            self.canvas.create_text(x, 360, text=str(i), anchor="n")

        # 绘制磁道序列
        x = 50 + self.start * 4
        y = 350
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
        for i in range(len(sequence)):
            x = 50 + sequence[i] * 4
            y = 330 - i * 20
            self.canvas.create_line(
                x, y, x, y + 20, width=2, fill="blue"
            )
            self.canvas.create_text(
                x, y - 10, text=str(sequence[i]), anchor="s"
            )

        # 显示结果
        avg_seek_length = total_distance / len(self.sequence)
        result_text = (
            f"磁道访问顺序: {sequence}\n"
            f"总共移动磁道数：{total_distance}\n"
            f"平均寻道长度: {avg_seek_length:.2f}"
        )
        self.result_label.config(text=result_text)


root = tk.Tk()
app = DiskSchedulingApp(root)
root.mainloop()
