### Simple Song Server ###
### Get currently playing song info and host it as server ###

import subprocess, time, socket, utils

# Setup information to be sent
def setup_current_info(is_playing):
    title, artist, artURL, length, album, position = utils.get_current_playing()

    final_info = title+"\n"
    final_info += artist+"\n"
    final_info += artURL+"\n"
    final_info += str(length)+"\n"
    final_info += str(is_playing)+"\n"
    final_info += album+"\n"
    final_info += str(position)+"\n"

    return final_info

# Server
def main():
    # Setup server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "0.0.0.0"
    port = 7463

    try:
        server_socket.bind((host, port))
    except OSError as err:
        # Set backup in case port is in use
        print("Port likely in use: " + str(err))
        return
    
    server_socket.listen(5)

    print("server started on port: " + str(port))

    # Info sending loop
    while True:
        try:
            # Accept client connecting
            client_socket, address = server_socket.accept()
            print("connected to by address: " + str(address))

            while True:
                # Loop getting song info
                try:
                    status = subprocess.run(["playerctl", "--player=subtui,spotify", "status"], capture_output=True, text=True, timeout=1).stdout.strip()
                except subprocess.TimeoutExpired:
                    status = ""
                
                if status == "Paused":
                    is_playing = False
                elif status == "Playing":
                    is_playing = True
                else: 
                    is_playing = False

                # Send info to client
                info = setup_current_info(is_playing)

                try: 
                    client_socket.send(info.encode("utf-8"))
                # End loop if client disconnects
                except ConnectionResetError as err:
                    print("CLIENT DISCONNECTED: " + str(err))
                    break
                except BrokenPipeError as err:
                    print("BROKEN PIPE: CLIENT LIKELY DISCONNECTED: " + str(err))
                    break
                
                time.sleep(0.5)
        
        # Stop server
        except KeyboardInterrupt:
            print("\nStopping server...")
            break

main()
