import os 
import channel
import bot
import yaml


def save_to_file(streamer_obj: channel.Channel) -> bool:
    """
    Saves a streamers channel object to their file
    :param streamer_obj: The class object of the streamer
    :return: True|False if the object was saved
    """

    try:
        # Create a file named after the streamer for easy input
        object_dict = streamer_obj.to_dict()
        streamer = object_dict["streamer"]
        path = os.path.join("channels", f"{streamer}.yaml")

        # Write dictionary out to the file
        with open(path, 'w+') as output_file:
            yaml.dump(object_dict, output_file, allow_unicode=True)

        # If successful return true
        output_file.close()
        return True

    # if something goes wrong, return false
    except:
        return False


def load_from_file(streamer_name: str) -> channel.Channel:
    """
    Loads a streamer class object from the file storage
    :param streamer_name: The name of the streamer to load
    """
    
    path = os.path.join("channels", f"{streamer_name}.yaml")

    # Open file and read in as json
    with open(path, 'r') as input_file:
        object_dict = yaml.safe_load(input_file)


    # Create object and return it
    streamer_obj = channel.Channel(
        object_dict["streamer"],
        object_dict["er_toggle"],
        object_dict["er_interval"],
        object_dict["stinky_toggle"],
        object_dict["stinky_interval"],
        object_dict["insult_toggle"],
        object_dict["insult_interval"],
        object_dict["shut_up"]
    )

    if object_dict["er_timer"] != 0:
        streamer_obj.er_timer = object_dict["er_timer"]

    if object_dict["stinky_timer"] != 0:
        streamer_obj.stinky_timer = object_dict["stinky_timer"]

    if object_dict["insult_timer"] != 0:
        streamer_obj.insult_timer = object_dict["insult_timer"]
    
    return streamer_obj
    

# bot.py
if __name__ == "__main__":

    yaml_path = os.path.join(os.getcwd(), 'config.yaml')

    with open(yaml_path, 'r') as config:
        config_file = yaml.safe_load(config)

    # List of channels to connect to
    connected_list = config_file['CONNECTED_CHANNELS']

    # Dictionary containing connected channels and thier variables
    channel_list = {}

    # Create Streamer Variables
    for streamer in connected_list:

        cwd = os.getcwd()
        path = os.path.join(cwd, "channels", f"{streamer}.yaml")

        # If the streamer already has a data file, load it
        if os.path.exists(path):

            channel_list[streamer] = load_from_file(streamer)

        # If data file does not exist, create a new one
        else:
            channel_list[streamer] = channel.Channel(streamer)
            save_to_file(channel_list[streamer])

    bot = bot.Bot(channel_list, config_file)
    bot.run()
