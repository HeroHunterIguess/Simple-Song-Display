### Simple Song Server ###
### Get currently playing song info and host it as server ###
# Run in a systemd service called simple-song-server.service


import subprocess, time, socket, utils

# Setup/format information to be sent
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

# Start Server 
def main():
    # Setup server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "0.0.0.0"
    port = 7463

    # Try to start server
    try:
        server_socket.bind((host, port))
    except OSError as err:
        print("Port likely in use:", err)
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
                
                # Check if song is playing or paused
                if status == "Paused":
                    is_playing = False
                elif status == "Playing":
                    is_playing = True
                else: 
                    is_playing = False

                # Send info to client
                info = setup_current_info(is_playing)

                # Try to send data
                try: 
                    client_socket.send(info.encode("utf-8"))
                # End loop if client disconnects
                except ConnectionResetError as err:
                    print("CLIENT DISCONNECTED: " + str(err))
                    break
                except BrokenPipeError as err:
                    print("BROKEN PIPE: CLIENT LIKELY DISCONNECTED:", err)
                    break
                
                time.sleep(0.5)
        
        # Stop server
        except KeyboardInterrupt:
            print("\nStopping server...")
            break

main()
