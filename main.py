import threading
import time

# Inicializando o mapa
mapa = [[0 for i in range(10)] for j in range(10)]
x = 3
y = 3
mapa[x][y] = 1

# Função para imprimir o mapa
def print_map():
    text = ""
    for i in mapa:
        for j in i:
            text += f"{j} "
        text += "\n"
    return text

# Função para mover o número 1 no mapa
def move(direction):
    global x, y
    mapa[x][y] = 0
    if direction == "w" and x > 0:
        x -= 1
    elif direction == "s" and x < 9:
        x += 1
    elif direction == "a" and y > 0:
        y -= 1
    elif direction == "d" and y < 9:
        y += 1
    mapa[x][y] = 1

# Classe do servidor
class Server(threading.Thread):
    def __init__(self):
        super().__init__()
        self.command = None
        self.lock = threading.Lock()

    def run(self):
        while True:
            if self.command:
                with self.lock:
                    move(self.command)
                    self.command = None
            time.sleep(0.1)

    def set_command(self, command):
        with self.lock:
            self.command = command

# Classe do cliente
class Client(threading.Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        while True:
            command = input("Digite o comando de movimento (w, a, s, d): ").strip().lower()
            if command in ["w", "a", "s", "d"]:
                self.server.set_command(command)
                time.sleep(0.2)  # Espera o servidor processar o comando
                print(print_map())

# Inicializando e iniciando as threads
server = Server()
client = Client(server)

server.start()
client.start()

server.join()
client.join()
