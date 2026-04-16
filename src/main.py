# bot.py
import os

import discord

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

TEST_GUILD_ID =  os.getenv('TEST_GUILD_ID')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SUBMISSIONS_CHANNEL_NAME = os.getenv('SUBMISSIONS_CHANNEL_NAME')
print(TEST_GUILD_ID)
print(DISCORD_TOKEN)
print(SUBMISSIONS_CHANNEL_NAME)
TEST_GUILD = discord.Object(int(TEST_GUILD_ID))  # replace with your guild id
    

class MyBot(commands.Bot):
    
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.test_forum: discord.ForumChannel = None 
        
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        guild = self.get_guild(TEST_GUILD.id)
        # print(guild.text_channels, guild.categories)
        
        forums = guild.forums
        roles = guild.roles 
        managed_roles = [] 
        for role in roles:
            tags = role.tags
            if tags.bot_id == self.user.id:
                managed_roles.append(role)
        
            
        for forum in forums:
            if forum.name == SUBMISSIONS_CHANNEL_NAME:
                self.test_forum = forum 
                break 
        if not self.test_forum: 
            self.test_forum = await guild.create_forum(SUBMISSIONS_CHANNEL_NAME, default_layout=discord.ForumLayoutType.gallery_view)
            pin_thread = await self.test_forum.create_thread(
                name="test thread",
                content = "test content"
            ) 
            await pin_thread[0].edit(pinned=True)
            
        assert(self.test_forum)
        print('hi')
        
                
    async def setup_hook(self) -> None:
        # Sync the application command with Discord
        await self.tree.sync(guild=TEST_GUILD)
                

    async def on_message(self, message):
        if type(message.channel) != discord.threads.Thread:
            return
        if message.channel.parent != self.test_forum:
            return
        
        await message.add_reaction("🐛")
        print(f"content: {message.content}") 



intents = discord.Intents.default()
intents.message_content = True


bot = MyBot(command_prefix='!', intents=intents)


class Signup(discord.ui.Modal, title='Signup'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.tree.command(guild=TEST_GUILD, description='Submit in')
async def signup(interaction: discord.Interaction):
    # Send the modal with an instance of our `Feedback` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(Signup())

bot.run(DISCORD_TOKEN)
