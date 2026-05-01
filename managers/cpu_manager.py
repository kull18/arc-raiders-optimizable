import psutil

class CPUManager:
    def __init__(self):
        self.GAME_NAME = "arc raiders"
        self.CPU_THRESHOLD = 80


    def search_process(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                name = proc.info["name"] or ""
                if self.GAME_NAME in name.lower():
                    return proc

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return None


    def optimize_process(self, process):

        try:
            process.nice(psutil.HIGH_PRIORITY_CLASS)

            core = list(range(psutil.cpu_count()))

            process.cpu_affinity(core)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Error optimizing process {process.pid}: {e}")

    def ajustar_dinamico(self, proceso):
        try:
            cpu = proceso.cpu_percent(interval=1)

            if cpu > self.CPU_THRESHOLD:
                # Reducir núcleos (ejemplo: usar 75%)
                total = psutil.cpu_count()
                nuevos = list(range(max(1, int(total * 0.75))))
                proceso.cpu_affinity(nuevos)

                print(f"Alto uso CPU ({cpu}%) → limitando núcleos: {nuevos}")

            else:
                # Restaurar todos los núcleos
                cores = list(range(psutil.cpu_count()))
                proceso.cpu_affinity(cores)

                print(f"[✔] CPU estable ({cpu}%) → usando todos los núcleos")

        except Exception as e:
            print(f"[ERROR dinámico] {e}")