import nextcord, tomllib
from nextcord.ext import commands

class SafeDict(dict):
    def __missing__(self, key):
        return f"{{{key}}}"

class On_Member_Join(commands.Cog):
    def __init__(self,client):
        self.client = client

    with open("config.toml", "rb") as config_file:
        config = tomllib.load(config_file)

    WELCOME = config["welcome"]["enabled"]
    WELCOME_CHANNEL = config["welcome"]["channel_id"]
    WELCOME_TITLE = config["welcome"]["message_title"]
    WELCOME_DESCRIPTION = config["welcome"]["message_description"]
    WELCOME_COLOR = config["welcome"]["embed_color"].strip("#")

    @commands.Cog.listener()
    async def on_member_join(self,member: nextcord.Member):
        if not self.WELCOME:
            return

        guild = member.guild
        placeholders = SafeDict({
            "member_mention": member.mention,
            "member_name": member.name,
            "member_id": str(member.id),
            "guild_name": guild.name,
            "guild_count": str(guild.member_count)
        })

        channel = self.client.get_channel(int(self.WELCOME_CHANNEL)) or await self.client.fetch_channel(int(self.WELCOME_CHANNEL))
        if not channel:
            return

        formatted_title = self.WELCOME_TITLE.format_map(placeholders)
        formatted_description = self.WELCOME_DESCRIPTION.format_map(placeholders)

        emb = nextcord.Embed(
            title=formatted_title,
            description=formatted_description,
            color=int(self.WELCOME_COLOR, 16)
        )
        
        emb.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=emb)

def setup(client):
    client.add_cog(On_Member_Join(client))
