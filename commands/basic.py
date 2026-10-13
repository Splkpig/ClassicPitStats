import discord
from discord.ext import commands
from discord import app_commands

prestigeCalculations = discord.Embed(title="Prestige Calculations", color=discord.Color.greyple())
prestigeCalculations.add_field(name="/prestige-info *player*", value="Displays a player's prestige progress", inline=False)
prestigeCalculations.add_field(name="/xp-until *player*", value="Calculates the needed XP until reaching a certain Prestige and Level", inline=False)

mapQuests = discord.Embed(title="Map Quests", color=discord.Color.greyple())
mapQuests.add_field(name="/kings-quest *player*", value="Displays the granted XP from completing a King's Quest", inline=False)
mapQuests.add_field(name="/genesis *player*", value="Displays a player's Genesis Faction, points, and progress", inline=False)

stats = discord.Embed(title="Stats", color=discord.Color.greyple())
stats.add_field(name="/overview *player*", value="Displays an overview of the player's stats", inline=False)
stats.add_field(name="/compare *player1* *player2*", value="Compares the overview stats of two players", inline=False)

leaderboards = discord.Embed(title="Leaderboards", color=discord.Color.greyple())
leaderboards.add_field(name="/leaderboard *leaderboard*", value="Displays the leaderboards for a certain leaderboard", inline=False)
leaderboards.add_field(name="/leaderboard-combat *leaderboard*", value="Displays the leaderboards for a certain combat related leaderboard", inline=False)
leaderboards.add_field(name="/leaderboards", value="Displays the top 10 players for each leaderboard", inline=False)
leaderboards.add_field(name="/leaderboard-positions *player*", value="Displays a player's leaderboard positions (top 500 of each leaderboard)", inline=False)
leaderboards.add_field(name="/leaderboard-compare-positions *player1* *player2*", value="Compares the leaderboard positions of two players", inline=False)

helpPages = [prestigeCalculations, mapQuests, stats, leaderboards]
currentPage = -1


# Set up the buttons to scroll through the help command pages
class simpleView(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage
        global helpPages

        if currentPage == -1:
            currentPage = 0
            embed = helpPages[currentPage]
            view = simpleView(timeout=None)

        elif currentPage == 0:
            embed = helpPages[currentPage]
            view = simpleView(timeout=None)

        else:
            embed = helpPages[currentPage - 1]
            currentPage -= 1
            view = simpleView(timeout=None)

        embed.set_footer(text=f"Current Page: {currentPage + 1} / {len(helpPages)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage
        global helpPages

        if currentPage == -1:
            currentPage = 0
            embed = helpPages[currentPage]
            view = simpleView(timeout=None)

        elif currentPage == len(helpPages) - 1:
            embed = helpPages[currentPage]
            view = simpleView(timeout=None)

        else:
            embed = helpPages[currentPage + 1]
            currentPage += 1
            view = simpleView(timeout=None)

        embed.set_footer(text=f"Current Page: {currentPage + 1} / {len(helpPages)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa


class helpCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    global currentPage

    # Create the help command
    @app_commands.command(name="help", description="Displays the bot's commands")
    async def help(self, interaction: discord.Interaction):
        global currentPage
        currentPage = -1

        embed = discord.Embed(title="Help!", color=discord.Color.greyple())
        embed.add_field(name="View the bot's different commands", value="")

        view = simpleView(timeout=None)

        await interaction.response.send_message(embed=embed, view=view)  # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(helpCommand(client))
