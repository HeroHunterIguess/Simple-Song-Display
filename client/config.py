### Simple Song Display configuration ###
# Default config
# Do not remove any values


#############################
### Appearance            ###
#############################

# Options are: "Windowed" or "DirectDraw"
display_mode = "Windowed"
# DirectDraw will draw to the following framebuffer 
# Default is /dev/fb1
frame_buffer = "1"

mode = "Centered" # Only option is 'Centered'

background_color = (30,30,30)

display_size = (480,320)

# Paddings
line_padding = 7
padding_top = 6
horizontal_padding = 4

album_cover_height = 8
album_cover_size = (182,182)

gaussian_blur_radius = 21
background_image_size = (480,480)

background_brightness = 0.4


#############################
### Text                  ###
#############################

main_text_color = (255,255,255)
secondary_text_color = (180,180,180)
tertiary_text_color = (155,155,155)

main_font = "Gotham Medium"
main_font_bold = False
secondary_font = "Gotham Light"
secondary_font_bold = False

main_font_size = 36
secondary_font_size = 29
tertiary_font_size = 24

tertiary_italic = True

# Text spacing
# This is the height of each line of text from the top
spacing_one = 197
spacing_two = 233
spacing_three = 264
spacing_four = 290

# Font size of clock = main font size * multiplier
clock_size_multiplier = 4 


#############################
### Debug                 ###
#############################

# Both require a log_file to be specified in misc section

output = False # General output/logging messages
output_transfer_info = False # Output the data recieved in each transfer


#############################
### No media screen       ###
#############################

no_media_background_image = False # Disables rendering of the image below and instead uses background_color
no_media_background_image_link = "https://raylees-void.neocities.org/image_storage/The_Arcadian_or_Pastoral_State.jpg"

no_media_clock = True # Show clock if no media is playing
no_media_message = "No media." # Disregarded if no_media_clock is true


#############################
### Misc                  ###
#############################

truncation_length = 10 # UNUSED # Length of a line of text before its shortened 

pause_icon = "https://raylees-void.neocities.org/image_storage/paused.png"
paused_darkening = 140

#log_file = "/home/herohunter/Everything/simple_song_display_log.txt"
