import discord
from discord.ext import commands
import datetime

class handlers(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            
        @commands.Cog.listener()
        async def on_command_error(self, ctx, error):
            if isinstance(error, commands.CommandNotFound):
                return
            
            if isinstance(error, commands.UserInputError):
                return

            if isinstance(error, commands.CommandOnCooldown):
                m, s = divmod(error.retry_after, 60)
                h, m = divmod(m, 60)
                if int(h) == 0 and int(m) == 0:
                    await ctx.send(f"This command is currently on cooldown. Please try the command again in **{int(s)}** seconds.")
                elif int(h) == 0 and int(m) != 0:
                    await ctx.send(f"This command is currently on cooldown. Please try the command again in **{int(m)}** minutes and **{int(s)}** seconds.")
                else:
                    await ctx.send(f"This command is currently on cooldown. Please try the command again in **{int(h)}** hours, **{int(m)}** minutes and **{int(s)}** seconds.")
                    
            elif isinstance(error, commands.CheckFailure):
                perms = "str".join(error.missing_perms)
                embed = discord.Embed(title='🚫 Error', description=f'You do not have any permissions to do that!\nRequired Perms: ``{perms}``')
                await ctx.send(embed=embed)
            raise error

async def setup(bot):
    await bot.add_cog(handlers(bot))