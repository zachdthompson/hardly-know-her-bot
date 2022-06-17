# bot.py
import os # for importing env vars for the bot to use
import channel
import re
import bot
import json
    
def save_to_file(object):

    try:
        # Create a file named after the streamer for easy input
        object_dict = object.to_dict()
        streamer = object_dict["streamer"]
        path = os.path.join("channels", f"{streamer}.txt")

        # Write dictionary out to the file
        with open(path, 'w') as output_file:
            output_file.write(json.dumps(object_dict))

        # If successful return true
        output_file.close()
        return True

    # if something goes wrong, return false
    except:
        return False

def file_exists(streamer):
    """Checks if a data file exists for a streamer or not"""

    cwd = os.getcwd()
    path = os.path.join(cwd, "channels", f"{streamer}.txt")

    if os.path.exists(path):
        return True

    else:
        return False


def load_from_file(streamer):
    
    path = os.path.join("channels", f"{streamer}.txt")

    # Open file and read in as json
    with open(path, 'r') as input_file:
        contents = input_file.read()

        object_dict = json.loads(contents)

    # Create object and return it
    streamer = channel.Channel(
        object_dict["streamer"],
        object_dict["er_toggle"],
        object_dict["er_interval"],
        object_dict["stinky_toggle"],
        object_dict["stinky_interval"],
        object_dict["insult_toggle"],
        object_dict["insult_interval"],
        object_dict["shut_up"]
    )
    
    return streamer
    

# bot.py
if __name__ == "__main__":

    # List of channels to connect to
    connected_list = os.environ["CONNECTED_CHANNELS"].split(',')

    # Dictionary containing connected channels and thier variables
    channel_list = {}

    # Create Streamer Variables
    for streamer in connected_list:

        # If the streamer already has a data file, load it
        if file_exists(streamer):
            
            channel_list[streamer] = load_from_file(streamer)

        # If data file does not exist, create a new one
        else:
            channel_list[streamer] = channel.Channel(streamer)
            save_to_file(channel_list[streamer])


    bot = bot.Bot(channel_list)
    bot.run()
