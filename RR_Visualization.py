import matplotlib.pyplot as plt
import random

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid  # 进程ID
        self.arrival_time = arrival_time  # 到达时间
        self.burst_time = burst_time  # 服务时间
        self.remaining_time = burst_time  # 剩余服务时间
        self.waiting_time = 0  # 等待时间
        self.turnaround_time = 0  # 周转时间

def round_robin(processes, time_quantum):
    ready_queue = []
    time = 0
    finished_processes = []

    print("时间片轮转调度算法演示:")

    while processes or ready_queue:
        # 将到达的进程添加到就绪队列
        for p in processes:
            if p.arrival_time <= time:
                ready_queue.append(p)
                processes.remove(p)

        if ready_queue:
            current_process = ready_queue.pop(0)
            print(f"时间: {time}  进程 {current_process.pid} 正在运行...")

            # 执行一个时间片
            execution_time = min(current_process.remaining_time, time_quantum)
            current_process.remaining_time -= execution_time
            time += execution_time

            if current_process.remaining_time == 0:
                # 进程完成
                current_process.turnaround_time = time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                finished_processes.append(current_process)
                print(f"时间: {time}  进程 {current_process.pid} 完成.")
            else:
                # 进程未完成，放回就绪队列末尾
                ready_queue.append(current_process)
        else:
            # CPU 空闲
            time += 1

    return finished_processes

# 生成随机进程
def generate_random_processes(num_processes):
    processes = []
    for i in range(num_processes):
        pid = f"P{i+1}"
        arrival_time = random.randint(0, num_processes * 2)  # 随机到达时间
        burst_time = random.randint(1, 10)  # 随机服务时间
        processes.append(Process(pid, arrival_time, burst_time))
    return processes

if __name__ == "__main__":
    num_processes = int(input("请输入进程数量: "))
    time_quantum = int(input("请输入时间片大小: "))

    processes = generate_random_processes(num_processes)

    # 按到达时间排序
    processes.sort(key=lambda x: x.arrival_time)

    finished_processes = round_robin(processes, time_quantum)

    # 计算平均等待时间和平均周转时间
    avg_waiting_time = sum([p.waiting_time for p in finished_processes]) / len(finished_processes)
    avg_turnaround_time = sum([p.turnaround_time for p in finished_processes]) / len(finished_processes)

    print("\n进程调度完成:")
    print(f"平均等待时间: {avg_waiting_time:.2f}")
    print(f"平均周转时间: {avg_turnaround_time:.2f}")

    # 可视化甘特图
    fig, ax = plt.subplots()
    for i, p in enumerate(finished_processes):
        ax.barh(i, p.burst_time, left=p.arrival_time + p.waiting_time, height=0.5, label=p.pid)

    ax.set_xlabel("时间")
    ax.set_ylabel("进程")
    ax.set_title("时间片轮转调度甘特图")
    plt.xticks(range(max([p.turnaround_time + p.arrival_time for p in finished_processes]) + 2))  # 设置 x 轴刻度
    plt.legend()

    # 设置支持中文的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.show()
