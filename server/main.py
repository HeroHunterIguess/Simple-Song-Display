### Simple Song Server ###
### This gets currently playing song info and sends it to a client ###


import subprocess, time, socket, utils, reference

def main():
    # Setup server vars
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

    print("Server started on port: " + str(port))


    # Info loop
    while True:
        try:
            # Accept client connecting
            client_socket, address = server_socket.accept()
            print("Connected to by address: " + str(address))

            # Loop getting song info
            while True:
                
                try:
                    # Check what is actively playing based on chosen player sources
                    status = subprocess.run(["playerctl", f"--player={reference.source_one},{reference.source_two}", "status"], capture_output=True, text=True, timeout=1).stdout.strip()
                except subprocess.TimeoutExpired:
                    status = ""
                
                # Assign variable based on if media is playing or paused
                is_playing = (status == "Playing")

                # Format song information
                info = utils.setup_current_info(is_playing)

                # Try to send data
                try: 
                    client_socket.send(info.encode("utf-8"))
                # End loop if client disconnects
                except ConnectionResetError as err:
                    print("Client disconnected: " + str(err))
                    break
                except BrokenPipeError as err:
                    print("BROKEN PIPE: client likely disconnected:", err)
                    break
                
                time.sleep(0.4)
        

        # Stop server
        except KeyboardInterrupt:
            print("\nStopping server...")
            break

main()
