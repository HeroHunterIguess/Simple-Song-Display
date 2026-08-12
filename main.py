### Get currently playing song info and host it as server ###

import paramiko, subprocess, time, socket, utils

# Write current information
def write_current_info(is_playing):
    title, artist, artURL, length, album = utils.get_current_playing()

    final_info = title+"\n"
    final_info += artist+"\n"
    final_info += artURL+"\n"
    final_info += str(length)+"\n"
    final_info += str(is_playing)+"\n"
    final_info += album+"\n"

    return final_info

def main():

    # Setup server info
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "0.0.0.0"
    port = 7463
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("server started on port: " + str(port))

    while True:
        try:
            client_socket, address = server_socket.accept()
            print("connected to by address: " + str(address))

            while True:
                # Loop getting song info
                status = subprocess.run("playerctl --player=subtui,spotify status", shell=True, capture_output=True, text=True).stdout.strip()
                if status == "Paused":
                    is_playing = False
                elif status == "Playing":
                    is_playing = True
                else: 
                    is_playing = False

                # Write info to raspi
                info = write_current_info(is_playing)

                client_socket.send(info.encode("utf-8"))
                
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping server...")
            break

main()
