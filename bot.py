import random
import re
import time
import os

import twitchio
from twitchio.ext import commands
from twitchio.client import Channel
from twitchio.client import User
import main


def time_passed(previous_timer, interval) -> bool:
    """
    Takes the time of the previous command and the streamer interval
    and looks for if enough time passed
    :param previous_timer: The last time something happened
    :param interval: The interval to wait to do it again
    :return: True|False if enough time has passed
    """
    if time.time() - previous_timer < int(interval):
        return False
    else:
        return True


def get_insult(friend: str) -> str:
    """
    Gets an insult for a specific friend based on their username
    """

    # Change message based on which friend I am insulting
    match friend.lower():
        case 'drachenwaffles':
            mari = [
                "DrachenWaffles? More like... like.. FartyWaffles! Goteem!",
                "Hey DrachenWaffles, can you drive me to the store? Oh wait...",
                "Mari stinks pretty bad tbh."
            ]
            return random.choice(mari)
        case 'theicarus101':
            oliver = [
                "Hey everyone look, its the kangaroo man Icarus!",
                "Oi Icarus, shut up m8 I'll fight you",
                "Icarus? More like... Pissarus. Goteem!"
            ]
            return random.choice(oliver)


class Bot(commands.Bot):
    """This is the actual bot"""

    def __init__(self, channel_list: dict, config_file: dict) -> None:
        self.channel_list = channel_list
        self.config_file = config_file

        # These words aren't funny, so skip them
        self.banned_words = self.config_file['BANNED_WORDS']

        # The list of friends to insult when seen
        self.friends = self.config_file['FRIENDS']

        # Initialise our Bot with our access token,
        # prefix, and a list of channels to join on boot...
        super().__init__(
                token=config_file['ACCESS_TOKEN'],
                prefix=config_file['BOT_PREFIX'],
                initial_channels=[key for key in channel_list]
            )

    async def event_message(self, message: twitchio.Message) -> None:
        """
        This function handles all message parsing and responses
        :param message: The messages that get read in via chat
        """

        # Ignore messages sent from the bot
        if message.echo:
            return

        # Check if we need to handle the message first
        if message.content[0] == '$':
            # only handle commands if the message is from me or a mod
            if message.author.is_mod or message.author.name == 'unknowablehobo':
                await self.handle_commands(message)
                return
        
        # The current channel the message is coming from
        streamer = self.channel_list[message.channel.name]

        # If the bot is asked to shut up, ignore everything except commands
        if streamer.shut_up and not message.content.__contains__('$'):
            return

        # Only looks for insults if enabled
        if streamer.insult_toggle:
            # Check for friends
            if message.author.name in self.friends:
                # Insult if enough time has passed
                if time_passed(streamer.insult_timer, streamer.insult_interval):
                    # Reset timer
                    streamer.insult_timer = time.time()
                    await Channel.send(
                        message.channel,
                        get_insult(message.author.name)
                    )
                    main.save_to_file(streamer)

        # Only process for -er if toggle is enabled
        if streamer.er_toggle:
            # Check if we can talk
            if time_passed(streamer.er_timer, streamer.er_interval):
                # Look for a 5+ letter words ending in -er after
                # casting the message to lower case
                regex = r"[A-z]{3,}(er)\b"
                find = re.search(regex, message.content.lower())
                if find:
                    word = find[0]
                    # Check for banned words
                    if word not in self.banned_words:
                        # Reset timer
                        streamer.er_timer = time.time()
                        await Channel.send(
                            message.channel,
                            f'{word.capitalize()}? I hardly know her!'
                        )
                        main.save_to_file(streamer)

        # Only look for stinky if enabled
        if streamer.stinky_toggle:
            # if the message has stinky in it
            if message.content.lower().__contains__('stinky'):
                # check if its been a minute since the last stinky
                if time_passed(streamer.stinky_timer, streamer.stinky_interval):
                    # Reset timer
                    streamer.stinky_timer = time.time()
                    await commands.Context.send(
                        message.channel,
                        'Uh Oh! STINKY!'
                    )
                    main.save_to_file(streamer)

    async def event_ready(self) -> None:
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    # turns off bot responses
    @commands.command()
    async def shutup(self, ctx: commands.Context):

        sender = ctx.author.name
        streamer = self.channel_list[ctx.channel.name]

        # Check for mod status of the sender 
        streamer.shut_up = True
        await ctx.send(f'Ouch, {sender}! I\'ll shut up now :( You\'ll have to '
                       f'say $imsorry if you want me back </3')

        # update the data file
        main.save_to_file(streamer)

    # handles turning the bot responses back on
    @commands.command()
    async def imsorry(self, ctx: commands.Context):

        sender = ctx.author.name
        streamer = self.channel_list[ctx.channel.name]
    
        streamer.shut_up = False
        await ctx.send(f'Do you love me again {sender}?!')

        # update the data file
        main.save_to_file(streamer)

    # Changes the intervals at which features will trigger
    @commands.command()
    async def interval(self, ctx: commands.Context):

        streamer = self.channel_list[ctx.channel.name]
        interval = ctx.message.content.split(' ')

        # Validate input for 3 total items, with the last one being a number
        if len(interval) < 3 or not interval[2].isdigit():
            await ctx.send(f'Please format the command as $interval '
                           f'<er|stinky|insult> <# of minutes>')

        feature = interval[1]
        minutes = interval[2]           # Using minutes is easer to read
        seconds = int(interval[2])*60    # Storing seconds is easier for later calculations
        changed = False                   # Tracks if the input was valid and something changed
        
        # Check for valid input features to change
        match feature:
            case 'er':
                streamer.er_interval = seconds
                changed = True
            case 'stinky':
                streamer.stinky_interval = seconds
                changed = True
            case 'insult':
                streamer.insult_timer = seconds
                changed = True

        # If change was detected, update the channel and save to file
        if changed:
            await ctx.send(
                f'I will now make {feature} jokes every {minutes} minute(s)!'
            )
            main.save_to_file(streamer)

        else:
            await ctx.send(f'Invalid input!')

    # Enables features
    @commands.command()
    async def enable(self, ctx: commands.Context):

        streamer = self.channel_list[ctx.channel.name]
        input = ctx.message.content.split(' ')

        # Validate input for 3 total items, with the last one being a number
        if len(input) < 2:
            await ctx.send(
                f'Please format the command as $enable <er|stinky|insult>'
            )

        feature = input[1]
        changed = False    # Tracks if the input was valid and something changed
        
        # Check for valid input features to change
        match feature:
            case 'er':
                streamer.er_toggle = True
                changed = True
            case 'stinky':
                streamer.stinky_toggle = True
                changed = True
            case 'insult':
                streamer.insult_toggle = True
                changed = True

        # If change was detected, update the channel and save to file
        if changed:
            await ctx.send(f'I will now make {feature} jokes!')
            main.save_to_file(streamer)

        else:
            await ctx.send(f'Invalid input!')

    # Disables features
    @commands.command()
    async def disable(self, ctx: commands.Context):

        streamer = self.channel_list[ctx.channel.name]
        input = ctx.message.content.split(' ')

        # Validate input for 3 total items, with the last one being a number
        if len(input) < 2:
            await ctx.send(
                f'Please format the command as $enable <er|stinky|insult>'
            )

        feature = input[1]
        changed = False    # Tracks if the input was valid and something changed
        
        # Check for valid input features to change
        match feature:
            case 'er':
                streamer.er_toggle = False
                changed = True
            case 'stinky':
                streamer.stinky_toggle = False
                changed = True
            case 'insult':
                streamer.insult_toggle = False
                changed = True

        # If change was detected, update the channel and save to file
        if changed:
            await ctx.send(f'I will stop making {feature} jokes...')
            main.save_to_file(streamer)

        else:
            await ctx.send(f'Invalid input!')
