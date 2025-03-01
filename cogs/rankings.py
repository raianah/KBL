from disnake.ext import commands
from disnake import Embed, Member, File, CustomActivity
from disnake.ui import View, Button
from typing import Union
from kbl.db import db
from millify import millify
from easy_pil import Editor, load_image_async, Font

from properties.funcs import ShopView, RankSettings, LeaderboardPages, bannerchoice, check_status


"""

	Please check IMPORTANT.md for the layout and descriptions of other commands. Some are very simple, and some are complex.
	For existing errors, check ERRORS.md.
	For overall and general information about this project, database schema, and more, check README.md.

	Goodluck to those who will use this once-so-called 'masterpiece' for their discord server.

	Sincerely,
		raianxh_

		
	PS: All commands here are all catered to KBL Discord Server. If you wish to use this in your own server, you need to tweak it a little and replace some objects with your own.
		You must be fluent to read Python and Discord Developer. Otherwise, feel free to remove/comment it.

	PPS: Shop & Ranksettings are currently disabled due to recent deletion of assets.

"""


class rankings(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("KBL (Rankings) is loaded.")

	@commands.command(aliases=['stats', 'statistic', 'stat', 'st'])
	async def statistics(self, ctx, member: Union[Member, str]=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		else:
			if member is None:
				member = ctx.author
				points, solidpoints, ligtaspoints, messages = await db.record("SELECT Coins, MonthlySP, LigtasPoints, Messages FROM main WHERE UserID = %s", member.id)
				users, b_users, lp_lb, msg_lb, lb0 = await db.column("SELECT UserID FROM main ORDER BY Coins DESC"), await db.column("SELECT UserID FROM main ORDER BY MonthlySP DESC"), await db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC"), await db.column("SELECT UserID FROM main ORDER BY Messages DESC"), await db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
				lpn_rank, lpn_xp, lpn_limit = await db.record("SELECT GeneralLevel, GeneralXP, GenLevelLimit FROM main WHERE UserID = %s", member.id)
				voter = "Disabled"
				embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
				embed.set_footer(text=f"Showing {member.name}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
				await ctx.send(embed=embed)
			elif isinstance(member, Member):
				member = member or ctx.author
				points, solidpoints, ligtaspoints, messages = await db.record("SELECT Coins, MonthlySP, LigtasPoints, Messages FROM main WHERE UserID = %s", member.id)
				users, b_users, lp_lb, msg_lb, lb0 = await db.column("SELECT UserID FROM main ORDER BY Coins DESC"), await db.column("SELECT UserID FROM main ORDER BY MonthlySP DESC"), await db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC"), await db.column("SELECT UserID FROM main ORDER BY Messages DESC"), await db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
				lpn_rank, lpn_xp, lpn_limit = await db.record("SELECT GeneralLevel, GeneralXP, GenLevelLimit FROM main WHERE UserID = %s", member.id)
				voter = "Disabled"
				embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
				embed.set_footer(text=f"Showing {member.name}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
				await ctx.send(embed=embed)
			elif isinstance(member, str):
				if member.lower() in ["--description", "--desc", "--d"]:
					embed=Embed(color=0x2f3136, title="Ranking Description").set_footer(text=f"Showing the basics of ranking in KBL", icon_url=ctx.author.display_avatar).set_thumbnail(url=ctx.guild.icon)
					embed.description = "**__Balance__**\n- <:money_icon:1075986284461445140> **Pera** is a type of currency in KBL that can be obtained by chatting in all **__Lipunan__** categories. Your pera will be added automatically per message (cooldown per message are being observed).\n- You can spend <:money_icon:1075986284461445140> **Pera** via `.shop`.\n  - You can also earn <:money_icon:1075986284461445140> **Pera** by collecting **Solid Points**, a point-based score that can be obtained by posting memes on <#961504020508340294>. The higher your current Solid Points, the higher the amount of your <:money_icon:1075986284461445140> **Pera** per message.\n- **Ligtas Points**, or LP, are another type of points that can only be occurred via thanking the user. It can be in a form of mention, or replied message. By this members will be filtered on who is the most helpful in the server. Don't forget to track users with the highest LP via `.leaderboard --lp` to show who's the most helpful.\n\n**__Rankings__**\n- Rankings are a way to engage more members on a server. By participating in various categories (Lapagan & Lipunan), you will be granted XP which levels up if you reached certain XP threshold per level.\n- In <#961504020508340294>, reaching at least top 30 will grant you a trophy that can be displayed on your rank card, or via `.trophy`.\n  - XP & Level from Lapagan & Lipunan categories are different, and won't conflict one from another.\n  - Leveling up also grants roles that changes as your level goes further."
					await ctx.send(embed=embed)
				else:
					await ctx.send("Available suffixes: `--description`, `--desc`, `--d`\n\nUsage: `.statistics --desc`")
			else:
				member = member or ctx.author
				points, solidpoints, ligtaspoints, messages = await db.record("SELECT Coins, MonthlySP, LigtasPoints, Messages FROM main WHERE UserID = %s", member.id)
				users, b_users, lp_lb, msg_lb, lb0 = await db.column("SELECT UserID FROM main ORDER BY Coins DESC"), await db.column("SELECT UserID FROM main ORDER BY MonthlySP DESC"), await db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC"), await db.column("SELECT UserID FROM main ORDER BY Messages DESC"), await db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
				lpn_rank, lpn_xp, lpn_limit = await db.record("SELECT GeneralLevel, GeneralXP, GenLevelLimit FROM main WHERE UserID = %s", member.id)
				voter = "Disabled"
				embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
				embed.set_footer(text=f"Showing {member.name}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
				await ctx.send(embed=embed)

	@commands.command(aliases=["level", "lvl"])
	async def rank(self, ctx, member: Union[Member, str]=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		else:
			if member is None:
				member = ctx.author
			elif type(member) == Member:
				if member.bot:
					return await ctx.send(f"{member.mention} is tagged as a bot. Overall bots don't gain XP nor gain level from this leveling.")
			activity = None
			for act in member.activities:
				if isinstance(act, CustomActivity):
					try:
						activity = f"{act.name}"
						break
					except:
						pass
				# if isinstance(act, Game):
				# 	pass
				# if isinstance(act, Streaming):
				# 	pass
				# if isinstance(act, Spotify):
				# 	pass
			if activity == None:
				activity = "-"
			elif len(activity) > 30:
				activity = activity.replace(activity[30:], "...")
			async with ctx.typing():
				# dt = datetime.datetime.now().weekday()
				# if dt in [4, 5, 6]:
				# 	sp = 5
				# else:
				# 	sp = 3
				view = View()
				button = Button(label=f"Voting disabled", url="https://top.gg/servers/961502956195303494/vote", disabled=True)
				view.add_item(button)
				gen_lvl, gen_xp, gen_lvl_limit = await db.record("SELECT GeneralLevel, GeneralXP, GenLevelLimit FROM main WHERE UserID = %s", member.id)
				points, msgs, bonus_coins = await db.record("SELECT Coins, Messages, MonthlySP FROM main WHERE UserID = %s", member.id)
				banner_choice, textbg, polybg, outlinebg = await db.record("SELECT BannerChoice, TextBG, PolyBG, OutlineBG FROM main WHERE UserID = %s", member.id)
				profile_banner = bannerchoice(banner_choice)
				lb = await db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
				percentage = int(((gen_xp * 100) / gen_lvl_limit))
				if percentage < 1:
					percentage = 0
				
				# --- INITIALIZING IMAGES --- #
				username = member.name.replace(member.name[15:], "...") if len(member.name) > 15 else member.name
				nickname = member.display_name.replace(member.display_name[15:], "...") if len(member.display_name) > 15 else member.display_name
				
				image = Editor("./properties/assets/kbl_podcast_bg.png").resize((1920, 1080), crop=True).blur(amount=7).rounded_corners()
				if member.avatar is None:
					profile, avatar = await load_image_async(str(member.display_avatar.url)), await load_image_async(str(member.display_avatar.url))
				else:
					profile, avatar = await load_image_async(str(member.avatar.url)), await load_image_async(str(member.display_avatar.url))
				
				profile_, avatar_ = Editor(profile).resize((342, 342)).circle_image(), Editor(avatar).resize((55, 55)).circle_image()
				profile_banner = Editor("./properties/assets/cyber_banner.png").resize((464, 1010))
				stats_icon, message_icon = Editor("./properties/assets/stats_icon.png").resize((80, 56)), Editor("./properties/assets/message_icon.png").resize((64, 54), crop=True)
				money_icon = Editor("./properties/assets/money_icon.png").resize((85, 64))
				status_icon, status = check_status(str(member.status))
				font, font1 = Font.montserrat(variant="bold", size=60), Font.montserrat(variant="bold", size=50)
				font2, font3 = Font.montserrat(variant="bold", size=104), Font.montserrat(variant="bold", size=47)
				font4, font5 = Font.montserrat(variant="bold", size=51), Font.montserrat(variant="bold", size=46)
				image.paste(profile_banner.image, (53, 0))
				image.paste(profile_.image, (120, 90))
				image.paste(avatar_.image, (619, 167))
				image.paste(stats_icon.image, (165, 471))
				image.paste(message_icon.image, (174, 555))
				image.paste(money_icon.image, (1415, 399))
				image.paste(status_icon.image, (619, 403))
				image.ellipse((200, 666), width=167, height=167, outline=polybg, stroke_width=15)
				image.ellipse((120, 90), width=342, height=342, outline="#0000ff", stroke_width=10)
				image.rectangle((585, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((919, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((1252, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((1585, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((603, 239), width=1259, height=137, outline=outlinebg, stroke_width=15, fill=polybg, radius=90)
				if percentage > 0:
					image.bar((603, 239), max_width=588, height=137, percentage=percentage, fill=outlinebg, radius=90)
				
				# --- APPLYING TEXT --- #
				image.text_stroke((655, 280), text=f"{millify(gen_xp, precision=2)} / {millify(gen_lvl_limit, precision=2)} (Level {gen_lvl})", font=font, stroke_width=4, stroke_fill="#000000", color=textbg, align="left")
				image.text((691, 175), text=f"{username}", font=font1, color=textbg, align="left")
				image.text((620, 48), text=f"{nickname}", font=font2, color=textbg, align="left")
				image.text((676, 403), text=f"{status}", font=font3, color=textbg, align="left")
				image.text((676, 484), text=f"{activity}", font=font3, color=textbg, align="left")
				image.text((1509, 409), text=f"{millify(points, precision=2) if points >= 10000 else points}", font=font4, color=textbg, align="left")
				image.text((281, 488), text=f"#{lb.index(member.id)+1}", font=font5, color=textbg, align="left")
				image.text((314, 564), text=f"{millify(msgs, precision=2) if msgs >= 10000 else msgs}", font=font5, color=textbg, align="center")
				card = File(fp=image.image_bytes, filename="rank.png")
				await ctx.send(file=card)

	@commands.command(aliases=["market"])
	async def shop(self, ctx):
		await ctx.trigger_typing()
		return await ctx.send("Shop will open soon!")
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		coins = await db.field("SELECT Coins FROM main WHERE UserID = %s", ctx.author.id)
		embed=Embed(color=0x2f3136, title=f"{ctx.guild.name}'s Server Shop", description=f"*You have <:money_icon:1075986284461445140> **{coins:,}**. Purchase something by using the selections below.*\n\n[1] 🖼️ **Rank Themes**\n[2] 🖼️ **Level Up Themes**\n[3] 🖼️ **Profile Banners**\n[4] 🖼️ **Text Colors**\n[5] 🖼️ **Outline Colors**\n[6] 🖼️ **Items**").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=ctx.author.avatar)
		await ctx.send(embed=embed, view=ShopView(ctx))

	@commands.command(aliases=["rsettings", "rsetting", "rs"])
	async def ranksettings(self, ctx):
		await ctx.trigger_typing()
		return await ctx.send("Rank Settings will open soon!")
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		else:
			# return await ctx.send("This command is not included in this month's Beta Test. Please wait for announcements regarding this test and who may use it.")
			async with ctx.typing():
				if len(ctx.author.name) > 15:
					username = ctx.author.name.replace(ctx.author.name[15:], "...")
				else:
					username = ctx.author.name
				if len(ctx.author.display_name) > 15:
					nickname = ctx.author.display_name.replace(ctx.author.display_name[15:], "...")
				else:
					nickname = ctx.author.display_name
				if ctx.author.avatar is None:
					profile, avatar = await load_image_async(str(ctx.author.display_avatar.url)), await load_image_async(str(ctx.author.display_avatar.url))
				else:
					profile, avatar = await load_image_async(str(ctx.author.avatar.url)), await load_image_async(str(ctx.author.display_avatar.url))
				image = Editor("./properties/assets/kbl_podcast_bg.png").resize((1920, 1080), crop=True).blur(amount=7).rounded_corners()
				profile_, avatar_ = Editor(profile).resize((342, 342)).circle_image(), Editor(avatar).resize((55, 55)).circle_image()
				banner_choice, textbg, polybg, outlinebg = await db.record("SELECT BannerChoice, TextBG, PolyBG, OutlineBG FROM main WHERE UserID = %s", ctx.author.id)
				profile_banner = bannerchoice(banner_choice)
				stats_icon, message_icon = Editor("./properties/assets/stats_icon.png").resize((80, 56)), Editor("./properties/assets/message_icon.png").resize((64, 54), crop=True)
				money_icon = Editor("./properties/assets/money_icon.png").resize((85, 64))
				status_icon, status = Editor("./properties/assets/online.png").resize((40, 40)), "Online"
				font, font1 = Font.montserrat(variant="bold", size=60), Font.montserrat(variant="bold", size=50)
				font2, font3 = Font.montserrat(variant="bold", size=104), Font.montserrat(variant="bold", size=47)
				font4, font5 = Font.montserrat(variant="bold", size=51), Font.montserrat(variant="bold", size=46)
				# --- PASTING FILES --- #
				image.paste(profile_banner.image, (53, 0))
				image.paste(profile_.image, (120, 90))
				image.paste(avatar_.image, (619, 167))
				image.paste(stats_icon.image, (165, 471))
				image.paste(message_icon.image, (174, 555))
				image.paste(money_icon.image, (1415, 399))
				image.paste(status_icon.image, (619, 403))
				# --- INSERTING SHAPES --- #
				image.ellipse((200, 666), width=167, height=167, outline=polybg, stroke_width=15)
				image.ellipse((120, 90), width=342, height=342, outline="#0000ff", stroke_width=10)
				image.rectangle((585, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((919, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((1252, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((1585, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((609, 554), width=402, height=113, outline=polybg, stroke_width=15, radius=90)
				image.text((681, 591), text=f"Daldalero", font=font1, color=textbg, align="left")
				image.rectangle((1020, 554), width=294, height=113, outline=polybg, stroke_width=15, radius=90)
				image.text((1075, 591), text=f"Payaso", font=font1, color=textbg, align="left")
				image.rectangle((603, 239), width=1259, height=137, outline=outlinebg, stroke_width=15, fill=polybg, radius=90)
				image.bar((603, 239), max_width=588, height=137, percentage=14, fill=outlinebg, radius=90)
				# --- APPLYING TEXT --- #
				image.text_stroke((655, 280), text=f"17 / 100 (Level 1)", font=font, stroke_width=4, stroke_fill="#000000", color=textbg, align="left")
				image.text((691, 175), text=f"{username}", font=font1, color=textbg, align="left")
				image.text((620, 48), text=f"{nickname}", font=font2, color=textbg, align="left")
				image.text((676, 403), text=f"{status}", font=font3, color=textbg, align="left")
				image.text((676, 484), text=f"-", font=font3, color=textbg, align="left")
				image.text((1509, 409), text=f"3.7k (+2)", font=font4, color=textbg, align="left")
				image.text((281, 488), text=f"#1", font=font5, color=textbg, align="left")
				image.text((314, 564), text=f"1.3k", font=font5, color=textbg, align="center")
				card = File(fp=image.image_bytes, filename="rank.png")
				await ctx.send(content="> Select between different dropdowns to pick.", file=card, view=await RankSettings(ctx))

	@commands.command(aliases=["leaderboard", "lb", "top"])
	async def leaderboards(self, ctx, suffix=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		mems = [member.id for member in ctx.guild.members if not member.bot]
		new_list = []
		if suffix is None:
			lb = await db.records("SELECT UserID, GeneralLevel, GeneralXP FROM main ORDER BY GeneralLevel DESC, GeneralXP DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC, GeneralXP DESC")
			for i in range(len(lb)-1):
				try:
					user, lvl, xp = lb[i][0], lb[i][1], lb[i][2]
					if user in mems:
						new_list.append((user, lvl, xp))
				except:
					pass
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="General Category", users=lb_, client=self.client)
			await paginator.start()
		elif suffix.lower() in ["--messages", "--message", "--msgs", "--msg"]:
			lb = await db.records("SELECT UserID, Messages FROM main ORDER BY Messages DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY Messages DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Messages", users=lb_, client=self.client)
			await paginator.start()
		elif suffix.lower() in ["--ligtaspoints", "--ligtas", "--lp"]:
			lb = await db.records("SELECT UserID, LigtasPoints FROM main ORDER BY LigtasPoints DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Ligtas Points", users=lb_, client=self.client)
			await paginator.start()
		elif suffix.lower() in ["--coins", "--coin", "--cn"]:
			lb = await db.records("SELECT UserID, Coins FROM main ORDER BY Coins DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY Coins DESC")
			for i in range(len(lb)-1):
				try:
					user, lvl = lb[i][0], lb[i][1]
					if user in mems:
						new_list.append((user, lvl))
				except:
					pass
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Coins", users=lb_, client=self.client)
			await paginator.start()
		else:
			lb = await db.records("SELECT UserID, GeneralLevel, GeneralXP FROM main ORDER BY GeneralLevel DESC, GeneralXP DESC")
			lb_ = await db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC, GeneralXP DESC")
			for i in range(len(lb)-1):
				try:
					user, lvl, xp = lb[i][0], lb[i][1], lb[i][2]
					if user in mems:
						new_list.append((user, lvl, xp))
				except:
					pass
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="General Category", users=lb_, client=self.client)
			await paginator.start()

	@commands.command(aliases=['pt', 'pts', 'point'])
	async def points(self, ctx, user: Member=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		user = user or ctx.author
		sp, lp = await db.record("SELECT MonthlySP, LigtasPoints FROM main WHERE UserID = %s", user.id)
		spl, lpl = await db.column("SELECT UserID FROM main ORDER BY MonthlySP DESC"), await db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC")
		embed=Embed(color=0x2f3136, title=f"{user.name}'s Points", description=f"• **Solid Points**: {round(sp, 1):,} (#{spl.index(user.id)+1})\n• **Ligtas Points**: {lp:,} (#{lpl.index(user.id)+1})")
		embed.set_footer(text="Earn SP via sending memes. Earn LP by being nice.", icon_url=user.display_avatar.url)
		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(rankings(client))