import socket
import random
import time

HOST = "192.168.100.42"
PORT = 65432
buffer_size = 1024
game_active = True
start_time = 0
end_time = 0
minesCords = []

def main():
    global game_active
    try:
        with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as TCPServerSocket:
            TCPServerSocket.bind((HOST,PORT))
            TCPServerSocket.listen()
            print("El servidor esta listo")

            Client_conn , Client_addr = TCPServerSocket.accept()
            with Client_conn:
                print(f"{Client_addr}: Has connected to the server")
                while game_active:
                    print("Waiting for the difficulty")
                    difficulty = int(Client_conn.recv(buffer_size).decode('utf-8'))

                    print(f"Difficulty level Selected: {difficulty}")
                    minesCords = setRandomMines(difficulty)
                    grid_size = 9 if difficulty == 1 else 16
                    num_mines = 10 if difficulty == 1 else 20

                    print(f"mines generated on: {minesCords}")
                    cells_discovered = 0
                    Client_conn.sendall(b"Grid ready to begin.")
                    start_time = time.time()

                    while game_active:
                        coords = Client_conn.recv(buffer_size).decode('utf-8')
                        x,y = map(int, coords.split(","))
                        print(f"Coords sent: {x} , {y}")

                        if(x,y) in minesCords:
                            game_active = False
                            Client_conn.sendall(b"Found mine, you've lost.")
                            print("the player has lost")
                            break
                        
                        cells_discovered += 1

                        if cyheckWinningCase(cells_discovered , grid_size , num_mines):
                            game_active = False
                            Client_conn.sendall(b"You've finished the entire table, you won")
                            print("the player has won")
                            break
                        else:
                            Client_conn.sendall(b"Casilla Libre")
                    
                    end_time = time.time()
                    game_duration = end_time - start_time
                    print(f"The match has last for {game_duration:.2f} seconds".encode('utf-8'))

    except Exception as e:
        print(f"Error while creating the server: {e}")
        game_active = False

def cyheckWinningCase(cells_discovered ,grid_size , num_mines):
    return cells_discovered == grid_size * grid_size - num_mines


def setRandomMines(difficulty):
    global minesCords
    if difficulty == 1:
        grid_size = 9
        num_mines = 10
    elif difficulty == 2:
        grid_size = 16
        num_mines = 20
    else:
        return []
    
    all_coords = [(x,y) for x in range(grid_size) for y in range(grid_size)]
    mines = random.sample(all_coords , num_mines)
    return mines

if __name__ == "__main__":
    main()