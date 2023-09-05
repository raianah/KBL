import time, datetime, ast, humanize
from disnake.ext import commands
from disnake import Embed, Member, File, CustomActivity, Game, Streaming, Spotify
from disnake.ui import View, Button
from typing import Union
from mizuki.db import db
from millify import millify
from easy_pil import Editor, load_image_async, Font
from properties.misc_1 import ShopView, RankSettings, LeaderboardPages, StarboardPages

def check_status(status):
	if status == "dnd":
		icon, status = Editor("./properties/assets/dnd.png").resize((40, 40)), "Do not Disturb"
	elif status == "online":
		icon, status = Editor("./properties/assets/online.png").resize((40, 40)), "Online"
	elif status == "idle":
		icon, status = Editor("./properties/assets/idle.png").resize((40, 40)), "Idle"
	elif status == "streaming":
		icon, status = Editor("./properties/assets/streaming.png").resize((40, 40)), "Streaming"
	else:
		icon, status = Editor("./properties/assets/offline.png").resize((40, 40)), "Offline/Invisible"
	return icon, status

def general_rank_names(level):
	if level < 10:
		role_name = "Daldalero"
	elif level >= 10 and level < 20:
		role_name = "Amb*t"
	elif level >= 20 and level < 30:
		role_name = "Bug*k"
	elif level >= 30 and level < 40:
		role_name = "K*mag"
	elif level >= 40 and level < 50:
		role_name = "Dep*ta"
	elif level >= 50 and level < 60:
		role_name = "Eng*t"
	elif level >= 60 and level < 70:
		role_name = "G*go"
	elif level >= 70 and level < 80:
		role_name = "H*ngal"
	elif level >= 80 and level < 90:
		role_name = "Imp*kto"
	elif level >= 90 and level < 100:
		role_name = "L*kayo"
	return role_name

def memes_rank_names(level):
	if level < 3:
		role_name = "Payaso"
	elif level >= 3 and level < 8:
		role_name = "Egul"
	elif level >= 8 and level < 18:
		role_name = "Dumi"
	elif level >= 18 and level < 33:
		role_name = "Cykat"
	elif level >= 33 and level < 50:
		role_name = "Banal"
	elif level >= 50:
		role_name = "Alamat"
	return role_name

def bannerchoice(value):
	if value == 0:
		profile_banner = Editor("./properties/assets/cyber_banner.png").resize((464, 1010))
	elif value == 1:
		profile_banner = Editor("./properties/assets/glory_banner.png").resize((464, 1010))
	elif value == 2:
		profile_banner = Editor("./properties/assets/nature_banner.png").resize((464, 1010))
	return profile_banner

def check_new_username(user):
	if user.discriminator == "0":
		return user.name
	else:
		return user

# "Thank you for participating in the past __testing phase__. Unfortunately we need to polish things on our side before fully releasing this update.\n\nAll progress will reset by the time leveling will re-release. Please be guided."

class kbl_3(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("KBL (Part 3) is loaded.")

	@commands.command()
	async def vote(self, ctx):
		return await ctx.send("This command is not included in this month's Beta Test. Please wait for announcements regarding this test and who may use it.")
		await ctx.send("__Help upvote Kilusang B\*bong Lipunan and receive rewards upon voting!__\n\n**Link**: <https://top.gg/servers/961502956195303494/vote>\n**Rewards**: +5 Bonus **__Solid Points__**\n\n**__Solid Points__** can be used to purchase text/outline colors via `.shop`. Your regular addition of SP will increase by 5 for 12 hours.")

	@commands.command(aliases=['stats', 'statistic', 'stat', 'st'])
	async def statistics(self, ctx, member: Union[Member, str]=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		else:
			if member is None:
				member = ctx.author
				lapagan_role_list = [962162865182216235, 962162588936962089, 962162495290757120, 962162402613420062, 962162467520262154, 962164001419173888, 961817056565661796]
				lipunan_role_list = [962164982353641512, 962164955585589310, 962164898866036796, 962164856151236618, 962164802275385355, 962164765654908929, 962164718846500886, 962166066455384116, 962209710533124107]
				lapagan_role_check = [role.id for role in member.roles if role.id in lapagan_role_list]
				lipunan_role_check = [role.id for role in member.roles if role.id in lipunan_role_list]
				points, solidpoints, ligtaspoints, messages, voting_duration = db.record("SELECT Points, MonthlyBonusPoints, LigtasPoints, Messages, VotingDuration FROM main WHERE UserID = ?", member.id)
				users = db.column("SELECT UserID FROM main ORDER BY Points DESC")
				b_users = db.column("SELECT UserID FROM main ORDER BY MonthlyBonusPoints DESC")
				lp_lb = db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC")
				msg_lb = db.column("SELECT UserID FROM main ORDER BY Messages DESC")
				m = check_new_username(member)
				if len(lapagan_role_check) > 0 and len(lipunan_role_check) > 0:
					lb0 = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
					lb1 = db.column("SELECT UserID FROM main ORDER BY MemesLevel DESC")
					lpn_rank, lpg_rank, lpn_xp, lpg_xp, lpn_limit, lpg_limit = db.record("SELECT GeneralLevel, MemesLevel, GeneralXP, MemesXP, GenLevelLimit, MemLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**\n• **Rank (Lapagan)**: Level {lpg_rank}\n　• {lpg_xp:,} XP / {lpg_limit:,} XP\n　• Top **{lb1.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)
				elif len(lapagan_role_check) > 0 and len(lipunan_role_check) == 0:
					lb1 = db.column("SELECT UserID FROM main ORDER BY MemesLevel DESC")
					lpg_rank, lpg_xp, lpg_limit = db.record("SELECT MemesLevel, MemesXP, MemLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lapagan)**: Level {lpg_rank}\n　• {lpg_xp:,} XP / {lpg_limit:,} XP\n　• Top **{lb1.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)
				elif len(lapagan_role_check) == 0 and len(lipunan_role_check) > 0:
					lb0 = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
					lpn_rank, lpn_xp, lpn_limit = db.record("SELECT GeneralLevel, GeneralXP, GenLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)
			elif isinstance(member, Member):
				member = member or ctx.author
				lapagan_role_list = [962162865182216235, 962162588936962089, 962162495290757120, 962162402613420062, 962162467520262154, 962164001419173888, 961817056565661796]
				lipunan_role_list = [962164982353641512, 962164955585589310, 962164898866036796, 962164856151236618, 962164802275385355, 962164765654908929, 962164718846500886, 962166066455384116, 962209710533124107]
				lapagan_role_check = [role.id for role in member.roles if role.id in lapagan_role_list]
				lipunan_role_check = [role.id for role in member.roles if role.id in lipunan_role_list]
				points, solidpoints, ligtaspoints, messages, voting_duration = db.record("SELECT Points, BonusCoins, LigtasPoints, Messages, VotingDuration FROM main WHERE UserID = ?", member.id)
				users = db.column("SELECT UserID FROM main ORDER BY Points")
				b_users = db.column("SELECT UserID FROM main ORDER BY BonusCoins")
				lp_lb = db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC")
				msg_lb = db.column("SELECT UserID FROM main ORDER BY Messages DESC")
				m = check_new_username(member)
				if len(lapagan_role_check) > 0 and len(lipunan_role_check) > 0:
					lb0 = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
					lb1 = db.column("SELECT UserID FROM main ORDER BY MemesLevel DESC")
					lpn_rank, lpg_rank, lpn_xp, lpg_xp, lpn_limit, lpg_limit = db.record("SELECT GeneralLevel, MemesLevel, GeneralXP, MemesXP, GenLevelLimit, MemLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**\n• **Rank (Lapagan)**: Level {lpg_rank}\n　• {lpg_xp:,} XP / {lpg_limit:,} XP\n　• Top **{lb1.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)
				elif len(lapagan_role_check) > 0 and len(lipunan_role_check) == 0:
					lb1 = db.column("SELECT UserID FROM main ORDER BY MemesLevel DESC")
					lpg_rank, lpg_xp, lpg_limit = db.record("SELECT MemesLevel, MemesXP, MemLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lapagan)**: Level {lpg_rank}\n　• {lpg_xp:,} XP / {lpg_limit:,} XP\n　• Top **{lb1.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)
				elif len(lapagan_role_check) == 0 and len(lipunan_role_check) > 0:
					lb0 = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
					lpn_rank, lpn_xp, lpn_limit = db.record("SELECT GeneralLevel, GeneralXP, GenLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)
			elif isinstance(member, str):
				if member.lower() in ["--description", "--desc", "--d"]:
					embed=Embed(color=0x2f3136, title="Ranking Description").set_footer(text=f"Showing the basics of ranking in KBL", icon_url=ctx.author.display_avatar).set_thumbnail(url=ctx.guild.icon)
					embed.description = "**__Balance__**\n- <:money_icon:1075986284461445140> **Pera** is a type of currency in KBL that can be obtained by chatting in all **__Lipunan__** categories. Your pera will be added automatically per message (cooldown per message are being observed).\n- You can spend <:money_icon:1075986284461445140> **Pera** via `.shop`.\n  - You can also earn <:money_icon:1075986284461445140> **Pera** by collecting **Solid Points**, a point-based score that can be obtained by posting memes on <#961504020508340294>. The higher your current Solid Points, the higher the amount of your <:money_icon:1075986284461445140> **Pera** per message.\n- **Ligtas Points**, or LP, are another type of points that can only be occurred via thanking the user. It can be in a form of mention, or replied message. By this members will be filtered on who is the most helpful in the server. Don't forget to track users with the highest LP via `.leaderboard --lp` to show who's the most helpful.\n\n**__Rankings__**\n- Rankings are a way to engage more members on a server. By participating in various categories (Lapagan & Lipunan), you will be granted XP which levels up if you reached certain XP threshold per level.\n- In <#961504020508340294>, reaching at least top 30 will grant you a trophy that can be displayed on your rank card, or via `.trophy`.\n  - XP & Level from Lapagan & Lipunan categories are different, and won't conflict one from another.\n  - Leveling up also grants roles that changes as your level goes further."
					await ctx.send(embed=embed)
				else:
					await ctx.send("Available suffixes: `--description`, `--desc`, `--d`\n\nUsage: `.statistics --desc`")
			else:
				member = ctx.author
				lapagan_role_list = [962162865182216235, 962162588936962089, 962162495290757120, 962162402613420062, 962162467520262154, 962164001419173888, 961817056565661796]
				lipunan_role_list = [962164982353641512, 962164955585589310, 962164898866036796, 962164856151236618, 962164802275385355, 962164765654908929, 962164718846500886, 962166066455384116, 962209710533124107]
				lapagan_role_check = [role.id for role in member.roles if role.id in lapagan_role_list]
				lipunan_role_check = [role.id for role in member.roles if role.id in lipunan_role_list]
				points, solidpoints, ligtaspoints, messages, voting_duration = db.record("SELECT Points, BonusCoins, LigtasPoints, Messages, VotingDuration FROM main WHERE UserID = ?", member.id)
				users = db.column("SELECT UserID FROM main ORDER BY Points")
				b_users = db.column("SELECT UserID FROM main ORDER BY BonusCoins")
				lp_lb = db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC")
				msg_lb = db.column("SELECT UserID FROM main ORDER BY Messages DESC")
				m = check_new_username(member)
				if len(lapagan_role_check) > 0 and len(lipunan_role_check) > 0:
					lb0 = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
					lb1 = db.column("SELECT UserID FROM main ORDER BY MemesLevel DESC")
					lpn_rank, lpg_rank, lpn_xp, lpg_xp, lpn_limit, lpg_limit = db.record("SELECT GeneralLevel, MemesLevel, GeneralXP, MemesXP, GenLevelLimit, MemLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**\n• **Rank (Lapagan)**: Level {lpg_rank}\n　• {lpg_xp:,} XP / {lpg_limit:,} XP\n　• Top **{lb1.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)
				elif len(lapagan_role_check) > 0 and len(lipunan_role_check) == 0:
					lb1 = db.column("SELECT UserID FROM main ORDER BY MemesLevel DESC")
					lpg_rank, lpg_xp, lpg_limit = db.record("SELECT MemesLevel, MemesXP, MemLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lapagan)**: Level {lpg_rank}\n　• {lpg_xp:,} XP / {lpg_limit:,} XP\n　• Top **{lb1.index(member.id)+1}** out of **{len(users)} users**", title=f"{m}'s User Statistics")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)
				elif len(lapagan_role_check) == 0 and len(lipunan_role_check) > 0:
					lb0 = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
					lpn_rank, lpn_xp, lpn_limit = db.record("SELECT GeneralLevel, GeneralXP, GenLevelLimit FROM main WHERE UserID = ?", member.id)
					#if voting_duration == 0 or int(time.time()) > voting_duration:
					#	voter = "[Not yet voted](https://top.gg/servers/961502956195303494/vote)"
					#else:
					#	voter = f"Voted (Expiry: <t:{voting_duration}:R>)"
					voter = "Disabled"
					embed=Embed(color=0x2f3136, description=f"**__Miscellaneous__**\n• <:money_icon:1075986284461445140> **{points:,}**\n　• Top **{users.index(member.id)+1}** out of **{len(users)} users**\n• **{solidpoints:,} Solid Points**\n　• Top **{b_users.index(member.id)+1}** out of **{len(users)} users**\n• **{ligtaspoints:,} Ligtas Points**\n　• Top **{lp_lb.index(member.id)+1}** out of **{len(users)} users**\n• **{messages:,} Messages**\n　• Top **{msg_lb.index(member.id)+1}** out of **{len(users)} users**\n• **Voting Status**: {voter}\n\n**__Rankings__**\n• **Rank (Lipunan)**: Level {lpn_rank}\n　• {lpn_xp:,} XP / {lpn_limit:,} XP\n　• Top **{lb0.index(member.id)+1}** out of **{len(users)} users**")
					embed.set_footer(text=f"Showing {m}'s server statistics.", icon_url=member.display_avatar).set_thumbnail(url=ctx.guild.icon)
					await ctx.send(embed=embed)

	@commands.command(aliases=["level", "lvl"])
	async def rank(self, ctx, member: Union[Member, str]=None, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		else:
			if member is None and suffix is None:
				member = ctx.author
			elif type(member) == Member:
				member = member
				if member.bot:
					return await ctx.send(f"{member.mention} is tagged as a bot. Overall bots don't gain XP nor gain level from this leveling.")
			elif member.lower() in ["--m", "--memes", "--meme"]:
				suffix = member.lower()
				member = ctx.author
			activity = None
			for act in member.activities:
				if isinstance(act, CustomActivity):
					try:
						activity = f"{act.name}"
						break
					except:
						pass
				if isinstance(act, Game):
					pass
				if isinstance(act, Streaming):
					pass
				if isinstance(act, Spotify):
					pass
			if activity == None:
				activity = "-"
			elif len(activity) > 30:
				activity = activity.replace(activity[30:], "...")
			async with ctx.typing():
				rank_name, m_rname = "", ""
				lapagan_role_list = [962162865182216235, 962162588936962089, 962162495290757120, 962162402613420062, 962162467520262154, 962164001419173888]
				lipunan_role_list = [962164982353641512, 962164955585589310, 962164898866036796, 962164856151236618, 962164802275385355, 962164765654908929, 962164718846500886, 962166066455384116]
				lapagan_role_check = [role.id for role in member.roles if role.id in lapagan_role_list]
				lipunan_role_check = [role.id for role in member.roles if role.id in lipunan_role_list]
				dt = datetime.datetime.now().weekday()
				if dt in [4, 5, 6]:
					sp = 5
				else:
					sp = 3
				view = View()
				button = Button(label=f"Voting disabled", url="https://top.gg/servers/961502956195303494/vote", disabled=True)
				view.add_item(button)
				gen_lvl, gen_xp, gen_lvl_limit = db.record("SELECT GeneralLevel, GeneralXP, GenLevelLimit FROM main WHERE UserID = ?", member.id)
				mem_lvl, mem_xp, mem_lvl_limit = db.record("SELECT MemesLevel, MemesXP, MemLevelLimit FROM main WHERE UserID = ?", member.id)
				points, msgs, bonus_coins, voting_duration = db.record("SELECT Points, Messages, BonusCoins, VotingDuration FROM main WHERE UserID = ?", member.id)
				banner_choice, textbg, polybg, outlinebg = db.record("SELECT BannerChoice, TextBG, PolyBG, OutlineBG FROM main WHERE UserID = ?", member.id)
				profile_banner = bannerchoice(banner_choice)
				if len(lipunan_role_check) == 0:
					suffix = "--m"
				if suffix in ["--m", "--memes", "--meme"]:
					lb = db.column("SELECT UserID FROM main ORDER BY MemesLevel DESC")
					percentage = int(((mem_xp * 100) / mem_lvl_limit))
					if percentage < 1:
						percentage = 0
				else:
					lb = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC")
					percentage = int(((gen_xp * 100) / gen_lvl_limit))
					if percentage < 1:
						percentage = 0
				# --- INITIALIZING IMAGES --- #
				if len(member.name) > 15:
					username = member.name.replace(member.name[15:], "...")
				else:
					username = member.name
				if len(member.display_name) > 15:
					nickname = ctx.author.display_name.replace(member.display_name[15:], "...")
				else:
					nickname = member.display_name
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
				#if suffix in ["--m", "--memes", "--meme", "b", "--b", "2", "--2"]:
				#	if len(lapagan_role_check) == 0:
				#		return await ctx.send("You are not listed in **Lapagan** Category! Please contact with KBL Staffs to address this issue.")
				#	image.ellipse((120, 90), width=342, height=342, outline="#ff0000", stroke_width=10)
				#else:
				image.ellipse((120, 90), width=342, height=342, outline="#0000ff", stroke_width=10)
				image.rectangle((585, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((919, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((1252, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				image.rectangle((1585, 731), width=293, height=296, outline=polybg, stroke_width=13, radius=60)
				if len(lipunan_role_check) > 0:
					rank_name = general_rank_names(gen_lvl)
				if len(lapagan_role_check) > 0:
					m_rname = memes_rank_names(mem_lvl)
				if len(rank_name) == 0:
					pass
				elif len(rank_name) == 4:
					image.rectangle((609, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
					image.text((687, 591), text=f"{rank_name}", font=font1, color=textbg, align="left")
				elif len(rank_name) == 6:
					image.rectangle((609, 554), width=294, height=113, outline=polybg, stroke_width=15, radius=90)
					image.text((664, 591), text=f"{rank_name}", font=font1, color=textbg, align="left")
				elif len(rank_name) > 6:
					image.rectangle((609, 554), width=402, height=113, outline=polybg, stroke_width=15, radius=90)
					image.text((681, 591), text=f"{rank_name}", font=font1, color=textbg, align="left")
				else:
					image.rectangle((609, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
					image.text((668, 591), text=f"{rank_name}", font=font1, color=textbg, align="left")
				if len(rank_name) == 0:
					if len(m_rname) == 4:
						image.rectangle((609, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((687, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) == 6:
						image.rectangle((609, 554), width=294, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((664, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) > 6:
						image.rectangle((609, 554), width=402, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((681, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					else:
						image.rectangle((609, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((668, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
				elif len(rank_name) == 4:
					if len(m_rname) == 4:
						image.rectangle((909, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((987, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) == 6:
						image.rectangle((909, 554), width=294, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((964, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) > 6:
						image.rectangle((909, 554), width=402, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((981, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					else:
						image.rectangle((909, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((968, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
				elif len(rank_name) == 6:
					if len(m_rname) == 4:
						image.rectangle((909, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((987, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) == 6:
						image.rectangle((909, 554), width=294, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((964, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) > 6:
						image.rectangle((909, 554), width=402, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((981, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					else:
						image.rectangle((909, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((968, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
				elif len(rank_name) > 6:
					if len(m_rname) == 4:
						image.rectangle((1020, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((1079, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) == 6:
						image.rectangle((1020, 554), width=294, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((1075, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) > 6:
						image.rectangle((1020, 554), width=402, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((1092, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					else:
						image.rectangle((1020, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((1079, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
				else:
					if len(m_rname) == 4:
						image.rectangle((909, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((987, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) == 6:
						image.rectangle((909, 554), width=294, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((964, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					elif len(m_rname) > 6:
						image.rectangle((909, 554), width=402, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((981, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
					else:
						image.rectangle((909, 554), width=292, height=113, outline=polybg, stroke_width=15, radius=90)
						image.text((968, 591), text=f"{m_rname}", font=font1, color=textbg, align="left")
				image.rectangle((603, 239), width=1259, height=137, outline=outlinebg, stroke_width=15, fill=polybg, radius=90)
				if percentage > 0:
					image.bar((603, 239), max_width=588, height=137, percentage=percentage, fill=outlinebg, radius=90)
				# --- APPLYING TEXT --- #
				if suffix in ["--m", "--memes", "--meme"]:
					image.text_stroke((655, 280), text=f"{millify(mem_xp, precision=2)} / {millify(mem_lvl_limit, precision=2)} (Level {mem_lvl}) - Lapagan", font=font, stroke_width=4, stroke_fill="#000000", color=textbg, align="left")
				else:
					image.text_stroke((655, 280), text=f"{millify(gen_xp, precision=2)} / {millify(gen_lvl_limit, precision=2)} (Level {gen_lvl}) - Lipunan", font=font, stroke_width=4, stroke_fill="#000000", color=textbg, align="left")
				image.text((691, 175), text=f"{username}#{member.discriminator}", font=font1, color=textbg, align="left")
				image.text((620, 48), text=f"{nickname}", font=font2, color=textbg, align="left")
				image.text((676, 403), text=f"{status}", font=font3, color=textbg, align="left")
				image.text((676, 484), text=f"{activity}", font=font3, color=textbg, align="left")
				image.text((1509, 409), text=f"{millify(points, precision=2) if points >= 10000 else points}", font=font4, color=textbg, align="left")
				image.text((281, 488), text=f"#{lb.index(member.id)+1}", font=font5, color=textbg, align="left")
				image.text((314, 564), text=f"{millify(msgs, precision=2) if msgs >= 10000 else msgs}", font=font5, color=textbg, align="center")
				card = File(fp=image.image_bytes, filename="rank.png")
				if int(time.time()) > voting_duration:
					await ctx.send(file=card, view=view)
				else:
					await ctx.send(file=card)

	@commands.command(aliases=["market"])
	async def shop(self, ctx):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		coins = db.field("SELECT Points FROM main WHERE UserID = ?", ctx.author.id)
		embed=Embed(color=0x2f3136, title=f"{ctx.guild.name}'s Server Shop", description=f"*You have <:money_icon:1075986284461445140> **{coins:,}**. Purchase something by using the selections below.*\n\n[1] 🖼️ **Rank Themes**\n[2] 🖼️ **Level Up Themes**\n[3] 🖼️ **Profile Banners**\n[4] 🖼️ **Text Colors**\n[5] 🖼️ **Outline Colors**\n[6] 🖼️ **Items**").set_footer(text="Purchase an item/theme by pressing '✅' button!", icon_url=ctx.author.avatar)
		await ctx.send(embed=embed, view=ShopView(ctx))

	@commands.command(aliases=["rsettings", "rsetting", "rs"])
	async def ranksettings(self, ctx):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		else:
			return await ctx.send("This command is not included in this month's Beta Test. Please wait for announcements regarding this test and who may use it.")
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
				banner_choice, textbg, polybg, outlinebg = db.record("SELECT BannerChoice, TextBG, PolyBG, OutlineBG FROM main WHERE UserID = ?", ctx.author.id)
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
				image.text_stroke((655, 280), text=f"17 / 100 (Level 1) - Lipunan", font=font, stroke_width=4, stroke_fill="#000000", color=textbg, align="left")
				image.text((691, 175), text=f"{username}#{ctx.author.discriminator}", font=font1, color=textbg, align="left")
				image.text((620, 48), text=f"{nickname}", font=font2, color=textbg, align="left")
				image.text((676, 403), text=f"{status}", font=font3, color=textbg, align="left")
				image.text((676, 484), text=f"-", font=font3, color=textbg, align="left")
				image.text((1509, 409), text=f"3.7k (+2)", font=font4, color=textbg, align="left")
				image.text((281, 488), text=f"#1", font=font5, color=textbg, align="left")
				image.text((314, 564), text=f"1.3k", font=font5, color=textbg, align="center")
				card = File(fp=image.image_bytes, filename="rank.png")
				await ctx.send(content="> Select between different dropdowns to pick.", file=card, view=RankSettings(ctx))

	@commands.command(aliases=["leaderboard", "lb", "top"])
	async def leaderboards(self, ctx, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		mems = [member.id for member in ctx.guild.members if not member.bot]
		if suffix is None:
			return await ctx.send("Thank you for participating in the past __testing phase__. Unfortunately we need to polish things on our side before fully releasing this update.\n\nAll progress will reset by the time leveling will re-release. Please be guided.")
			lb = db.records("SELECT UserID, GeneralLevel, GeneralXP FROM main ORDER BY GeneralLevel DESC, GeneralXP DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC, GeneralXP DESC")
			for i in range(len(lb)-1):
				try:
					user, lvl, xp = lb[i][0], lb[i][1], lb[i][2]
					if user in mems:
						new_list.append((user, lvl, xp))
				except:
					pass
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="General Category", users=lb_, client=self.client)
			await paginator.start()
		elif suffix in ["--m", "--memes", "--meme"]:
			return await ctx.send("Thank you for participating in the past __testing phase__. Unfortunately we need to polish things on our side before fully releasing this update.\n\nAll progress will reset by the time leveling will re-release. Please be guided.")
			lb = db.records("SELECT UserID, MemesLevel, MemesXP FROM main ORDER BY MemesLevel DESC, MemesXP DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY MemesLevel DESC, MemesXP DESC")
			for i in range(len(lb)-1):
				try:
					user, lvl, xp = lb[i][0], lb[i][1], lb[i][2]
					if user in mems:
						new_list.append((user, lvl, xp))
				except:
					pass
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Memes Category", users=lb_, client=self.client)
			await paginator.start()
		elif suffix.lower() in ["--messages", "--message", "--msgs", "--msg"]:
			lb = db.records("SELECT UserID, Messages FROM main ORDER BY Messages DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY Messages DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Messages", users=lb_, client=self.client)
			await paginator.start()
		elif suffix.lower() in ["--ligtaspoints", "--ligtas", "--lp"]:
			lb = db.records("SELECT UserID, LigtasPoints FROM main ORDER BY LigtasPoints DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC")
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Ligtas Points", users=lb_, client=self.client)
			await paginator.start()
		elif suffix.lower() in ["--coins", "--coin", "--points", "--point", "--pts", "--pt"]:
			return await ctx.send("Thank you for participating in the past __testing phase__. Unfortunately we need to polish things on our side before fully releasing this update.\n\nAll progress will reset by the time leveling will re-release. Please be guided.")
			lb = db.records("SELECT UserID, Points FROM main ORDER BY Points DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY Points DESC")
			for i in range(len(lb)-1):
				try:
					user, lvl = lb[i][0], lb[i][1]
					if user in mems:
						new_list.append((user, lvl))
				except:
					pass
			paginator = LeaderboardPages(entries=lb, ctx=ctx, _type="Points", users=lb_, client=self.client)
			await paginator.start()
		elif suffix.lower() in ["--solidpoints", "--solid", "--sp"]:
			await ctx.send("The command has been shifted to `.sp`.")
		else:
			return await ctx.send("Thank you for participating in the past __testing phase__. Unfortunately we need to polish things on our side before fully releasing this update.\n\nAll progress will reset by the time leveling will re-release. Please be guided.")
			lb = db.records("SELECT UserID, GeneralLevel, GeneralXP FROM main ORDER BY GeneralLevel DESC, GeneralXP DESC")
			lb_ = db.column("SELECT UserID FROM main ORDER BY GeneralLevel DESC, GeneralXP DESC")
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
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		user = user or ctx.author
		m = check_new_username(user)
		sp, lp = db.record("SELECT MonthlyBonusPoints, LigtasPoints FROM main WHERE UserID = ?", user.id)
		spl, lpl = db.column("SELECT UserID FROM main ORDER BY BonusCoins DESC"), db.column("SELECT UserID FROM main ORDER BY LigtasPoints DESC")
		embed=Embed(color=0x2f3136, title=f"{m}'s Points", description=f"• **Solid Points**: {round(sp, 1):,} (#{spl.index(user.id)+1})\n• **Ligtas Points**: {lp:,} (#{lpl.index(user.id)+1})")
		embed.set_footer(text="Earn SP via sending memes. Earn LP by being nice.", icon_url=user.display_avatar.url)
		await ctx.send(embed=embed)

	@commands.command(aliases=['str'])
	async def starboard(self, ctx, key: Union[Member, str]=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		new_list = []
		if key is None:
			starboard = db.field("SELECT StarboardList FROM global")
			_starboard = ast.literal_eval(starboard)
			_starboard_items = list(_starboard.items())
			if len(_starboard_items) == 0:
				await ctx.send("There is no current entry/ies in starboard. Try again later.")
			else:
				for i in range(len(_starboard_items)-1):
					try:
						new_list.append((_starboard_items[0], _starboard_items[1]))
					except:
						pass
				paginator = StarboardPages(entries=new_list, ctx=ctx, _type="Global", user=None)
				await paginator.start()
		elif isinstance(key, Member):
			starboard = db.field("SELECT StarboardList FROM main WHERE UserID = ?", key.id)
			_starboard = ast.literal_eval(starboard)
			_starboard_items = list(_starboard.items())
			_starboard_items.reverse()
			if len(_starboard_items) == 0:
				await ctx.send(f"There is no current entry/ies in {key.mention}'s starboard.")
			else:
				for i in range(len(_starboard_items)-1):
					msg = await ctx.channel.fetch_message(_starboard_items[1][0])
					_join = int(msg.created_at.timestamp())
					_relative = datetime.timedelta(seconds=int(time.time()) - _join)
					_hum = humanize.naturaldelta(_relative)
					new_list.append(f"{i+1}. `{_starboard_items[0]}` • [View Entry]({msg.jump_url}) • {_starboard_items[1][1]} • {_starboard_items[1][3]} votes")
				paginator = StarboardPages(entries=new_list, ctx=ctx, _type="Member", user=msg)
				await paginator.start()
		elif isinstance(key, str):
			try:
				starboard = db.field("SELECT StarboardList FROM global")
				_starboard = ast.literal_eval(starboard)
				msg = await ctx.channel.fetch_message(_starboard[key][0])
				user_starboard = db.field("SELECT StarboardList FROM main WHERE UserID = ?", msg.author.id)
				_user_starboard = ast.literal_eval(user_starboard)
				_join = int(msg.created_at.timestamp())
				_relative = datetime.timedelta(seconds=int(time.time()) - _join)
				_hum = humanize.naturaldelta(_relative)
				media = "\n".join([f"Media #{i+1} - [Click me!]({med})" for i, med in enumerate(msg.attachments)])
				embed = Embed(title=f"{m} • Entry #{_starboard_items[0]}", description=f"Posted {_hum}\nEntry Key: {_starboard_items[0]}\nStatus: {_starboard_items[1][1]}\nRemarks: {_starboard_items[1][2]}\nVotes: {_starboard_items[1][3]}\n\n{media}")
				embed.set_footer(text="To vote for this message, type .svote <member> <key>").set_thumbnail(url=msg.author.avatar)
				await ctx.send(embed=embed)
			except KeyError:
				await ctx.send("Invalid \"key\" phrase. Please double-check the key then try again.")
		else:
			await ctx.send("`.help starboard`")

	@commands.command(aliases=['svote'])
	async def starboardvote(self, ctx, key=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if key is not None:
			try:
				starboard = db.field("SELECT StarboardList FROM global")
				_starboard = ast.literal_eval(starboard)
				msg = await ctx.channel.fetch_message(_starboard[key][0])
				user_starboard = db.field("SELECT StarboardList FROM main WHERE UserID = ?", msg.author.id)
				_user_starboard = ast.literal_eval(user_starboard)
				_user_starboard[key][3] = _user_starboard[key] + 1
				db.execute("UPDATE main SET StarboardList = ? WHERE UserID = ?", f"{_user_starboard}", msg.author.id)
				await ctx.send(f"Successfully voted for {msg.author.mention}'s entry.\nTotal Votes: {_user_starboard[key][3] + 1}")
			except KeyError:
				await ctx.send("Invalid \"key\" phrase. Please double-check the key then try again.")
		else:
			await ctx.send("This command requires a \"key\" input. Please try again.\n`.help starboardvote`")

def setup(client):
	client.add_cog(kbl_3(client))