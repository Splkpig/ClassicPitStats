import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from useful_things import formatting_functions
from useful_things import pit_functions
from useful_things.api_functions import getInfo
from useful_things.discord_functions import footerDateGen
from useful_things.pit_functions import calcBracketColor

# Global lists of the Pit Classic leaderboards in functional and formatted forms
globalLeaderboardsList = ["kills", "assists", "damage_dealt", "deaths", "total_xp", "current_gold", "cash_earned", "playtime_minutes", "gapple_eaten", "ghead_eaten", "lava_bucket_emptied", "left_clicks", "chat_messages", "wheat_farmed", "fished_anything", "blocks_broken", "blocks_placed", "king_quest_completion", "sewer_treasures_found", "night_quests_completed", "renown", "arrows_fired", "arrow_hits", "jumped_into_pit", "launched_by_launchers", "diamond_items_purchased", "fishes_fished", "fishing_rod_launched"]
globalLeaderboardsFormatedList = ["<:ironsword:1247392632129323080> Kills", "<:woodensword:1248118747697250376> Assists", "<:damagedealt:1248127865103585391> Damage Dealt", "<:ironchestplate:1247719811857907762> Deaths", "<:xpbottle:1245974825865056276> Total XP", "<:goldingot:1247391882968043652> Current Gold", "<:goldingot:1247391882968043652> Lifetime Gold", "<a:minecraftclock:1247400003786510479> Playtime", "<:goldenapple:1248127429084577913> Golden Apples Eaten", "<:goldenhead:1248127570373775433> Golden Heads", "<:lavabucket:1248126173074952222> Lava Buckets Emptied", ":regional_indicator_l: Left Clicks", ":regional_indicator_t: Chat Messages", "<:wheat:1248124503255420928> Wheat Farmed", "<:tripwirehook:1248127264755810407> Fished Anything", "<:diamondpickaxe:1248119046172446792> Blocks Broken", "<:obsidian:1248119285075935396> Blocks Placed", "<:goldenhelmet:1248126543553892443> Kings Quest Completions", "<:chest:1248125595678937099> Sewer Treasures", "<:coal:1248125818744602636> Night Quests", "<:emerald:1248128261272244305> Current Renown", "<:Bow:1248118009369854002> Arrows Shot", "<:Arrow:1248117169653284926> Arrow Hits", "<:thepit:1248129525825409054> Jumps into Mid", "<:slimeblock:1248126317745143828> Launcher Launches", "<:diamondchestplate:1248121536985169960> Diamond Items Purchased", "<:rawcod:1248126906851790848> Fished Fish", "<:fishingrod:1248127083549556736> Fishing Rod Casts"]
globalLeaderboardsNameList = ["Kills", "Assists", "Damage Dealt", "Deaths", "Total XP", "Current Gold", "Lifetime Gold", "Playtime", "Golden Apples Eaten", "Golden Heads", "Lava Buckets Emptied", "Left Clicks", "Chat Messages", "Wheat Farmed", "Fished Anything", "Blocks Broken", "Blocks Placed", "Kings Quest Completions", "Sewer Treasures", "Night Quests", "Current Renown", "Arrows Shot", "Arrow Hits", "Jumps into Mid", "Launcher Launches", "Diamond Items Purchased", "Fished Fish", "Fishing Rod Casts"]

# Track the current page and leaderboard
currentPage = 0
globalLeaderboard = ''


# Get the positions of players (by UUID) on every leaderboard, in the same order as globalLeaderboardsList
async def getAllPositions(uuids: list):
    return await asyncio.gather(*[asyncio.to_thread(pit_functions.getLeaderboardPositions, lb, uuids) for lb in globalLeaderboardsList])


# Create the buttons to scroll through the rankings of a leaderboard
class simpleView(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage
        global globalLeaderboard

        if currentPage == 0:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(globalLeaderboard)]} Page: {currentPage + 1}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbed(pit_functions.getLeaderboardData(globalLeaderboard, 10, currentPage), embed, currentPage)
            view = simpleView(timeout=None)
            embed.set_footer(text=footerDateGen())

            await interaction.response.edit_message(embed=embed, view=view) # noqa
        else:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(globalLeaderboard)]} Page: {currentPage}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbed(pit_functions.getLeaderboardData(globalLeaderboard, 10, currentPage - 1), embed, currentPage - 1)
            currentPage -= 1
            view = simpleView(timeout=None)
            embed.set_footer(text=footerDateGen())

            await interaction.response.edit_message(embed=embed, view=view) # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage

        embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(globalLeaderboard)]} Page: {currentPage + 2}", color=discord.Color.greyple())
        embed = formatting_functions.leaderboardEmbed(pit_functions.getLeaderboardData(globalLeaderboard, 10, currentPage + 1), embed, currentPage + 1)
        currentPage += 1
        view = simpleView(timeout=None)
        embed.set_footer(text=footerDateGen())

        await interaction.response.edit_message(embed=embed, view=view) # noqa


currentPageAll = 0


# Create the buttons to scroll through the top 10 players of each leaderboard
class simpleViewAll(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPageAll
        global globalLeaderboard

        if currentPageAll == 0:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll]}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbedAll(pit_functions.getLeaderboardDataAll(globalLeaderboardsList[currentPageAll], 10), embed)
            view = simpleViewAll(timeout=None)

        else:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll - 1]}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbedAll(pit_functions.getLeaderboardDataAll(globalLeaderboardsList[currentPageAll - 1], 10,), embed)
            currentPageAll -= 1
            view = simpleViewAll(timeout=None)

        embed.set_footer(text=f"Current Page: {currentPageAll + 1} / {len(globalLeaderboardsList)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPageAll

        if currentPageAll == len(globalLeaderboardsList) - 1:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll]}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbedAll(pit_functions.getLeaderboardDataAll(globalLeaderboardsList[currentPageAll], 10), embed)
            view = simpleViewAll(timeout=None)

        else:
            embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll + 1]}", color=discord.Color.greyple())
            embed = formatting_functions.leaderboardEmbedAll(pit_functions.getLeaderboardDataAll(globalLeaderboardsList[currentPageAll + 1], 10), embed)
            currentPageAll += 1
            view = simpleViewAll(timeout=None)

        embed.set_footer(text=f"Current Page: {currentPageAll + 1} / {len(globalLeaderboardsList)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa


leaderboardPositionPage = 0
leaderboardPositionPages = []


# Create the buttons to scroll through a player's current leaderboard positions
class simpleViewPositions(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global leaderboardPositionPage
        global leaderboardPositionPages

        if leaderboardPositionPage == 0:
            embed = leaderboardPositionPages[leaderboardPositionPage]
            view = simpleViewPositions(timeout=None)

        else:
            embed = leaderboardPositionPages[leaderboardPositionPage - 1]
            leaderboardPositionPage -= 1
            view = simpleViewPositions(timeout=None)

        embed.set_footer(text=f"Current Page: {leaderboardPositionPage + 1} / {len(leaderboardPositionPages)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global leaderboardPositionPage
        global leaderboardPositionPages

        if leaderboardPositionPage == len(leaderboardPositionPages) - 1:
            embed = leaderboardPositionPages[leaderboardPositionPage]
            view = simpleViewPositions(timeout=None)

        else:
            embed = leaderboardPositionPages[leaderboardPositionPage + 1]
            leaderboardPositionPage += 1
            view = simpleViewPositions(timeout=None)

        embed.set_footer(text=f"Current Page: {leaderboardPositionPage + 1} / {len(leaderboardPositionPages)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa


class leaderboards(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Create the leaderboard positions command
    @app_commands.command(name="leaderboard-positions", description="Shows a player's leaderboard positions")
    async def overview(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        pass

        global leaderboardPositionPage
        global leaderboardPositionPages

        leaderboardPositionPage = 0
        leaderboardPositionPages = []

        await interaction.response.defer()  # noqa

        player = player.strip()
        data = await asyncio.to_thread(getInfo, f"{pit_functions.CLASSIC_API}/player/{player}")

        if data.get("message", "") != "":
            embedFail = discord.Embed(title=f"{player} not found", color=discord.Color.red())

            await interaction.followup.send(embed=embedFail)  # noqa

        else:
            playerData = data["data"]["player"]
            currentPrestige = playerData["prestige"]
            currentLevel = playerData["level"]
            uuid = playerData["uuid"].replace("-", "")

            global globalLeaderboardsFormatedList
            leaderboardsFormatedList = globalLeaderboardsFormatedList
            playersRankings = []

            embed = discord.Embed(title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {playerData['ign']}", color=calcBracketColor(currentPrestige))
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{uuid}?format=webp")

            rankingsFormatted = [positions.get(uuid, 999999) for positions in await getAllPositions([uuid])]

            for i in range(0, len(rankingsFormatted)):
                playersRankings.append({leaderboardsFormatedList[i]: rankingsFormatted[i]})
                # print(f"finished {leaderboardsFormatedList[i][leaderboardsFormatedList[i].index(' ') + 1:]}")

            sorted_leaderboards = sorted(playersRankings, key=lambda x: list(x.values())[0], reverse=False)

            i = 0
            for idx, leaderboard in enumerate(sorted_leaderboards, start=1):
                if i % 10 == 0 and i != 0:
                    leaderboardPositionPages.append(embed)
                    embed = discord.Embed(title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {playerData['ign']}", color=calcBracketColor(currentPrestige))
                    embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{uuid}?format=webp")
                leaderboard_name, ranking = leaderboard.popitem()
                if ranking == 999999:
                    embed.add_field(name=f"{leaderboard_name}:", value="N/A", inline=False)
                elif ranking == 1:
                    embed.add_field(name=f"{leaderboard_name}:", value=f":first_place: #{ranking}", inline=False)
                elif ranking <= 10:
                    embed.add_field(name=f"{leaderboard_name}:", value=f":second_place: #{ranking}", inline=False)
                elif ranking <= 100:
                    embed.add_field(name=f"{leaderboard_name}:", value=f":third_place: #{ranking}", inline=False)
                else:
                    embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking}", inline=False)
                if i == len(sorted_leaderboards) - 1:
                    leaderboardPositionPages.append(embed)
                i += 1

            embed = leaderboardPositionPages[0]
            embed.set_footer(text=f"Current Page: {leaderboardPositionPage + 1} / {len(leaderboardPositionPages)}")
            view = simpleViewPositions(timeout=None)

            await interaction.followup.send(embed=embed, view=view)  # noqa

    # Create the leaderboard command
    @app_commands.command(name="leaderboard", description="Shows a leaderboard")
    @app_commands.choices(leaderboard=[app_commands.Choice(name='Total XP', value="total_xp"), app_commands.Choice(name='Current Gold', value="current_gold"), app_commands.Choice(name='Lifetime Gold', value="cash_earned"), app_commands.Choice(name='Playtime', value="playtime_minutes"), app_commands.Choice(name='Chat Messages', value="chat_messages"), app_commands.Choice(name='Wheat Farmed', value="wheat_farmed"), app_commands.Choice(name='Fished Anything', value="fished_anything"), app_commands.Choice(name='Blocks Broken', value="blocks_broken"), app_commands.Choice(name='Blocks Placed', value="blocks_placed"), app_commands.Choice(name='Kings Quest Completions', value="king_quest_completion"), app_commands.Choice(name='Sewer Treasures', value="sewer_treasures_found"), app_commands.Choice(name='Night Quests', value="night_quests_completed"), app_commands.Choice(name='Current Renown', value="renown"), app_commands.Choice(name='Jumps into Mid', value="jumped_into_pit"), app_commands.Choice(name='Launcher Launches', value="launched_by_launchers"), app_commands.Choice(name='Diamond Items Purchased', value="diamond_items_purchased"), app_commands.Choice(name='Fished Fish', value="fishes_fished"), app_commands.Choice(name='Fishing Rod Casts', value="fishing_rod_launched")])
    async def leaderboard(self, interaction: discord.Interaction, leaderboard: str):
        global globalLeaderboard
        global currentPage
        currentPage = 0
        globalLeaderboard = leaderboard

        await interaction.response.defer() # noqa

        embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(leaderboard)]} Page: {currentPage + 1}", color=discord.Color.greyple())
        i = 1

        for player in pit_functions.getLeaderboardData(leaderboard, 10, 0):
            embed.add_field(name=f"#{i}:", value=f"{player}", inline=False)
            i += 1

        embed.set_footer(text=footerDateGen())

        view = simpleView(timeout=None)
        await interaction.followup.send(embed=embed, view=view)

    # Create the leaderboard combat command
    @app_commands.command(name="leaderboard-combat", description="Shows a combat related leaderboard")
    @app_commands.choices(leaderboard=[app_commands.Choice(name='Kills', value="kills"), app_commands.Choice(name='Assists', value="assists"), app_commands.Choice(name='Damage Dealt', value="damage_dealt"), app_commands.Choice(name='Deaths', value="deaths"), app_commands.Choice(name='Golden Apples Eaten', value="gapple_eaten"), app_commands.Choice(name='Golden Heads', value="ghead_eaten"), app_commands.Choice(name='Lava Buckets Emptied', value="lava_bucket_emptied"), app_commands.Choice(name='Left Clicks', value="left_clicks"), app_commands.Choice(name='Arrows Shot', value="arrows_fired"), app_commands.Choice(name='Arrow Hits', value="arrow_hits")])
    async def leaderboardCombat(self, interaction: discord.Interaction, leaderboard: str):
        global globalLeaderboard
        global currentPage
        currentPage = 0
        globalLeaderboard = leaderboard

        await interaction.response.defer() # noqa

        embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[globalLeaderboardsList.index(leaderboard)]} Page: {currentPage + 1}", color=discord.Color.greyple())
        i = 1

        for player in pit_functions.getLeaderboardData(leaderboard, 10, 0):
            embed.add_field(name=f"#{i}:", value=f"{player}", inline=False)
            i += 1

        embed.set_footer(text=footerDateGen())

        view = simpleView(timeout=None)
        await interaction.followup.send(embed=embed, view=view)

    # Create the leaderboards command
    @app_commands.command(name="leaderboards", description="Shows the top 10 of every leaderboard")
    async def leaderboardsAll(self, interaction: discord.Interaction):
        global currentPageAll
        currentPageAll = 0

        await interaction.response.defer() # noqa

        embed = discord.Embed(title=f"{globalLeaderboardsFormatedList[currentPageAll]}", color=discord.Color.greyple())
        i = 1

        for player in pit_functions.getLeaderboardData(globalLeaderboardsList[currentPageAll], 10, 0):
            embed.add_field(name=f"#{i}:", value=f"{player}", inline=False)
            i += 1

        embed.set_footer(text=f"Current Page: {currentPageAll + 1} / {len(globalLeaderboardsList)}")

        view = simpleViewAll(timeout=None)
        await interaction.followup.send(embed=embed, view=view)

    # Create the compare leaderboard positions command
    @app_commands.command(name="leaderboard-compare-positions", description="Compares the leaderboard positions of two players")
    async def comparePositions(self, interaction: discord.Interaction, player1: str, player2: str):
        """
        Args:
            player1 (str): A Minecraft username
            player2 (str): A Minecraft username
        """
        pass

        global leaderboardPositionPage
        global leaderboardPositionPages
        global globalLeaderboardsFormatedList

        leaderboardPositionPage = 0
        leaderboardPositionPages = []

        await interaction.response.defer()  # noqa

        player = player1.strip()
        player1 = player2.strip()
        data, data1 = await asyncio.gather(asyncio.to_thread(getInfo, f"{pit_functions.CLASSIC_API}/player/{player}"), asyncio.to_thread(getInfo, f"{pit_functions.CLASSIC_API}/player/{player1}"))

        if data.get("message", "") != "" or data1.get("message", "") != "":
            notFound = player if data.get("message", "") != "" else player1
            embedFail = discord.Embed(title=f"{notFound} not found", color=discord.Color.red())

            await interaction.followup.send(embed=embedFail)  # noqa

        else:
            playerData = data["data"]["player"]
            currentPrestige = playerData["prestige"]
            currentLevel = playerData["level"]
            uuid = playerData["uuid"].replace("-", "")

            playerData1 = data1["data"]["player"]
            currentPrestige1 = playerData1["prestige"]
            currentLevel1 = playerData1["level"]
            uuid1 = playerData1["uuid"].replace("-", "")

            leaderboardsFormatedList = globalLeaderboardsFormatedList
            playersRankings = []
            playersRankings1 = []

            allPositions = await getAllPositions([uuid, uuid1])
            rankingsFormatted = [positions.get(uuid, 999999) for positions in allPositions]
            rankingsFormatted1 = [positions.get(uuid1, 999999) for positions in allPositions]

            for i in range(0, len(rankingsFormatted)):
                playersRankings.append({leaderboardsFormatedList[i]: rankingsFormatted[i]})
                playersRankings1.append(rankingsFormatted1[i])
                # print(f"finished {leaderboardsFormatedList[i][leaderboardsFormatedList[i].index(' ') + 1:]}")
            sorted_leaderboards = sorted(playersRankings, key=lambda x: list(x.values())[0], reverse=False)

            signs = []
            for idx, leaderboard in enumerate(sorted_leaderboards, start=1):
                leaderboard_name, ranking = next(iter(leaderboard.items()))
                if ranking != 999999 and playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] != 999999:
                    if ranking > playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]:
                        signs.append('<')
                    elif ranking < playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]:
                        signs.append('>')
                    else:
                        signs.append('=')
                else:
                    signs.append('')

            count1 = signs.count('>')
            count2 = signs.count('<')
            leader = 0
            if count1 > count2:
                leader = 1
            else:
                leader = 2

            if leader == 1:
                embed = discord.Embed(title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {playerData['ign']} vs [{formatting_functions.int_to_roman(currentPrestige1)}{currentLevel1}] {playerData1['ign']}", color=calcBracketColor(currentPrestige))
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{uuid}?format=webp")
            else:
                embed = discord.Embed(title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {playerData['ign']} vs [{formatting_functions.int_to_roman(currentPrestige1)}{currentLevel1}] {playerData1['ign']}", color=calcBracketColor(currentPrestige1))
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{uuid1}?format=webp")

            i = 0
            for idx, leaderboard in enumerate(sorted_leaderboards, start=1):
                leaderboard_name, ranking = leaderboard.popitem()
                if i % 10 == 0 and i != 0:
                    leaderboardPositionPages.append(embed)
                    if leader == 1:
                        embed = discord.Embed(title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {playerData['ign']} vs [{formatting_functions.int_to_roman(currentPrestige1)}{currentLevel1}] {playerData1['ign']}", color=calcBracketColor(currentPrestige))
                        embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{uuid}?format=webp")
                    else:
                        embed = discord.Embed(title=f"Leaderboard positions for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {playerData['ign']} vs [{formatting_functions.int_to_roman(currentPrestige1)}{currentLevel1}] {playerData1['ign']}", color=calcBracketColor(currentPrestige1))
                        embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{uuid1}?format=webp")

                if ranking == 999999:
                    if playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 999999:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"N/A = N/A", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 1:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"N/A < :first_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 10:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"N/A < :second_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 100:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"N/A < :third_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    else:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"N/A < #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                elif ranking == 1:
                    if playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 999999:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":first_place: #{ranking} > N/A", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 1:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":first_place: #{ranking} {signs[i]} :first_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 10:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":first_place: #{ranking} {signs[i]} :second_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 100:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":first_place: #{ranking} {signs[i]} :third_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    else:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":first_place: #{ranking} {signs[i]} #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                elif ranking <= 10:
                    if playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 999999:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":second_place: #{ranking} > N/A", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 1:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":second_place: #{ranking} {signs[i]} :first_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 10:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":second_place: #{ranking} {signs[i]} :second_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 100:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":second_place: #{ranking} {signs[i]} :third_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    else:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":second_place: #{ranking} {signs[i]} #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                elif ranking <= 100:
                    if playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 999999:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":third_place: #{ranking} > N/A", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 1:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":third_place: #{ranking} {signs[i]} :first_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 10:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":third_place: #{ranking} {signs[i]} :second_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 100:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":third_place: #{ranking} {signs[i]} :third_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    else:
                        embed.add_field(name=f"{leaderboard_name}:", value=f":third_place: #{ranking} {signs[i]} #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                else:
                    if playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 999999:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking} > N/A", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] == 1:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking} {signs[i]} :first_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 10:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking} {signs[i]} :second_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    elif playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)] <= 100:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking} {signs[i]} :third_place: #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                    else:
                        embed.add_field(name=f"{leaderboard_name}:", value=f"#{ranking} {signs[i]} #{playersRankings1[globalLeaderboardsFormatedList.index(leaderboard_name)]}", inline=False)
                if i == len(sorted_leaderboards) - 1:
                    leaderboardPositionPages.append(embed)
                i += 1

            embed = leaderboardPositionPages[0]
            embed.set_footer(text=f"Current Page: {leaderboardPositionPage + 1} / {len(leaderboardPositionPages)}")
            view = simpleViewPositions(timeout=None)

            await interaction.followup.send(embed=embed, view=view)  # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(leaderboards(client))
