import discord

PURPLE = 0x510490
RED = 0xff0000
GREEN = 0x00ff00

timeout_command_cancel = discord.Embed(
    title = 'Oops!',
    description = "You didn't respond in time!",
    footer = 'Every response has a 60 second timeout unless mentioned otherwise.',
    color = RED
)

command_cancel = discord.Embed(
    title = 'Okey-doke!',
    description = 'Alrighty! Command cancelled.',
    footer = 'Redo the command to do it again.',
    color = RED
)


# Custom Command

    # cc add

def keyword_added(keyword, reply, prefix):
    return discord.Embed(
        title = 'Keyword Added!',
        description = f'Reply `{reply}` has been added to keyword `{keyword}`.',
        footer = f'Use command "{prefix}help cc" for help.',
        color = GREEN
    )

def confirm_add(keyword, reply):
    return discord.Embed(
        title = 'You sure?',
        description = f'Are you sure you want to add response, `{reply}`, to key `{keyword}` (y/n)',
        footer = f'Respond in "y" or "n"',
        color = PURPLE
    )

def key_exists(keyword):
    return discord.Embed(
        title = 'Hold on!',
        description = f'Keyword `{keyword}` already exists! Are you sure you want to add a reply to it? (y/n)',
        footer = 'Respond in "y" or "n"',
        color = PURPLE
    )

def reply_exists(keyword, reply):
    return discord.Embed(
        title = 'Reply Exists.',
        description = f'Reply `{reply}` already exists for keyword `{keyword}`. Command cancelled.',
        footer = f'Redo the command to do it again.',
        color = RED
    )

    
    # cc remove

def key_not_found(keyword):
    return discord.Embed(
        title = 'Keyword not found!'.title(),
        description = f'Keyword, `{keyword}` not found! Bummer! Command Cancelled.',
        footer = 'Redo the command to try again.',
        color = RED
    )

def show_replies(keyword: str, replies: list):
    return discord.Embed(
        title = f'Replies for "{keyword}"',
        descrption = f'Enter index number of reply to be removed: ',
        fields = [
            {
                'name' : f'{replies.index(reply) - 1}. {reply}',
                'inline' : False
            } for reply in replies[keyword]
        ],
        footer = 'Respond with "c" to cancel command.',
        color = PURPLE
    )

def invalid_index(index: str):
    return discord.Embed(
        title = f'Invalid Index!',
        description = f'Index `{index}` is invalid! Command cancelled.',
        footer = 'Redo the command to try again.',
        color = RED
    )

def remove_reply_confirm(keyword: str, reply: str):
    return discord.Embed(
        title = 'Are you sure?',
        description = 
            f'Are you sure you want to remove response, `{reply}` from keyword, `{keyword}``. (y/n)',
        footer = 'Respond with "y" for yes or "n" for no.',
        color = PURPLE
    )

def reply_removed(keyword: str, reply: str):
    return discord.Embed(
        title = f'Response Removed!',
        description = f'Response `{reply}` has been removed from keyword `{keyword}`.',
        color = GREEN
    )