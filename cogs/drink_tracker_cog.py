import json
from typing import Any

import disnake
from disnake.ext import commands

class DrinkTrackerCog(commands.Cog):
    def __init__(self, bot: commands.InteractionBot, db: Any):
        self.bot = bot
        self.db = db

    @commands.slash_command(description="Order a drink.")
    @commands.cooldown(1, 60)
    async def order_drink(self, inter: disnake.ApplicationCommandInteraction):
        member_id = inter.author.id
        self.db.add_drink(member_id)
        await inter.response.send_message("Coming right up!")

    @commands.slash_command(description="See how many drinks you've ordered.")
    async def bill(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
        if member is None:
            member = inter.author
        
        num_drinks = self.db.get_num_drinks(member.id)
        await inter.response.send_message(f"**{member.display_name}** has ordered {num_drinks} drinks.")

    @commands.slash_command(description="See the number of drinks everyone has ordered.")
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction):
        stats = self.db.all()

        description = []
        for record in stats:
            member = inter.guild.get_member(record["member_id"])
            if member is not None:
                nickname = member.display_name
            else: # user probably left the server
                nickname = self.bot.get_user(record["member_id"]).name
            description.append(f"**{nickname}** - {record['drinks']}")
        
        embed = disnake.Embed(
            title="Drink Leaderboard",
            description="\n".join(description),
        )
        await inter.response.send_message(embed=embed)

    # for debugging/migration only
    @commands.slash_command(description="Dump drink stats to a message.")
    @commands.default_member_permissions(manage_guild=True)
    async def dump_stats(self, inter: disnake.ApplicationCommandInteraction):
        stats = self.db.all()
        await inter.response.send_message(json.dumps(stats))