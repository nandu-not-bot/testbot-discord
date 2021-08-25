import discord

PURPLE = 0x510490

timeout_command_cancel = discord.Embed(
    title = 'Oops!',
    description = "You didn't respond in time!",
    footer = 'Every response has a 60 second timeout unless mentioned otherwise.',
    color = discord.Colour.red()
)

command_cancel = discord.Embed(
    title = 'Okey-doke!',
    description = 'Alrighty! Command cancelled.',
    footer = 'Redo the command to do it again.',
    color = discord.Colour.red()
)


# Custom Command

    # cc add

def keyword_added(keyword, reply, prefix):
    return discord.Embed(
        title = 'Keyword Added!',
        description = f'Reply `{reply}` has been added to keyword `{keyword}`.',
        footer = f'Use command "{prefix}help cc" for help.',
        color = discord.Colour.green()
    )

def confirm_add(keyword, reply):
    return discord.Embed(
        title = 'You sure?',
        description = f'Are you sure you want to add response, `{reply}`, to key `{keyword}` (y/n)',
        footer = f'Respond in "y" or "n"',
        color = PURPLE
    )

def reply_exists(keyword, reply):
    return discord.Embed(
        title = 'Reply Exists.',
        description = f'Reply `{reply}` already exists for keyword `{keyword}`. Command cancelled.',
        footer = f'Redo the command to do it again.',
        color = discord.Colour.red()
    )

    
    # cc remove

