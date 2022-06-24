from calendar import month
import discord
from discord.ext import commands
import discord
import asyncio
import random
import json
from datetime import date

class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DELAY = 0.8

        with open(r"data.json", "r") as f:
            self.coins = json.load(f)

        self.bot.loop.create_task(self.save_points())

        self.deck_list = {
            "2♣": 2,
            "2♦": 2,
            "2♥": 2,
            "2♠": 2,
            "3♣": 3,
            "3♦": 3,
            "3♥": 3,
            "3♠": 3,
            "4♣": 4,
            "4♦": 4,
            "4♥": 4,
            "4♠": 4,
            "5♣": 5,
            "5♦": 5,
            "5♥": 5,
            "5♠": 5,
            "6♣": 6,
            "6♦": 6,
            "6♥": 6,
            "6♠": 6,
            "7♣": 7,
            "7♦": 7,
            "7♥": 7,
            "7♠": 7,
            "8♣": 8,
            "8♦": 8,
            "8♥": 8,
            "8♠": 8,
            "9♣": 9,
            "9♦": 9,
            "9♥": 9,
            "9♠": 9,
            "10♣": 10,
            "10♦": 10,
            "10♥": 10,
            "10♠": 10,
            "J♣": 10,
            "J♦": 10,
            "J♥": 10,
            "J♠": 10,
            "Q♣": 10,
            "Q♦": 10,
            "Q♥": 10,
            "Q♠": 10,
            "K♣": 10,
            "K♦": 10,
            "K♥": 10,
            "K♠": 10,
            "A♣": 11,
            "A♦": 11,
            "A♥": 11,
            "A♠": 11,
        }

        self.HIT = "\U0001F1ED"
        self.STAND = "\U0001F1F8"

    # Auto Data Saving
    async def save_points(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"data.json", "w") as f:
                json.dump(self.coins, f, indent=4)

            await asyncio.sleep(0.3)
    
    # Auto Register User
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
         return
        if message.author.bot: return

        author_id = str(message.author.id)

        if not author_id in self.coins:
            self.coins[author_id] = {}
            self.coins[author_id]["coins"] = 0
            self.coins[author_id]["daily"] = ""
            self.coins[author_id]["monthly"] = ""
    
    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(title="Kidnapper Commands Menu")
        embed.add_field(name="Commands", value="`coins [member]` - Shows how many coins you or the member have.\n`daily` - Daily coins\n`monthly` - Monthly coins\n`hunt` - Hunt for animals in exchange for coins!\n`fish` - Go fishing in exchange for coins!\n`dig` - Digs for coins!\n `work` - Work for coins!\n`pet` - Pet yourself for coins!\n`mine` - Mine ores in exchange for coins!\n`kidnap` - Kidnap children in exchange for ransom!\n`blackjack <bet>` - Blackjack for coins\n`gamble <bet>` - Gambles for coins", inline=False)
        embed.add_field(name="Owner Commands", value="`givecoins <member> [amount]` - Gives members coins from the given amount\n`removecoins <member> [amount]` - Removes a members coins in the given amount\n`setcoins <member> [amount]` - Set a member's coins to the amount given\n`kill` - Kill members to reset their coins", inline=False)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["pts", "p"])
    async def coins(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)

        c = self.coins[member_id]["coins"]

        if member.id == ctx.author.id:
            await ctx.reply(f"You have **{c:,}** coins!")
        else:
            await ctx.reply(f"{member.mention} have **{c:,}** coins!")

    @commands.command()
    @commands.cooldown(1, 300, type=commands.BucketType.user)
    async def hunt(self, ctx):
        animals_small = ["Frog", "Squirrel", "Cow", "Bird", "Pig", "Chicken"]
        animals_big   = ["Elephant", "Tiger", "Boar", "Bear", "Lion", "Horse", "Zebra"]
        animtype      = random.randint(1,2)

        if animtype == 1: # big
            c = random.randint(50000, 100000)
            self.coins[str(ctx.author.id)]["coins"] += c
            await ctx.reply(f"You hunted an **{random.choice(animals_big)}** and got **{c:,}** coins!")

        if animtype == 2: # small
            c = random.randint(1000, 50000)
            self.coins[str(ctx.author.id)]["coins"] += c
            await ctx.reply(f"You hunted an **{random.choice(animals_small)}** and got **{c:,}** coins!")

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def fish(self, ctx):
        c = random.randint(100, 10000)
        self.coins[str(ctx.author.id)]["coins"] += c
        await ctx.reply(f"You went fishing and got **{c:,}** coins!")

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def dig(self, ctx):
        c = random.randint(50, 1000)
        self.coins[str(ctx.author.id)]["coins"] += c
        await ctx.reply(f"You went digging and got **{c:,}** coins!")

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def work(self, ctx):
        self.coins[str(ctx.author.id)]["coins"] += 10000
        await ctx.reply("You went to work and got **10,000** coins!")

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def pet(self, ctx):
        self.coins[str(ctx.author.id)]["coins"] += 1000
        await ctx.reply("You petted yourself and got **1,000** coins!")

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def mine(self, ctx):
        die_chance = random.randint(1, 100) # <2 = die

        if die_chance <= 3:
            c = self.coins[str(ctx.author.id)]["coins"]
            self.coins[str(ctx.author.id)]["coins"] -= c
            await ctx.reply(f"You went mining and died. You lost all of your coins.")
        
        else:
            c = random.randint(500, 1000)
            self.coins[str(ctx.author.id)]["coins"] += c
            await ctx.reply(f"You went mining and got **{c:,}** coins!")
        
    @commands.command()
    @commands.cooldown(1, 600, type=commands.BucketType.user)
    async def kidnap(self, ctx):
        arrest = random.randint(1, 50)

        if arrest != 25:
            c = self.coins[str(ctx.author.id)]["coins"]
            self.coins[str(ctx.author.id)]["coins"] -= c
            await ctx.reply(f"You kidnapped someone but you were caught by the police.")
        
        else:
            c = random.randint(100000, 500000)
            self.coins[str(ctx.author.id)]["coins"] += c
            await ctx.reply(f"You kidnapped a kid and got **{c:,}** coins as ransom!")

    @commands.command()
    async def daily(self, ctx):
        today = date.today()
        d2 = today.strftime("%d")
        if d2 != self.coins[str(ctx.author.id)]["daily"]:
            self.coins[str(ctx.author.id)]["daily"] = d2
            self.coins[str(ctx.author.id)]["coins"] += 15000
            await ctx.reply("Successfully claimed daily **15,000** points!")
        else:
            await ctx.reply("You currently cannot claim your daily. please try again tomorrow!")

    @commands.command()
    async def monthly(self, ctx):
        today = date.today()
        d2 = today.strftime("%B")
        if d2 != self.coins[str(ctx.author.id)]["monthly"]:
            self.coins[str(ctx.author.id)]["monthly"] = d2
            self.coins[str(ctx.author.id)]["coins"] += 100000
            await ctx.reply("Successfully claimed monthly **100,000** points!")
        else:
            await ctx.reply("You currently cannot claim your monthly. please try again next month!")

    @commands.command()
    async def givecoins(self, ctx, member : discord.Member = None, amount : int = None):
        if ctx.author.id != ctx.guild.owner.id:
            await ctx.reply("This command is server owner only.")
        else:
            member = ctx.author if not member else member
            member_id = str(member.id)
            
            if amount == None:
                await ctx.reply("Please add an amount you want to give to the user!")
                return

            self.coins[member_id]["coins"] += amount
            await ctx.reply(f"Gave **{amount:,}** coins to {member.mention}")
    
    @commands.command()
    async def removecoins(self, ctx, member : discord.Member = None, amount : int = None):
        if ctx.author.id != ctx.guild.owner.id:
            await ctx.reply("This command is server owner only.")
        else:
            member = ctx.author if not member else member
            member_id = str(member.id)
            
            if amount == None:
                await ctx.reply("Please add an amount you want to remove to the user!")
                return
                
            self.coins[member_id]["coins"] -= amount
            await ctx.reply(f"Removed **{amount:,}** coins to {member.mention}")
    
    @commands.command()
    async def setcoins(self, ctx, member : discord.Member = None, amount : int = None):
        if ctx.author.id != ctx.guild.owner.id:
            await ctx.reply("This command is server owner only.")
        else:
            member = ctx.author if not member else member
            member_id = str(member.id)
            
            if amount == None:
                await ctx.reply("Please add an amount you want to set to the user!")
                return

            self.coins[member_id]["coins"] = amount
            await ctx.reply(f"Set {member.mention}'s coins to **{amount:,}**")
    
    @commands.command()
    async def kill(self, ctx, member : discord.Member = None):
        if ctx.author.id != ctx.guild.owner.id:
            await ctx.reply("This command is server owner only.")
        if member == None:
            await ctx.reply("Please mention a user to kill!")
        else:
            member_id = str(member.id)

            self.coins[member_id]["coins"] -= self.coins[member_id]["coins"]
            await ctx.reply(f"Successfully killed {member.mention}! They no longer have coins.")

    @commands.command(pass_context=True, aliases=["bj"])
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def blackjack(self, ctx, bet : int = None):
        if bet == None:
            return await ctx.reply("Please place your bet!")
        
        if bet >= self.coins[str(ctx.author.id)]["coins"] + 1:
            return await ctx.reply("You cant bet higher than you currently have!")
            
        if not ctx.guild:
            return await ctx.channel.send(
                "> **Sneaky huh**"
            )

        self.player = []
        self.dealer = []

        self.deck = []
        for card in self.deck_list:
            self.deck.append(card)

        # Game setup
        self.setup_turn()
        self.embed = self.update_ui(ctx)
        self.stop_flag = False
        self.check_blackjack(ctx, bet=bet)
        self.msg = await ctx.channel.send(embed=self.embed)
        await self.msg.edit(embed=self.embed)

        await self.msg.add_reaction(self.HIT)
        await self.msg.add_reaction(self.STAND)

        self.hit_clicked = False
        self.stand_clicked = False

        def check_reaction(reaction, user):
            if str(reaction.emoji) == self.HIT:
                self.hit_clicked = True
                return user == ctx.author and str(reaction.message) == str(self.msg)
            elif str(reaction.emoji) == self.STAND:
                self.stand_clicked = True
                return user == ctx.author and str(reaction.message) == str(self.msg)

        # Game loop
        while True:
            if self.stop_flag:
                break

            try:
                reaction = await self.bot.wait_for(
                    "reaction_add", check=check_reaction, timeout=60.0
                )
            except asyncio.TimeoutError:
                reaction = self.stand_clicked = True
                await ctx.channel.send(
                    "You took too long, {0.author.mention}. Your frame was closed.".format(
                        ctx
                    )
                )

            if reaction and self.hit_clicked:
                self.hit_clicked = False

                self.get_card(self.player)
                self.embed = self.update_ui(ctx)
                await self.msg.edit(embed=self.embed)

                if self.check_edge(self.player):
                    self.coins[str(ctx.author.id)]["coins"] -= bet
                    self.embed = self.update_ui(ctx, "BUST", True)
                    await self.msg.edit(embed=self.embed)
                    break

                await self.msg.remove_reaction(self.HIT, ctx.author)

            elif reaction and self.stand_clicked:
                self.stand_clicked = False

                self.embed = self.update_ui(ctx, "Dealer's hand", True)
                await self.msg.edit(embed=self.embed)
                await asyncio.sleep(self.DELAY)

                while self.get_score(self.dealer) < 17:
                    self.get_card(self.dealer)
                    self.embed = self.update_ui(ctx, "Drawing...", True)
                    await self.msg.edit(embed=self.embed)
                    await asyncio.sleep(self.DELAY)

                if self.check_edge(self.dealer):
                    self.coins[str(ctx.author.id)]["coins"] += bet
                    self.embed = self.update_ui(ctx, "WIN", True)
                    await self.msg.edit(embed=self.embed)
                    break

                self.embed = self.update_ui(ctx, self.check_result(id=ctx.author.id, bet=bet), True)
                await self.msg.edit(embed=self.embed)
                break

    def get_card(self, user):
        card = random.choice(self.deck)
        user.append(card)
        self.deck.remove(card)
        return card

    def get_score(self, user, ra9=True):
        if not ra9:
            return str(self.deck_list.get(user[0]))

        deck_score = []
        for n in user:
            deck_score.append(self.deck_list.get(n))

        if sum(deck_score) > 21:
            for i, n in enumerate(deck_score):
                if deck_score[i] == 11:
                    deck_score[i] = 1

        return sum(deck_score)

    def show_cards(self, user, ra9=True):
        if ra9:
            return " ".join("`" + item + "`" for item in user)
        return "`" + user[0] + "` `?`"

    def update_ui(self, ctx_m, footer_m="Would you like\nto stand on it?", ra9=False):
        embed = discord.Embed(color=ctx_m.author.color)
        embed.set_author(name="Blackjack", icon_url=ctx_m.author.avatar)
        embed.set_footer(text=footer_m, icon_url=self.bot.user.avatar)
        embed.add_field(
            name="Your score: **" + str(self.get_score(self.player)) + "**",
            value=self.show_cards(self.player),
            inline=False,
        )
        embed.add_field(
            name="Dealer score: **" + str(self.get_score(self.dealer, ra9)) + "**",
            value=self.show_cards(self.dealer, ra9),
            inline=False,
        )
        return embed

    def setup_turn(self):
        self.get_card(self.player)
        self.get_card(self.dealer)
        self.get_card(self.player)
        self.get_card(self.dealer)

    def check_edge(self, user):
        if self.get_score(user) > 21:
            return True
        return False

    def check_result(self, id : int, bet : int):
        if (
            self.get_score(self.player) > self.get_score(self.dealer)
        ) and not self.check_edge(self.player):
            self.coins[str(id)]["coins"] += bet
            return "WIN"
        elif self.get_score(self.player) == self.get_score(self.dealer):
            return "PUSH"
        else:
            self.coins[str(id)]["coins"] -= bet
            return "LOSE"

    def check_blackjack(self, ctx_m, bet):
        if self.get_score(self.player, True) == 21:
            if self.get_score(self.dealer, True) == 21:
                self.embed = self.update_ui(ctx_m, "BLACKJACK\n PUSH", True)
                self.stop_flag = True
            else:
                self.embed = self.update_ui(ctx_m, "BLACKJACK\n WIN", True)
                self.stop_flag = True
        elif self.get_score(self.dealer, True) == 21:
            self.embed = self.update_ui(ctx_m, "BLACKJACK\n LOSE", True)
            self.stop_flag = True
        
    @commands.command()
    async def gamble(self, ctx, amount : int = None):
        author_id = str(ctx.author.id)
        ucoins = self.coins[author_id]["coins"]

        if amount >= 999:
            u_num = random.randint(1, 25)
            b_num = random.randint(15, 25)
        
        if amount >= 9999:
            u_num = random.randint(1, 20)
            b_num = random.randint(10, 20)
        
        if amount >= 99999:
            u_num = random.randint(1, 15)
            b_num = random.randint(5, 15)
        
        else:
            u_num = random.randint(1, 10)
            b_num = random.randint(5, 10)

        if amount == None:
            await ctx.reply("Please place your bet!")
            return

        if amount <= 99:
            await ctx.reply("You can't gamble below 100. try again!")
            return

        elif self.coins[author_id]["coins"] <= 99:
          await ctx.reply("You do not have enough coins! you need atleast 100 coins to gamble.")
          return

        elif self.coins[author_id]["coins"] >= 99:
            if u_num >= b_num:
                self.coins[author_id]["coins"] += amount
                nucoins = self.coins[author_id]["coins"]
                results = discord.Embed(title="Gambling Game", colour=0x01eff00)
                results.add_field(name="Results:", value=f"{ctx.author.name}: {u_num}\nKidnapper: {b_num}\n**You won! You now have {nucoins:,} coins!**", inline=False)

            if u_num <= b_num:
                self.coins[author_id]["coins"] -= amount
                nucoins = self.coins[author_id]["coins"]
                results = discord.Embed(title="Gambling Game", colour=0xff1100)
                results.add_field(name="Results:", value=f"{ctx.author.name}: {u_num}\nKidnapper: {b_num}\n**You lost. You now have {nucoins:,} coins!**", inline=False)      
      
            if u_num == b_num:
                self.coins[author_id]["coins"] -= amount
                results = discord.Embed(title="Gambling Game", colour=0xff1100)
                results.add_field(name="Results:", value=f"{ctx.author.name}: {u_num}\nKidnapper: {b_num}\n**It was a Tie! You did not won any coins.**", inline=False)

            await ctx.reply(embed=results)

async def setup(bot):
    await bot.add_cog(commands(bot))