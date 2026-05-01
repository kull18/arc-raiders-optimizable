import psutil
import config


class ProcessManager:

    def __init__(self):
        pass

    def list_processes(self):
        for proc in psutil.process_iter():
            try:
                print(f"PID: {proc.pid}, name: {proc.name()}")
                self.identify_useless_process(proc.name, proc.cpu_percent(interval=0.1), proc.memory_info().rss / (1024 * 1024))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def identify_useless_process(self, name, cpu, memory_usage):
        try:
            if name not in config.valuable_process and name not in config.system_process:
                if cpu > 5 and memory_usage > 5:
                    print(f"[UNKNOWN] process: {name} (memory: {memory_usage} MB, CPU: {cpu}%)")
                else:
                    print(f"[KNOWN] process: {name} (memory: {memory_usage} MB, CPU: {cpu}%)")
            else:
                return print(f"Process valued: {name} (memory: {memory_usage} MB, CPU: {cpu}%)")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    def kill_process(self, pid):
        try:
             proc = psutil.Process(pid)
             proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Error killing process {pid}: {e}")

    def change_priority(self, pid, priority):
        try:
            proc = psutil.Process(pid)
            proc.nice(priority)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Error changing priority of process {pid}: {e}")