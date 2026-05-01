from managers.process_manager import ProcessManager
from managers.cpu_manager import CPUManager
import time

if __name__ == "__main__":
    process_manager = ProcessManager()
    process_manager.list_processes()
    process = None 

    while process is None:
        if not process or not process.is_running():
            process = CPUManager().search_process()
            if process:
                print(f"Proceso encontrado: {process.name()} (PID: {process.pid})")
                CPUManager().optimize_process(process)
            else:
                print("Esperando a que el proceso del juego se inicie...")

    CPUManager().ajustar_dinamico(process)
    time.sleep(5)