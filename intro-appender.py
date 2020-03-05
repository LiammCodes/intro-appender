# Video Appender
# Created by Liam Moore
# March 1st, 2020

import subprocess
import os
import glob
# from sys import exit

# functions
def get_resolution(video):
    resolution = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=height,width', '-of', 'csv=s=x:p=0', video])
    resolution = resolution.decode()
    resolution_list = resolution.split("x")

    # get width
    get_resolution.width = resolution_list[0]
    # get height
    get_resolution.height = resolution_list[1]

def resize(video, width, height):
    subprocess.call(['ffmpeg', '-i', video, '-vf', 'scale=' + width + ':' + height + ':force_original_aspect_ratio=decrease,pad=' + width + ':' + height + ':(ow-iw)/2:(oh-ih)/2', '-r', '30', 'Results/temp.mp4'])

# take initial input
print(".--------------------------------------------------.")
print("|--------------- Intro Appender v1.0 --------------|")
print("| MAKE SURE THIS PROGRAM IS IN THE SAME FOLDER AS  |")
print("| THE VIDEOS YOU WISH TO USE IN YOUR FINAL PRODUCT |")
print("'--------------------------------------------------'")

# find current working directory
cwd = os.getcwd()

# look for Videos folder
if ((not os.path.exists(cwd + "/Videos"))):
    os.mkdir(cwd + "/Videos")
    print("Videos folder created.")
else:
    print("Videos folder found.")

# prompt user to place videos in assigned folders
print("Please put the intro video in the current directory, and place the video series in the \"Videos\" folder.")
answer = input("Press any key to continue (or type quit)... ")

# locate intro file
while answer != "quit":

    # makes sure there is only one intro file in the root directory
    count = 0
    while (count != 1):
        count = 0
        
        # locates intro file(s) (must only be one, but handles more as an error)
        for intro in glob.glob("*.mp4"):
            count = count + 1

        if (count != 1):
            print("Too many or not enough videos in root directory. Make sure theres only one (the intro) and try again.")
            print(count)
            answer = input("Press any key to continue (or type quit)... ")
            
            if (answer == "quit"): 
                break

    # locate intro inout path
    intro_input_path = cwd + '/' + intro

    # check if Results folder exists, make the directory if not
    if not os.path.exists(cwd + '/Results'):
        print("No results folder found, creating one now...")
        os.mkdir(cwd + "/Results")
        print("Folder created.")
    else:
        print("Results folder found.")

    # dummy thicc loop for appending intro to every file in "Videos" folder
    for video_input_path in glob.glob("Videos/*.mp4"):

        # is the video and intro the same resolution

        # get width & height of INTRO
        get_resolution(intro)
        intro_width = get_resolution.width
        intro_height = get_resolution.height
        intro_pixel_count = int(intro_width) * int(intro_height)

        # get width & height of VIDEO
        get_resolution(video_input_path)
        video_width = get_resolution.width
        video_height = get_resolution.height
        video_pixel_count = int(video_width) * int(video_height)

        # check which video has the smaller resolution, and downscale it....
        # intro video need to be downscaled to video size (only needs to happen once)
        if(video_pixel_count < intro_pixel_count):
            resize(intro, video_width, video_height)
        elif(intro_pixel_count < video_pixel_count):
            resize(video, intro_width, intro_height)

        # scale intro to be 1280x720
        # subprocess.call(['ffmpeg', '-i', intro, '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2', '-r', '30', 'Results/intro_conformed.mp4'])
        # subprocess.call(['ffmpeg', '-i', video, '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2', '-r', '30', 'Results/intro_conformed.mp4'])

        # write files to temp txt file
        with open("temp.txt", "w") as file:
            file.write("file Results/temp.mp4" + "\nfile " + video_input_path)

        video_list = video_input_path.split("Videos/")
        video = video_list[1]

        # output segment
        video_output_path = cwd + '/Results/' + video
        print("Working...")
        subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'temp.txt', '-c', 'copy', video_output_path])
        os.remove("temp.txt")
        # TODO
        os.remove("Results/temp.mp4")

        # completion message
        print(intro + " and " + video + " were concatinated successfully.")

    # take input to continue loop
    print("Complete!")
    answer = "quit"

print("Exiting...")