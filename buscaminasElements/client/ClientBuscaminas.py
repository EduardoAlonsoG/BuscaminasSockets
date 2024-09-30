import socket
from buscaminasElements.client.ConnectElements import ConnectElements

HOST = "192.168.100.42"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024

def print_board(grid_size):
    print("    A B C D E F G H I J K L M N O P Q"[0:grid_size * 2])
    for i in range(grid_size):
        print(f"{i + 1}  " + " ".join(["-"] * grid_size))

def update_cell_board(board, x, y, value):
    board[x][y] = value

def askForCoords():
    print("select the coords of the cell you want to discover")
    x = int(input("x -> ")) - 1
    y = ord(input("y -> ").upper()) - ord('A')
    return x , y

def askDifficulty():
    print("Select the difficulty level: ")
    print("1 ->  Noob   (9x9)  grid | 10 minas")
    print("2 -> Expert (16x16) grid | 40 minas")
    return input("select Difficulty")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        TCPClientSocket.connect((HOST, PORT))

        difficulty = askDifficulty()
        TCPClientSocket.sendall(difficulty.encode('utf-8'))

        confirmation = TCPClientSocket.recv(buffer_size).decode('utf-8')
        print(confirmation)

        grid_size = 9 if difficulty == '1' else 16
        board = [["-"] * grid_size for _ in range(grid_size)]
        print_board(grid_size)

        game_active = True
        while game_active:
            x,y = askForCoords()
            coords = f"{x},{y}"

            TCPClientSocket.sendall(coords.encode('utf-8'))

            response = TCPClientSocket.recv(buffer_size).decode('utf-8')
            print(response)
            if "Found mine" in response:
                # Mostrar todas las minas
                print("Has perdido. Aquí están las minas.")
                game_active = False
            elif "you won" in response:
                print("¡Felicidades! Has ganado la partida.")
                game_active = False
            else:
                # Actualizar el tablero
                update_cell_board(board, x, y, "O")
                print_board(grid_size)
        duration = TCPClientSocket.recv(buffer_size).decode('utf-8')
        print(duration)

if __name__ == "__main__":
    main()