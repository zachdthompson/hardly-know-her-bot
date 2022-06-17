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
    

# bot.py
if __name__ == "__main__":


    connected_list = os.environ["CONNECTED_CHANNELS"].split(',')

    # Dictionary containing connected channels and specific variables
    channel_list = {}

    for streamer in connected_list:
        channel_list[streamer] = channel.Channel(streamer)

    for created in channel_list:
        save_to_file(channel_list[created])

    # bot = bot.Bot(channel_list)
    # bot.run()
