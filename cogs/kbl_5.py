# --- DATES IN SECONDS --- #
# OCTOBER 1   - 1696089600 # --- DONE ---
# NOVEMBER 1  - 1698768000 #
# DECEMBER 1  - 1701360000 #
# JANUARY 1   - 1704038400 #
# FEBRUARY 1  - 1706716800 #
# MARCH 1     - 1709222400 #
# APRIL 1     - 1711900800 #
# ------------------------ #

import time, datetime, pytz
from disnake import Embed, Member
from disnake.ext import commands, tasks
from mizuki.db import db
from properties.misc_1 import LeaderboardPages

class kbl_5(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.monthly_awards.start()
	
	@tasks.loop(seconds=1)
	async def monthly_awards(self):
		monthly_time = db.field("SELECT MEA FROM global")
		if int(time.time()) > monthly_time:
			manila_time = pytz.timezone("Asia/Manila")
			date_now = datetime.datetime.now(manila_time)
			month_now = date_now.strftime("%B")
			channel = await self.client.fetch_channel(961504020508340294)
			top_members = db.records("SELECT UserID, BonusCoins FROM main ORDER BY BonusCoins DESC")
			diamond = f"<:diamond_trophy:1135933219670339664> • <@!{top_members[0][0]}>: **{top_members[0][1]} SP**"
			platinum = f"<:platinum_trophy:1135933215761244310> • <@!{top_members[1][0]}>: **{top_members[1][1]} SP**"
			gold = "\n".join([f"<:golden_trophy:1094533382395920444> • <@!{top_members[i][0]}>: **{top_members[i][1]} SP**" for i, j in enumerate(top_members[2:10], 3)])
			silver = "\n".join([f"<:silver_trophy:1094533380458156112> • <@!{top_members[i][0]}>: **{top_members[i][1]} SP**" for i, j in enumerate(top_members[10:20], 11)])
			bronze = "\n".join([f"<:bronze_trophy:1094533376096075897> • <@!{top_members[i][0]}>: **{top_members[i][1]} SP**" for i, j in enumerate(top_members[20:30], 21)])
			db.execute("UPDATE trophies SET Diamond = Diamond + 1 WHERE UserID = ?", top_members[0][0])
			db.execute("UPDATE trophies SET Platinum = Platinum + 1 WHERE UserID = ?", top_members[1][0])
			for i in range(2):
				db.execute("UPDATE main SET SPBonus = 0.5, SPBonusTime = ? WHERE UserID = ?", int(time.time())+432000, top_members[i][0])
			for i in range(2, 10):
				db.execute("UPDATE trophies SET Gold = Gold + 1 WHERE UserID = ?", top_members[i][0])
				db.execute("UPDATE main SET SPBonus = 0.4, SPBonusTime = ? WHERE UserID = ?", int(time.time())+345600, top_members[i][0])
			for i in range(10, 20):
				db.execute("UPDATE trophies SET Silver = Silver + 1 WHERE UserID = ?", top_members[i][0])
				db.execute("UPDATE main SET SPBonus = 0.3, SPBonusTime = ? WHERE UserID = ?", int(time.time())+259200, top_members[i][0])
			for i in range(20, 30):
				db.execute("UPDATE trophies SET Bronze = Bronze + 1 WHERE UserID = ?", top_members[i][0])
				db.execute("UPDATE main SET SPBonus = 0.3, SPBonusTime = ? WHERE UserID = ?", int(time.time())+259200, top_members[i][0])
			db.execute("UPDATE global SET MEA = 1698768000")
			embed0 = Embed(color=0x2f3136, title=f"Meme Excellence Awards ({month_now})", description=f"{diamond}\n{platinum}\n{gold}")
			embed1 = Embed(color=0x2f3136, title=f"Meme Excellence Awards ({month_now})", description=f"{silver}")
			embed2 = Embed(color=0x2f3136, title=f"Meme Excellence Awards ({month_now})", description=f"{bronze}").set_footer(text="Your SP will be reset to 0. Keep grinding to reach higher score!")
			await channel.send(content="Congratulations on the **Top 30** meme posters of the month! Continue grinding your points to be recognized in the next awarding <t:1698768000:R>", embeds=[embed0, embed1, embed2])
		sp_expired_reward = db.column("SELECT UserID FROM main WHERE SPBonusTime < ? AND SPBonusTime != 0", int(time.time()))
		if len(sp_expired_reward) > 0:
			for member in sp_expired_reward:
				db.execute("UPDATE main SET SPBonusTime = 0, SPBonus = 0 WHERE UserID = ?", member)

	@commands.Cog.listener()
	async def on_ready(self):
		print("KBL (Part 5) is loaded.")

	@commands.command(aliases=["tro", "c"])
	async def trophy(self, ctx, user: Member = None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		user = user or ctx.author
		diamond, platinum, gold, silver, bronze = db.record("SELECT Diamond, Platinum, Gold, Silver, Bronze FROM trophies WHERE UserID = ?", user.id)
		embed=Embed(color=0x2f3136, title=f"{user}'s Trophy Collection").set_footer(text="Collect trophies by being in the Top 30 SP Leaderboards.\nThe higher your position, the greater the rewards!", icon_url=user.guild.icon)
		embed.add_field(name="\u200b", value=f"<:diamond_trophy:1135933219670339664> • **{diamond}**").add_field(name="\u200b", value=f"<:platinum_trophy:1135933215761244310> • **{platinum}**")
		embed.add_field(name="\u200b", value=f"<:golden_trophy:1094533382395920444> • **{gold}**").add_field(name="\u200b", value=f"<:silver_trophy:1094533380458156112> • **{silver}**")
		embed.add_field(name="\u200b", value=f"<:bronze_trophy:1094533376096075897> • **{bronze}**").add_field(name="\u200b", value="\u200b")
		await ctx.send(embed=embed)

	@commands.command(aliases=["sp"])
	async def solidpoints(self, ctx, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if suffix is None:
			lb = db.records("SELECT UserID, MonthlyBonusPoints FROM main ORDER BY MonthlyBonusPoints DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY MonthlyBonusPoints DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Solid Points (Monthly)", users=lb_, client=self.client)
			await paginator.start()
		elif suffix in ["--all-time", "--yearly", "--annual", "--y"]:
			lb = db.records("SELECT UserID, BonusCoins FROM main ORDER BY BonusCoins DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY BonusCoins DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Solid Points (Yearly)", users=lb_, client=self.client)
			await paginator.start()
		elif suffix in ["--monthly", "--m"]:
			lb = db.records("SELECT UserID, MonthlyBonusPoints FROM main ORDER BY MonthlyBonusPoints DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY MonthlyBonusPoints DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Solid Points (Monthly)", users=lb_, client=self.client)
			await paginator.start()
		else:
			lb = db.records("SELECT UserID, MonthlyBonusPoints FROM main ORDER BY MonthlyBonusPoints DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY MonthlyBonusPoints DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Solid Points (Monthly)", users=lb_, client=self.client)
			await paginator.start()

def setup(client):
	client.add_cog(kbl_5(client))