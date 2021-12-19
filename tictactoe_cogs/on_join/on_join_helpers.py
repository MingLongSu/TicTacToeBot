import json

# adds a new guild to the database of guilds the bot has been added to
def add_guild(guild_id, guild_owner):
    # fetching data for all guilds
    with open('./data/all_guilds.json', 'r') as file:
        all_guild_data=json.load(file)

    # checking if there is data for the currrently passed guild_id
    if guild_id not in all_guild_data:
        all_guild_data[f'{ guild_id }']={}
        all_guild_data[f'{ guild_id }']['owner_id']=guild_owner
        all_guild_data[f'{ guild_id }']['ttt_channel']=None

    # updating the json with the new guild added
    with open('./data/all_guilds.json', 'w') as file:
        json.dump(all_guild_data, file, indent=len(all_guild_data[f'{ guild_id }']))

