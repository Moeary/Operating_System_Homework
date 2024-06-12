import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 定义PCB类
class PCB:
    def __init__(self, id, name, priority, work_time, arrive_time):
        self.id = id
        self.name = name
        self.priority = priority
        self.work_time = work_time
        self.arrive_time = arrive_time
        self.begin_time = 0
        self.finish_time = 0
        self.tat = 0
        self.wtat = 0

    def __str__(self):
        return f"PCB(id={self.id}, name='{self.name}', priority={self.priority}, " \
               f"work_time={self.work_time}, arrive_time={self.arrive_time}, " \
               f"begin_time={self.begin_time}, finish_time={self.finish_time}, " \
               f"tat={self.tat}, wtat={self.wtat})"
# 定义作业调度应用类
class ProcessSchedulingApp:
    # 初始化
    def __init__(self, master):
        self.master = master
        master.title("作业调度模拟")

        # 进程信息输入区域
        self.input_frame = tk.LabelFrame(master, text="进程信息", padx=10, pady=10)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.id_label = tk.Label(self.input_frame, text="序号:")
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(self.input_frame, width=5)
        self.id_entry.grid(row=0, column=1)

        self.name_label = tk.Label(self.input_frame, text="进程名:")
        self.name_label.grid(row=0, column=2)
        self.name_entry = tk.Entry(self.input_frame, width=10)
        self.name_entry.grid(row=0, column=3)

        self.priority_label = tk.Label(self.input_frame, text="优先级:")
        self.priority_label.grid(row=0, column=4)
        self.priority_entry = tk.Entry(self.input_frame, width=5)
        self.priority_entry.grid(row=0, column=5)

        self.work_time_label = tk.Label(self.input_frame, text="服务时间:")
        self.work_time_label.grid(row=0, column=6)
        self.work_time_entry = tk.Entry(self.input_frame, width=5)
        self.work_time_entry.grid(row=0, column=7)

        self.arrive_time_label = tk.Label(self.input_frame, text="到达时间:")
        self.arrive_time_label.grid(row=0, column=8)
        self.arrive_time_entry = tk.Entry(self.input_frame, width=5)
        self.arrive_time_entry.grid(row=0, column=9)

        self.add_button = tk.Button(self.input_frame, text="添加", command=self.add_process)
        self.add_button.grid(row=0, column=10, padx=10)

        # 进程列表区域
        self.process_list_frame = tk.LabelFrame(master, text="进程列表", padx=12, pady=12)
        self.process_list_frame.grid(row=1, column=0, padx=12, pady=12, sticky="nw")

        self.process_table = ttk.Treeview(self.process_list_frame, columns=(
        "id", "name", "priority", "work_time", "arrive_time", "begin_time", "finish_time", "tat", "wtat"),
                                          show="headings")
        self.process_table.column("id", width=50)
        self.process_table.heading("id", text="序号")
        self.process_table.column("name", width=50)
        self.process_table.heading("name", text="进程名")
        self.process_table.column("priority", width=50)
        self.process_table.heading("priority", text="优先级")
        self.process_table.column("work_time", width=50)
        self.process_table.heading("work_time", text="服务时间")
        self.process_table.column("arrive_time", width=50)
        self.process_table.heading("arrive_time", text="到达时间")
        self.process_table.column("begin_time", width=50)
        self.process_table.heading("begin_time", text="开始运行时间")
        self.process_table.column("finish_time", width=50)
        self.process_table.heading("finish_time", text="结束运行时间")
        self.process_table.column("tat", width=50)
        self.process_table.heading("tat", text="周转时间")
        self.process_table.column("wtat", width=50)
        self.process_table.heading("wtat", text="带权周转时间")
        self.process_table.pack()

        # 平均时间显示区域
        self.avg_time_frame = tk.LabelFrame(master, text="平均时间", padx=10, pady=10)
        self.avg_time_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        self.avg_tat_label = tk.Label(self.avg_time_frame, text="平均周转时间:")
        self.avg_tat_label.grid(row=0, column=0)
        self.avg_tat_value = tk.Label(self.avg_time_frame, text="")
        self.avg_tat_value.grid(row=0, column=1)

        self.avg_wtat_label = tk.Label(self.avg_time_frame, text="平均带权周转时间:")
        self.avg_wtat_label.grid(row=1, column=0)
        self.avg_wtat_value = tk.Label(self.avg_time_frame, text="")
        self.avg_wtat_value.grid(row=1, column=1)

        # 算法选择和执行区域
        self.algorithm_frame = tk.LabelFrame(master, text="算法选择", padx=10, pady=10)
        self.algorithm_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

        self.algorithm_label = tk.Label(self.algorithm_frame, text="请选择调度算法:")
        self.algorithm_label.grid(row=0, column=0)

        self.algorithm_var = tk.StringVar(self.algorithm_frame)
        self.algorithm_var.set("FCFS")  # 默认选择FCFS算法
        self.algorithm_options = ["FCFS", "SJF", "HRN"]
        self.algorithm_dropdown = tk.OptionMenu(self.algorithm_frame, self.algorithm_var, *self.algorithm_options)
        self.algorithm_dropdown.grid(row=0, column=1)

        self.execute_button = tk.Button(self.algorithm_frame, text="执行", command=self.execute_algorithm)
        self.execute_button.grid(row=0, column=2, padx=10)

        self.clear_button = tk.Button(self.algorithm_frame, text="清空", command=self.clear_table)
        self.clear_button.grid(row=0, column=3)

        # 图表显示区域
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=4, padx=10, pady=10)

        
        self.generate_button = tk.Button(self.input_frame, text="随机生成", command=self.generate_processes)
        self.generate_button.grid(row=1, column=0, columnspan=11, pady=(5, 0))
        
        # 初始化进程列表
        self.processes = []
    # 添加进程
    def add_process(self):
        try:
            id = int(self.id_entry.get())
            name = self.name_entry.get()
            priority = int(self.priority_entry.get())
            work_time = float(self.work_time_entry.get())
            arrive_time = float(self.arrive_time_entry.get())

            # 创建PCB对象并添加到进程列表
            pcb = PCB(id, name, priority, work_time, arrive_time)
            self.processes.append(pcb)

            # 更新进程列表显示
            self.process_table.insert("", tk.END, values=(
            pcb.id, pcb.name, pcb.priority, pcb.work_time, pcb.arrive_time, "", "", "", ""))

            # 清空输入框
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.work_time_entry.delete(0, tk.END)
            self.arrive_time_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值！")
    # 生成随机进程
    def generate_processes(self):
        try:
            # 获取要生成的进程数量
            n = int(tk.simpledialog.askstring("输入", "请输入要生成的进程数量："))

            # 生成n组随机进程信息
            for i in range(n):
                id = i + 1
                name = f"P{id}"
                priority = random.randint(1, 5)
                work_time = random.randint(1, 10)
                arrive_time = random.randint(0, 10)

                # 创建PCB对象并添加到进程列表
                pcb = PCB(id, name, priority, work_time, arrive_time)
                self.processes.append(pcb)

                # 更新进程列表显示
                self.process_table.insert("", tk.END, values=(
                    pcb.id, pcb.name, pcb.priority, pcb.work_time, pcb.arrive_time, "", "", "", ""))

        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值！")
    # 执行调度算法
    def execute_algorithm(self):
        # 获取选择的算法
        algorithm = self.algorithm_var.get()

        # 执行相应的调度算法
        if algorithm == "FCFS":
            self.execute_fcfs()
        elif algorithm == "SJF":
            self.execute_sjf()
        elif algorithm == "HRN":
            self.execute_hrn()

        # 更新进程列表和平均时间显示
        self.update_process_table()
        self.update_avg_time()

        # 绘制甘特图
        self.draw_gantt_chart()
    # 先来先服务算法 (FCFS)
    def execute_fcfs(self):
        # 按照到达时间排序
        self.processes.sort(key=lambda x: x.arrive_time)

        # 计算每个进程的开始时间、结束时间、周转时间和带权周转时间
        current_time = 0
        for pcb in self.processes:
            pcb.begin_time = max(current_time, pcb.arrive_time)
            pcb.finish_time = pcb.begin_time + pcb.work_time
            pcb.tat = pcb.finish_time - pcb.arrive_time
            pcb.wtat = pcb.tat / pcb.work_time
            current_time = pcb.finish_time
    # 最短作业优先算法 (SJF)
    def execute_sjf(self):
        # 按照到达时间排序
        self.processes.sort(key=lambda x: x.arrive_time)

        # 创建一个列表来存储已经完成的进程
        completed_processes = []

        # 初始化当前时间和就绪队列
        current_time = 0
        ready_queue = []

        # 循环执行，直到所有进程都完成
        while len(completed_processes) < len(self.processes):
            # 将到达时间小于等于当前时间的进程添加到就绪队列中
            for pcb in self.processes:
                if pcb.arrive_time <= current_time and pcb not in ready_queue and pcb not in completed_processes:
                    ready_queue.append(pcb)

            # 按照服务时间对就绪队列进行排序
            ready_queue.sort(key=lambda x: x.work_time)

            # 如果就绪队列不为空，则选择服务时间最短的进程执行
            if ready_queue:
                # 获取就绪队列中的第一个进程
                pcb = ready_queue.pop(0)

                # 计算进程的开始时间、结束时间、周转时间和带权周转时间
                pcb.begin_time = current_time
                pcb.finish_time = pcb.begin_time + pcb.work_time
                pcb.tat = pcb.finish_time - pcb.arrive_time
                pcb.wtat = pcb.tat / pcb.work_time

                # 更新当前时间
                current_time = pcb.finish_time

                # 将进程添加到已完成进程列表中
                completed_processes.append(pcb)
            else:
                # 如果就绪队列为空，则将当前时间更新为下一个进程的到达时间
                next_arrive_time = min([pcb.arrive_time for pcb in self.processes if pcb not in completed_processes])
                current_time = next_arrive_time
    # 最高优先级算法 (HRN)
    def execute_hrn(self):
        # 按照到达时间排序
        self.processes.sort(key=lambda x: x.arrive_time)

        # 创建一个列表来存储已经完成的进程
        completed_processes = []

        # 初始化当前时间和就绪队列
        current_time = 0
        ready_queue = []

        # 循环执行，直到所有进程都完成
        while len(completed_processes) < len(self.processes):
            # 将到达时间小于等于当前时间的进程添加到就绪队列中
            for pcb in self.processes:
                if pcb.arrive_time <= current_time and pcb not in ready_queue and pcb not in completed_processes:
                    ready_queue.append(pcb)

            # 按照响应比对就绪队列进行排序
            ready_queue.sort(key=lambda x: ((current_time - x.arrive_time) + x.work_time) / x.work_time, reverse=True)

            # 如果就绪队列不为空，则选择响应比最高的进程执行
            if ready_queue:
                # 获取就绪队列中的第一个进程
                pcb = ready_queue.pop(0)

                # 计算进程的开始时间、结束时间、周转时间和带权周转时间
                pcb.begin_time = current_time
                pcb.finish_time = pcb.begin_time + pcb.work_time
                pcb.tat = pcb.finish_time - pcb.arrive_time
                pcb.wtat = pcb.tat / pcb.work_time

                # 更新当前时间
                current_time = pcb.finish_time

                # 将进程添加到已完成进程列表中
                completed_processes.append(pcb)
            else:
                # 如果就绪队列为空，则将当前时间更新为下一个进程的到达时间
                next_arrive_time = min([pcb.arrive_time for pcb in self.processes if pcb not in completed_processes])
                current_time = next_arrive_time
    # 更新进程列表
    def update_process_table(self):
        # 清空表格
        for item in self.process_table.get_children():
            self.process_table.delete(item)

        # 插入更新后的进程信息
        for pcb in self.processes:
            self.process_table.insert("", tk.END, values=(
            pcb.id, pcb.name, pcb.priority, pcb.work_time, pcb.arrive_time, pcb.begin_time, pcb.finish_time, pcb.tat,
            pcb.wtat))
    # 更新平均时间显示
    def update_avg_time(self):
        # 计算平均周转时间和平均带权周转时间
        avg_tat = sum([pcb.tat for pcb in self.processes]) / len(self.processes)
        avg_wtat = sum([pcb.wtat for pcb in self.processes]) / len(self.processes)

        # 更新显示
        self.avg_tat_value.config(text=f"{avg_tat:.2f}")
        self.avg_wtat_value.config(text=f"{avg_wtat:.2f}")
    # 绘制甘特图
    def draw_gantt_chart(self):
        # 清空图表
        self.ax.clear()

        # 设置图表标题和轴标签
        self.ax.set_title("甘特图")
        self.ax.set_xlabel("时间")
        self.ax.set_ylabel("进程")

        # 绘制每个进程的条形图
        for i, pcb in enumerate(self.processes):
            self.ax.barh(i, pcb.work_time, left=pcb.begin_time, height=0.5, label=pcb.name)

        # 设置y轴刻度标签
        self.ax.set_yticks(range(len(self.processes)))
        self.ax.set_yticklabels([pcb.name for pcb in self.processes])

        # 显示图例
        self.ax.legend()

        # 调整布局
        self.figure.tight_layout()

        # 更新图表显示
        self.canvas.draw()
    # 清空表格
    def clear_table(self):
        # 清空进程列表和表格
        self.processes = []
        for item in self.process_table.get_children():
            self.process_table.delete(item)

        # 清空平均时间显示
        self.avg_tat_value.config(text="")
        self.avg_wtat_value.config(text="")

        # 清空图表
        self.ax.clear()
        self.canvas.draw()

# 主函数
if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessSchedulingApp(root)
    root.mainloop()

