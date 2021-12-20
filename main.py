import socket
from util import *
import urllib.request

def main(sock: socket.socket):
    def __server(sock: socket.socket):
        # Creating server, binding to port 50240
        sock.bind(('', 50240))
        sock.listen(5)
        print(f'\n\t* Your current external IP-adress is {urllib.request.urlopen("https://ident.me").read().decode("utf8")}')
        print('\t* Tell your friends to connect to this IP-adress;')
        print('\t* Make sure the 50240 port is open')
        player_count = input('\nEnter the number of players (2-11, don\'t forget yourself): ')
        while player_count not in [str(a) for a in range(2,12)]:
            print('ERROR: incorrect number, try again')
            player_count = input('Enter the number of players (2-11, don\'t forget yourself): ')
        player_count = int(player_count)
        client_connections = {}
        i = 0
        print(f'\nAwaiting for {player_count} connections...')
        while i < player_count:
            conn, addr = sock.accept()
            p_name = s_connect.input(conn, 'Enter Your name: ').capitalize()
            while p_name in client_connections.keys():
                print(f'\tERROR: connection attempt from address with already stored name: {p_name}')
                conn.send(('Connection unsuccessfull: player with this name has already joined\nChange your name and try to reconnect').encode())
                p_name = s_connect.input(conn, 'Enter Your name: ').capitalize()

            print(f'> Recieved connection:\n\tAddress {addr[0]}, player {p_name}')
            conn.send((f'\nConnection successfull\nWelcome, {p_name}!\nWaiting for others to join...').encode())
            client_connections[p_name] = {'Connection': conn, 'Address' : addr}
            i += 1

        names = shuffle_lst([*client_connections])
        game = PokerTable()
        for name in names:
            game.players.append(PokerPlayer(name, connect = client_connections[name], place=names.index(name)))
        for p in client_connections:
            client_connections[p]['Connection'].send('print'.encode())
            client_connections[p]['Connection'].recv(1024)
            client_connections[p]['Connection'].send('All the players connected, waiting for host to start...'.encode())
        __finished = False
        while not __finished:
            game_type = input('Choose the game version: [T]exas Hold\'em or [O]maha\n > ').upper()
            while game_type not in ['T','O']:
                print(f'{game_type} is not an option')
                game_type = input('Choose the game version: [T]exas Hold\'em or [O]maha\n > ').upper()

            print('You\'ve chosen {}'.format(["Texas Hold\'em", "Omaha"]["TO".index(game_type)]))
            game.viewers = game.players
            if input('Start new game (Y/...)? ').upper() == 'Y':
                game.game_of_poker(game_type=game_type)
            else:
                for index in client_connections:
                    conn = client_connections[index]['Connection']
                    s_connect.send_custom(conn, 'close', 'Game finished, thanks for playing!')
                __finished = True
        print('Game finished, thanks for playing!')

    def __client(sock: socket.socket):
        server_ip = input('\nEnter host IP-adress to connect to the game: ')
        while True:
            try:
                sock.connect((server_ip, 50240))
                s_connect.receive(sock)
                data = sock.recv(1024).decode()
                while data.startswith('Connection unsuccessfull'):
                    print(data)
                    s_connect.receive(sock)
                    data = sock.recv(1024).decode()
                print(data)
                trigger = False
                while not trigger:
                    trigger = s_connect.receive(sock)
            except ConnectionRefusedError as err:
                print('\n'+str(err))
                if input('Try to reconnect (Y/...)? ').upper() not in 'Y':
                    print('Reconnection attempt denied\n')
                    break

    current_type = input('Choose your type: [S]erver or [C]lient (any other choice closes the window): ').upper()
    if current_type == 'S':
        __server(sock)
    elif current_type == 'C':
        __client(sock)
    else:
        quit()

if __name__ == '__main__':
    sock = socket.socket()
    main(sock)
