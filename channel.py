"""
    Channel class file

    This file keeps track of each channel the bot is connected to, as
    well as timers and intervals specific to that channel. This allows
    the bot to function independently on each channel instead of relying on global timers.

"""



class Channel:

    def __init__(
                    self, 
                    streamer: str,
                    er_toggle: bool = True,
                    er_interval: int = 600,
                    stinky_toggle: bool = False,
                    stinky_interval: int = 600,
                    insult_toggle: bool = False,
                    insult_interval: int = 1200,
                    shut_up: bool = False
                ):
        """
        Creates a class object for each channel and establishes the
        default settings.
        :param streamer: The streamer's channel name
        :param er_toggle: Bool status of making jokes for -er words
        :param er_interval: Interval between -er jokes
        :param stinky_toggle: Bool status of making stinky jokes
        :param stinky_interval: Interval between stinky jokes
        :param insult_toggle: Bool status of insulting my friends
        :param insult_interval: Interval between insults
        :param shut_up: Bool status of if the bot is enabled
        """

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

    def to_dict(self) -> dict:
        """
        Takes a Channel object and creates a dictionary of variables
        :return: Dict of class values
        """

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

