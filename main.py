import socket
from util import *
import urllib.request
import os

def main(sock: socket.socket):
    def __server(sock: socket.socket):

        # Creating server, binding to port 50240
        sock.bind(('', 50240))
        print(f'\n\t* Your current external IP-adress is {urllib.request.urlopen("https://ident.me").read().decode("utf8")}')
        print('\t* Tell your friends to connect to this IP-adress;')
        print('\t* Make sure the 50240 port is open')
        player_count = input('\nEnter the number of players (2-11, don\'t forget yourself): ')
        while player_count not in [str(a) for a in range(2,12)]:
            print('ERROR: incorrect number, try again')
            player_count = input('Enter the number of players (2-11, don\'t forget yourself): ')
        player_count = int(player_count)
        sock.listen(player_count)
        client_connections = {}
        i = 0
        print(f'\nAwaiting for {player_count} connections...')

        # Accepting players
        while i < player_count:
            conn, addr = sock.accept()
            p_name = sync_conn.input(conn, 'Enter Your name: ').capitalize()
            while p_name in client_connections.keys():
                print(f'\tERROR: connection attempt from address with already stored name: {p_name}')
                conn.send(('Connection unsuccessfull: player with this name has already joined\nChange your name and try to reconnect').encode())
                p_name = sync_conn.input(conn, 'Enter Your name: ').capitalize()

            print(f'> Recieved connection:\n\tAddress {addr[0]}, player {p_name}')
            conn.send((f'\nConnection successfull\nWelcome, {p_name}!\nWaiting for others to join...').encode())
            client_connections[p_name] = {'Connection': conn, 'Address' : addr}
            i += 1

        names = shuffle_lst([*client_connections.keys()])
        game = PokerTable()
        for name in names:
            game.players.append(PokerPlayer(name, connect = client_connections[name], place=names.index(name)))
        sync_conn.print(game.players, 'All the players connected, waiting for host to start...')

        # Game
        while True:
            game_type = input('Choose an option: \n[T]exas Hold\'em\n[O]maha\n\n[Q]uit\n\n> ').upper()
            while game_type not in ['T', 'O', 'Q']:
                print(f'{game_type} is not an option;')
                game_type = input('choose the game version: \n[T]exas Hold\'em\n[O]maha\n\n[Q]uit\n> ').upper()
            if game_type != 'Q':
                print('You\'ve chosen {}'.format(["Texas Hold\'em", "Omaha"]["TO".index(game_type)]))
                while input('Start new game (Y/...)? ').upper() == 'Y':
                    game.game_of_poker(game_type)
            else:
                for player_name in client_connections.keys():
                    conn = client_connections[player_name]['Connection']
                    sync_conn.send_custom(conn, 'close', 'Game finished, thanks for playing!')
                print('Game finished, thanks for playing!')
                break

    def __client(sock: socket.socket):
        if os.path.exists(os.getcwd() + '/util/ip_data.txt') and input('Would you like to use previous IP (Y/...)? ').upper() == "Y":
            server_ip = open(os.getcwd() + '/util/ip_data.txt','r').readline()
        else:
            server_ip = input('\nEnter host IP-adress to connect to the game: ')
        while True:
            try:
                sock.connect((server_ip, 50240))
                sync_conn.receive(sock)
                data = sock.recv(1024).decode()
                while data.startswith('Connection unsuccessfull'):
                    print(data)
                    sync_conn.receive(sock)
                    data = sock.recv(1024).decode()
                print(data)
                trigger = False
                while not trigger:
                    trigger = sync_conn.receive(sock)
                open(os.getcwd() + '/util/ip_data.txt', 'w').write(server_ip)
            except Exception as err:
                print('\n'+str(err))
                if input('Try to reconnect (Y/...)? ').upper() not in 'Y':
                    print('Reconnection attempt denied\n')
                    break
    current_type = input('Choose your type: [S]erver or [C]lient (any other choice -> close): ').upper()
    if current_type not in ['C', 'S']:
        return
    __server(sock) if current_type == 'S' else __client(sock)

if __name__ == '__main__':
    sock = socket.socket()
    main(sock)
