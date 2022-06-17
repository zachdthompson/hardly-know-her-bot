import re
import time
import os
from twitchio.ext import commands
from twitchio.client import Channel
from twitchio.client import User

def time_passed(oldtime, interval):
    """Takes the time of the previous command and the streamer interval and looks for seconds passed"""
    if (time.time() - oldtime < int(interval)):
        return False
    else:
        return True

def get_insult(friend):
    """Gets an insult for a specific friend based on their username"""

    # Change message based on which friend I am insulting
    match friend:
        case 'drachenwaffles':
            return 'Waffles stinks >:('
        case 'theicarus101':
            return 'Oi, get lost Icarus'
        case 'gayfairycat':
            return 'Anne is smelly...'


class Bot(commands.Bot):
    """This is the actual bot"""

    def __init__(self, channel_list):
        self.channel_list = channel_list
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(
                token=os.environ['ACCESS_TOKEN'], 
                prefix=os.environ['BOT_PREFIX'],
                initial_channels=[key for key in channel_list]
            )


    async def event_message(self, message):
        """This function handles all message parsing and responses"""

        # Regex to find hardly know her jokes
        regex = r"[A-z]{3,}(er)\b"

        # These words arent funny, so skip them
        banned_words = os.environ['BANNED_WORDS']

        # The list of friends to insult when seen
        friends = os.environ['FRIENDS']
        
        # The current channel the message is coming from
        streamer = self.channel_list[message.channel.name]

        # Ignore messages sent from the bot
        if message.echo:
            return

        # If the bot is asked to shut up, ignore everything except commands
        if streamer.shut_up and not message.content.__contains__('$'):
            return

        #check for friends, insult them on the interval
        if message.author.name in friends and time_passed(streamer.insult_friends_timer, streamer.interval):
            streamer.insult_friends_timer = time.time()
            await Channel.send(message.channel, get_insult(message.author.name))
        
        # Look for a match after casting the message to lower case
        find = re.search(regex, message.content.lower())

        # Found a 5+ letter word ending in er
        if (find):
            # Check if its been a minute since the last joke, only proceed if true
            # Check for banned words
            if time_passed(streamer.er_timer, streamer.interval) and (find[0] not in banned_words):
                # set new timer
                streamer.er_timer = time.time()
                await Channel.send(message.channel, f'{find[0].capitalize()}? I hardly know her!')


        # if the message has stinky in it
        elif (message.content.lower().__contains__('stinky')):
            # check if its been a minute since the last stinky
            if time_passed(streamer.stinky_timer, streamer.interval):
                # reset stinky timer
                streamer.stinky_timer = time.time()
                await commands.Context.send(message.channel, f'Uh Oh! STINKY!')


        # handle for commands
        else:
            await self.handle_commands(message)


    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    
    # turns off bot responses
    @commands.command()
    async def shutup(self, ctx: commands.Context):

        sender = ctx.author.name
        streamer = self.channel_list[ctx.channel.name]

        # Ignore Icarus
        if sender == 'theicarus101':
            ctx.reply('Oi frick off you jerk! Dont tell me what to do!')

        # Check for mod status of the sender
        elif (ctx.author.is_mod):
            streamer.shut_up = True
            await ctx.send(f'Ouch, {sender}! I\'ll shut up now :( You\'ll have to say $imsorry if you want me back </3')

        else:
            await ctx.send('You cant tell me what to do, smelly!')


    # handles turning the bot responses back on
    @commands.command()
    async def imsorry(self, ctx: commands.Context):

        sender = ctx.author.name
        streamer = self.channel_list[ctx.channel.name]
        
        # Check for mod status of the sender
        if (ctx.author.is_mod):
            streamer.shut_up = False
            await ctx.send(f'Do you love me again {sender}?!')
    

    # handles turning the bot responses back on
    @commands.command()
    async def interval(self, ctx: commands.Context):

        streamer = self.channel_list[ctx.channel.name]
        interval = ctx.message.content.split(' ')

        # Make sure the interval sent is a number
        if not interval[1].isdigit():
            await ctx.send(f'Please format the command as $interval <# of seconds>')
            return
        
        # Update streamer interval
        if (ctx.author.is_mod) or ctx.author.name == 'unknowablehobo':
            streamer.interval = interval[1]
            await ctx.send(f'I will now make dumb jokes every {interval[1]} seconds!')


    # Handles the help command
    @commands.command()
    async def help(self, ctx: commands.Context):
        
        # Check for mod status of the sender
        if (ctx.author.is_mod):
            await ctx.reply(f'$shutup - Disable bot, $interval <number> - Change reply interval seconds')
        
        else:
            await ctx.reply('I dont have to tell you anything!')
