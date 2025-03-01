import time, datetime, pytz
from disnake import Embed, Member
from disnake.ext import commands, tasks
from kbl.db import db

from properties.funcs import LeaderboardPages, last_day


"""

	Please check IMPORTANT.md for the layout and descriptions of other commands. Some are very simple, and some are complex.
	For existing errors, check ERRORS.md.
	For overall and general information about this project, database schema, and more, check README.md.

	Goodluck to those who will use this once-so-called 'masterpiece' for their discord server.

	Sincerely,
		raianxh_

		
	PS: Monthly awards are all catered to KBL Discord Server. If you wish to use this in your own server, you need to tweak it a little and replace some objects with your own.
		You must be fluent to read Python and Discord Developer. Otherwise, feel free to remove/comment it.

	PPS: For current issues relating to this, check ERRORS.md.

"""


class monthly_awards(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.monthly_awards.start()
	
	@tasks.loop(seconds=1)
	async def monthly_awards(self):
		monthly_time = await db.field("SELECT MMA FROM global")
		if int(time.time()) > monthly_time:
			manila_time = pytz.timezone("Asia/Manila")
			date_now = datetime.datetime.now(manila_time)
			month_now = date_now.strftime("%B")
			channel = await self.client.fetch_channel(961504020508340294)
			top_members = await db.records("SELECT UserID, MonthlySP FROM main ORDER BY MonthlySP DESC")
			diamond = f"<:diamond_trophy:1135933219670339664> • <@!{top_members[0][0]}>: **{top_members[0][1]} SP**"
			platinum = "\n".join([f"<:platinum_trophy:1135933215761244310> • <@!{top_members[i][0]}>: **{top_members[i][1]} SP**" for i, j in enumerate(top_members[1:3], 2)])
			gold = "\n".join([f"<:golden_trophy:1094533382395920444> • <@!{top_members[i][0]}>: **{top_members[i][1]} SP**" for i, j in enumerate(top_members[3:10], 4)])
			silver = "\n".join([f"<:silver_trophy:1094533380458156112> • <@!{top_members[i][0]}>: **{top_members[i][1]} SP**" for i, j in enumerate(top_members[10:20], 11)])
			bronze = "\n".join([f"<:bronze_trophy:1094533376096075897> • <@!{top_members[i][0]}>: **{top_members[i][1]} SP**" for i, j in enumerate(top_members[20:30], 21)])
			await db.execute("UPDATE main SET Diamond = Diamond + 1 WHERE UserID = %s", top_members[0][0])
			
			for i in range(2):
				await db.execute("UPDATE main SET SPBonus = 0.5, SPBonusTime = %s WHERE UserID = %s", int(time.time())+432000, top_members[i][0])
			for i in range(1, 3):
				await db.execute("UPDATE main SET Platinum = Platinum + 1 WHERE UserID = %s", top_members[i][0])
			for i in range(3, 10):
				await db.execute("UPDATE main SET Gold = Gold + 1 WHERE UserID = %s", top_members[i][0])
				await db.execute("UPDATE main SET SPBonus = 0.4, SPBonusTime = %s WHERE UserID = %s", int(time.time())+345600, top_members[i][0])
			for i in range(10, 20):
				await db.execute("UPDATE main SET Silver = Silver + 1 WHERE UserID = %s", top_members[i][0])
				await db.execute("UPDATE main SET SPBonus = 0.3, SPBonusTime = %s WHERE UserID = %s", int(time.time())+259200, top_members[i][0])
			for i in range(20, 30):
				await db.execute("UPDATE main SET Bronze = Bronze + 1 WHERE UserID = %s", top_members[i][0])
				await db.execute("UPDATE main SET SPBonus = 0.3, SPBonusTime = %s WHERE UserID = %s", int(time.time())+259200, top_members[i][0])
			for i in range(len(top_members) - 1):
				await db.execute("UPDATE main SET TotalSP = TotalSP + %s, MonthlySP = 0 WHERE UserID = %s", top_members[i][1], top_members[i][0])
			
			ldotm = last_day(date_now.year, date_now.month)
			last_day_current = datetime.datetime.combine(ldotm, datetime.time(20, 0, 0))
			datetime_current = manila_time.localize(last_day_current).timestamp()
			await db.execute("UPDATE global SET MMA = %s", int(datetime_current))
			embed0 = Embed(color=0x2f3136, title=f"Monthly Meme Awards ({month_now})", description=f"{diamond}\n{platinum}\n{gold}")
			embed1 = Embed(color=0x2f3136, title=f"Monthly Meme Awards ({month_now})", description=f"{silver}")
			embed2 = Embed(color=0x2f3136, title=f"Monthly Meme Awards ({month_now})", description=f"{bronze}").set_footer(text="Your SP will be reset to 0. Keep grinding to reach higher score!")
			await channel.send(content=f"Congratulations on the **Top 30** meme posters of the month (<:diamond_trophy:1135933219670339664> <@{top_members[0][0]}>)! Continue grinding your points to be recognized in the next awarding <t:{int(datetime_current)}:R>", embeds=[embed0, embed1, embed2])
			sp_expired_reward = await db.column("SELECT UserID FROM main WHERE SPBonusTime < %s AND SPBonusTime != 0", int(time.time()))
			if len(sp_expired_reward) > 0:
				for member in sp_expired_reward:
					await db.execute("UPDATE main SET SPBonusTime = 0, SPBonus = 0 WHERE UserID = %s", member)

	@commands.Cog.listener()
	async def on_ready(self):
		print("KBL (Part 5) is loaded.")

	@commands.command(aliases=["tro", "c"])
	async def trophy(self, ctx, user: Member = None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		user = user or ctx.author
		diamond, platinum, gold, silver, bronze = await db.record("SELECT Diamond, Platinum, Gold, Silver, Bronze FROM main WHERE UserID = %s", user.id)
		embed=Embed(color=0x2f3136, title=f"{user}'s Trophy Collection").set_footer(text="Collect trophies by being in the Top 30 SP Leaderboards.\nThe higher your position, the greater the rewards!", icon_url=user.guild.icon)
		embed.add_field(name="\u200b", value=f"<:diamond_trophy:1135933219670339664> • **{diamond}**").add_field(name="\u200b", value=f"<:platinum_trophy:1135933215761244310> • **{platinum}**")
		embed.add_field(name="\u200b", value=f"<:golden_trophy:1094533382395920444> • **{gold}**").add_field(name="\u200b", value=f"<:silver_trophy:1094533380458156112> • **{silver}**")
		embed.add_field(name="\u200b", value=f"<:bronze_trophy:1094533376096075897> • **{bronze}**").add_field(name="\u200b", value="\u200b")
		await ctx.send(embed=embed)

	@commands.command(aliases=["sp"])
	async def solidpoints(self, ctx, suffix=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if suffix is None:
			lb = await db.records("SELECT UserID, MonthlySP FROM main ORDER BY MonthlySP DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY MonthlySP DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Solid Points (Monthly)", users=lb_, client=self.client)
			await paginator.start()
		elif suffix in ["--all-time", "--yearly", "--annual", "--y"]:
			lb = await db.records("SELECT UserID, TotalSP FROM main ORDER BY TotalSP DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY TotalSP DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Solid Points (Yearly)", users=lb_, client=self.client)
			await paginator.start()
		elif suffix in ["--monthly", "--m"]:
			lb = await db.records("SELECT UserID, MonthlySP FROM main ORDER BY MonthlySP DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY MonthlySP DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Solid Points (Monthly)", users=lb_, client=self.client)
			await paginator.start()
		else:
			lb = await db.records("SELECT UserID, MonthlySP FROM main ORDER BY MonthlySP DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY MonthlySP DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Solid Points (Monthly)", users=lb_, client=self.client)
			await paginator.start()

def setup(client):
	client.add_cog(monthly_awards(client))