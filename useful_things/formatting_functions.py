import re


# Add commas to a given number
def add_commas(number):
    return "{:,}".format(number)


# Convert an int into its roman numeral form
def int_to_roman(num):
    if num == 0:
        return ""

    if not (1 <= num <= 50):
        raise ValueError("Number out of range, must be between 1 and 50")

    val = [
        50, 40, 10, 9, 5, 4, 1
    ]
    syb = [
        "L", "XL", "X", "IX", "V", "IV", "I"
    ]

    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num + "-"


# Get a player's current level given their formatted prestige and level string
def extract_substring(input_string):
    hyphen_pos = input_string.find('-')

    if hyphen_pos == -1:
        return None

    start_pos = hyphen_pos + 5
    if start_pos >= len(input_string):
        return None

    end_pos = input_string.find('§', start_pos)
    if end_pos == -1:
        return None

    result = input_string[start_pos:end_pos]
    return result


# Convert a playtime in minutes int into a formatted string that can include months and days
def format_playtime(playtime_minutes):
    MINUTES_IN_HOUR = 60
    HOURS_IN_DAY = 24
    DAYS_IN_MONTH = 30

    total_hours = playtime_minutes / MINUTES_IN_HOUR

    if total_hours < HOURS_IN_DAY:
        return f"{total_hours:.0f} hr"
    elif total_hours < HOURS_IN_DAY * DAYS_IN_MONTH:
        days = int(total_hours // HOURS_IN_DAY)
        hours = total_hours % HOURS_IN_DAY
        return f"{days} d, {hours:.0f} hr"
    else:
        total_days = total_hours / HOURS_IN_DAY
        months = int(total_days // DAYS_IN_MONTH)
        days = total_days % DAYS_IN_MONTH
        return f"{months} mo, {days:.0f} d"


# Get a player's name from their formatted nametag
def extract_name(input_string):
    last_index = input_string.rfind(' ')

    if last_index != -1:
        name = input_string[last_index + 3:]
        return name
    else:
        return None


# Format a player's ranking data and remove and unwanted ranking data
def formatRankingsData(listToFormat):
    blackListed = ['damageRatio', 'highestStreak', 'kdr', 'tierOnes', 'tierTwos', 'darkPantsT2', 'totalJumps', 'bounty', 'genesisPoints', 'joins', 'bowAccuracy', 'swordHits', 'meleeDamageDealt', 'meleeDamageReceived', 'meleeDamageRatio', 'bowDamageDealt', 'bowDamageReceived', 'bowDamageRatio', 'xpHourly', 'goldHourly', 'killsHourly', 'kadr', 'killAssistHourly', 'contractsStarted', 'contractsRatio', 'ingotsGold']

    return [value if key in blackListed else (value if isinstance(value, (int, float)) else 999999) for key, value in listToFormat.items() if key not in blackListed]


def leaderboardEmbed(players, embed, page):
    i = 1
    for player in players:
        embed.add_field(name=f"#{page * 10 + i}:", value=f"{player}", inline=False)
        i += 1
    return embed


def leaderboardEmbedAll(players, embed):
    i = 1
    for player in players:
        embed.add_field(name=f"#{i}:", value=f"{player}", inline=False)
        i += 1
    return embed
