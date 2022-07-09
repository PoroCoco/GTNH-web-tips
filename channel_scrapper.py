from readline import get_history_item
import discord
import json 
from config import PRIVATE_TOKEN

tips_channel_id = 995095207286669342
upvote_str_name = "👍"

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await update()


@client.event
async def on_message(message):
    if message.channel.id != tips_channel_id:
        return

    print("this needs to be added")
    print(message.content)
    return


async def update():
    tips = await get_history() 
    with open('json_tips.json', 'w') as outfile:
        outfile.write(tips)


async def get_history():
    channel = client.get_channel(tips_channel_id)
    messages = await channel.history(limit=None).flatten()
    tips =[]

    for message in messages:
        json_tip = tip_to_json(message)
        if json_tip != None:
            tips.append(json_tip)
    return json.dumps(tips)

def tip_to_json(message):
    tip = {
        "UserName" : "",
        "Upvotes" : 0,
        "Categories" : [],
        "Tiers" : [],
        "Content" : ""
    }

    if type(message.author) == discord.Member :
        tip["UserName"] = message.author.nick
    else:
        tip["UserName"] = message.author.name

    for react in message.reactions:
        emoji = react.emoji
        emoji_name= ""

        if type(emoji) == str:
            emoji_name = emoji
        else:
            emoji_name = emoji.name

        if emoji_name == upvote_str_name:
            tip["Upvotes"] = react.count

    parts = message.content.split("\n")

    #if the message doesn't respect the template 
    if len(parts) < 3:
        return 

    #get the items after "Category:"
    categories = parts[0].split(":")[1]
    #splits the items on ',' and '/'
    categories.replace(",","@").replace("/","@").split("@")

    if type(categories) == str :
        tip["Categories"].append(categories.strip().lower())
    else:
        for category in categories:
            tip["Categories"].append(category.strip().lower())


    tier = parts[1].split(":")[1]
    tip["Tiers"] = tier.strip().lower()

    tip["Content"] = parts[2]

    return json.dumps(tip)



client.run(PRIVATE_TOKEN)
