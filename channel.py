"""
    Channel class file

    This file keeps track of each channel the bot is connected to, as well as
    timers and interals specific to that channel. This allows the bot to function
    independantly on each channel instead of relying on global timers.

    Constructor:
    Streamer = Streamer name *required
    interval = How frequently the streamer wants commands, default 600
    er_timner = Keeps track of the last time a hardly know her was made
    stinky_timer = Keeps track of the last time stinky was said
    insult_friends_timer = Keeps track of the last insult at friends

"""



class Channel:

    def __init__(
                    self, 
                    streamer, 
                    er_toggle = True,
                    er_interval = 600,
                    stinky_toggle = True,
                    stinky_interval = 600,
                    insult_toggle = False,
                    insult_interval = 1200,
                    shut_up = False
                ):

        self.streamer = streamer

        # Hardly Know Her Variables
        self.er_timer = 0 # Timers reset to 0
        self.er_interval = er_interval
        self.er_toggle = er_toggle

        # Stinky variables
        self.stinky_timer = 0 # Timers reset to 0
        self.stinky_interval = stinky_interval
        self.stinky_toggle = stinky_toggle

        # Insult Variables
        self.insult_timer = 0 # Timers reset to 0
        self.insult_interval = insult_interval
        self.insult_toggle = insult_toggle

        # General variables
        self.shut_up = shut_up

    def to_dict(self):
        """Takes a Channel object and creates a dictionary to be saved to a file"""

        output = {
            "streamer": self.streamer,
            "er_interval": self.er_interval,
            "er_toggle": self.er_toggle,
            "stinky_interval": self.stinky_interval,
            "stinky_toggle": self.stinky_toggle,
            "insult_interval": self.insult_interval,
            "insult_toggle": self.insult_toggle,
            "shut_up": self.shut_up,
        }

        return output

