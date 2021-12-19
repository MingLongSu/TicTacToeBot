import json

# retrieves data for all guilds
def get_all_guilds(): 
    with open('./data/all_guilds.json', 'r') as file:
        all_guild_data=json.load(file)

    return all_guild_data

# writes back to the file to save changes
def overwrite_all_guilds(all_guild_data_updated):
    with open('./data/all_guilds.json', 'w') as file:
        json.dump(all_guild_data_updated, file, indent=len(all_guild_data_updated))