from disnake import Embed, Member, File, Object, File
from disnake.ext import commands
from mizuki.db import db
from io import BytesIO
from typing import Union
import time, datetime, random, aiohttp, ast
from properties.misc_1 import PartnershipPages, help_

welcome_list = open("./properties/welcome_list.txt").readlines()

def ping_checker(number):
	if number < 70:
		emoj = "🟢"
	elif number >= 70 and number < 140:
		emoj = "🟠"
	elif number >= 140:
		emoj = "🔴"
	return emoj

def check_new_username(user):
	if user.discriminator == "0":
		return user.name
	else:
		return user

def convert_duration(seconds):
	new_list = []
	delta = datetime.timedelta(seconds=seconds)
	minute, second = (delta.seconds % 3600) // 60, (delta.seconds % 60)
	if seconds >= 3600:
		hour = delta.days * 24 + delta.seconds // 3600
		new_list.append(f"{hour}h")
	if minute > 0:
		new_list.append(f"{minute}m")
	if second > 0:
		new_list.append(f"{second}s")
	return new_list

def gen_role_checker(level):
	if level < 10:
		role = None
	elif level >= 10 and level < 20:
		role = Object(962164982353641512)
	elif level >= 20 and level < 30:
		role = Object(962164955585589310)
	elif level >= 30 and level < 40:
		role = Object(962164898866036796)
	elif level >= 40 and level < 50:
		role = Object(962164856151236618)
	elif level >= 50 and level < 60:
		role = Object(962164802275385355)
	elif level >= 60 and level < 70:
		role = Object(962164765654908929)
	elif level >= 70 and level < 80:
		role = Object(962164718846500886)
	#elif level >= 80 and level < 90:
	#	role = "Imp*kto"
	#elif level >= 90 and level < 100:
	#	role = "L*kayo"
	return role

def mem_role_checker(level):
	if level < 3:
		role = None
	elif level >= 3 and level < 8:
		role = Object(962162865182216235)
	elif level >= 8 and level < 18:
		role = Object(962162588936962089)
	elif level >= 18 and level < 33:
		role = Object(962162495290757120)
	elif level >= 33 and level < 50:
		role = Object(962162402613420062)
	elif level >= 50:
		role = Object(962162467520262154)
	return role

class kbl_1(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.client.help_command = None

	@commands.Cog.listener()
	async def on_ready(self):
		print("KBL (Part 1) is loaded.")
		global startTime
		startTime = int(time.time())

	@commands.command()
	async def help(self, ctx, command=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		await help_(command, ctx)

	@commands.command()
	async def ping(self, ctx):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		new_list = convert_duration(int(round(time.time()-startTime)))
		timestamp = " ".join([item for item in new_list])
		emoj = ping_checker(round(self.client.latency * 1000))
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			mm = f"🔴 Maintenance (<t:{md+3600}:R>)"
		else:
			mm = "🟢 Enabled"
		embed=Embed(color=0x2f3136, description=f"**Ping**: {emoj} {round(self.client.latency * 1000)}ms\n**Uptime**: {timestamp}\n**Status**: {mm}")
		await ctx.send(embed=embed)

	@commands.command()
	async def reload(self, ctx, *, extension=None):
		if ctx.author.id in [603256030742183959, 697129372867625054]:
			if ctx.author.id == 697129372867625054:
				mem = await ctx.guild.fetch_member(603256030742183959)
				await mem.send(f"thethimteam#1890 commences a maintenance mode!")
			await ctx.trigger_typing()
			if extension is None:
				await ctx.send("Please put a `extension` name!")
			else:
				try:
					self.client.reload_extension(f"{extension}")
					await ctx.send(f"Successfully reloaded `{extension}` file.")
				except:
					await ctx.send(f"Incorrect extension file ({extension})")

	@commands.command()
	async def maintenance(self, ctx, command=None):
		await ctx.trigger_typing()
		if ctx.author.id in [603256030742183959, 697129372867625054]:
			if ctx.author.id == 697129372867625054:
				mem = await ctx.guild.fetch_member(603256030742183959)
				await mem.send(f"thethimteam#1890 commences a maintenance mode!")
			await ctx.trigger_typing()
			if command == "--start":
				db.execute("UPDATE global SET Maintenance = 1, MaintenanceDuration = ?", int(time.time()))
				embed=Embed(color=0x2f3136, title=f"Scheduled Maintenance (<t:{int(time.time())+3600}:R>)", description=f"Good day! <@1050024676627320872> is now in maintenance mode. During the maintenance period all commands will be disabled for a brief period of time. This is to safely deploy new updates to the bot.\n\nETA: <t:{int(time.time())+3600}:R> (<t:{int(time.time())+3600}:t>)")
				return await ctx.send(embed=embed)
			elif command == "--done":
				db.execute("UPDATE global SET Maintenance = 0, MaintenanceDuration = 0")
				embed=Embed(color=0x2f3136, title=f"Scheduled Maintenance (Done)", description="Good evening! <@1050024676627320872>'s maintenance has been lifted and all commands are now enabled for usage.")
				return await ctx.send(embed=embed)
			else:
				md = db.record("SELECT MaintenanceDuration FROM global")
				if md is None:
					db.execute("UPDATE global SET MaintenanceDuration = 0")
				if md[-1] > 0:
					embed=Embed(color=0x2f3136, title=f"Scheduled Maintenance (<t:{md[-1]}:R>)", description=f"Good day! <@1050024676627320872> is scheduled for maintenance <t:{md[-1]}:R> (<t:{md[-1]}:t>). This is to safely deploy new updates to the bot.\n\nETA: <t:{md[-1]+8600}:R> (<t:{md[-1]+8600}:t>)")
					return await ctx.send(embed=embed)
				else:
					return await ctx.send(f"<@1050024676627320872> is not currently in maintenance!")
		else:
			md = db.record("SELECT MaintenanceDuration FROM global")
			if md[-1] > 0:
				embed=Embed(color=0x2f3136, title=f"Scheduled Maintenance (<t:{md[-1]}:R>)", description=f"Good day! <@1050024676627320872> is scheduled for maintenance <t:{md[-1]}:R> (<t:{md[-1]}:t>). This is to safely deploy new updates to the bot.\n\nETA: <t:{md[-1]+8600}:R> (<t:{md[-1]+8600}:t>)")
				await ctx.send(embed=embed)
			else:
				await ctx.send(f"<@1050024676627320872> is not currently in maintenance!")

	@commands.command()
	async def ma(self, ctx, user: Member=None, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.ma [user]`.\nE.g; `.ma @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			if role.id == 1001430287143669800:
				if suffix == None:
					#reg = db.record("SELECT * FROM main WHERE UserID = ?", user.id)
					#if reg is None:
					#	db.execute("INSERT INTO main (UserID) VALUES (?)", user.id)
					#else:
					#	luc = db.field("SELECT MemLevelUpChecker FROM main WHERE UserID = ?", user.id)
					#	role = mem_role_checker(luc)
					#	if role is not None:
					#		await user.add_roles(role)
					m = check_new_username(user)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2 = Object(962161356486901770), Object(962164001419173888) # LAPAGAN, PAYASO
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
					embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
					await ctx.send(content=f"{user.mention}", embed=embed)
					try:
						embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server")
						embed_.set_image(url=f"{random.choice(welcome_list)}")
						await user.send(embed=embed_)
					except:
						pass
					return
				elif suffix.lower() == "--fix":
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = await ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					if r_role in user.roles:
						await ctx.send(f"{user.mention} is not yet verified! You can't use `--fix` extension with unverified user!")
					else:
						col_list = [bg_role.id, r_role.id, age_role.id, sedula.id, role1.id, role2.id, role3.id, role4.id]
						for role in user.roles:
							if role.id in col_list:
								await user.remove_roles(role)
						m = check_new_username(user)
						await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
						embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
						return await ctx.send(content=f"{user.mention}", embed=embed)
				else:
					await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def mb(self, ctx, user: Member=None, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.mb [user]`.\nE.g; `.mb @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			if role.id == 1001430287143669800:
				if suffix == None:
					#reg = db.record("SELECT * FROM main WHERE UserID = ?", user.id)
					#if reg is None:
					#	db.execute("INSERT INTO main (UserID) VALUES (?)", user.id)
					#else:
					#	luc = db.field("SELECT GenLevelUpChecker FROM main WHERE UserID = ?", user.id)
					#	role = gen_role_checker(luc)
					#	if role is not None:
					#		await user.add_roles(role)
					async with aiohttp.ClientSession() as session:
						async with session.get(random.choice(welcome_list)) as response:
							data = await response.read()
					img = BytesIO(data)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2 = Object(962161205106069624), Object(962166066455384116) # LIPUNAN, BULWAGAN
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					m = check_new_username(user)
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
					embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
					await ctx.send(content=f"{user.mention}", embed=embed)
					try:
						channel = await self.client.fetch_channel(961504364269301764)
						await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
					except:
						pass
					try:
						embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server")
						embed_.set_image(url=f"{random.choice(welcome_list)}")
						await user.send(embed=embed_)
					except:
						pass
					return
				elif suffix.lower() == "--fix":
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					if r_role in user.roles:
						await ctx.send(f"{user.mention} is not yet verified! You can't use `--fix` extension with unverified user!")
					else:
						col_list = [bg_role.id, r_role.id, age_role.id, sedula.id, role1.id, role2.id, role3.id, role4.id]
						for role in user.roles:
							if role.id in col_list:
								await user.remove_roles(role)
						await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
						m = check_new_username(user)
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
						embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
						await ctx.send(content=f"{user.mention}", embed=embed)
						try:
							channel = await self.client.fetch_channel(961504364269301764)
							await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
						except:
							pass
				else:
					await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def mc(self, ctx, user: Member=None, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.mc [user]`.\nE.g; `.mc @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			if role.id == 1001430287143669800:
				if suffix == None:
					#reg = db.record("SELECT * FROM main WHERE UserID = ?", user.id)
					#if reg is None:
					#	db.execute("INSERT INTO main (UserID) VALUES (?)", user.id)
					#else:
					#	luc, guc = db.record("SELECT GenLevelUpChecker, MemLevelUpChecker FROM main WHERE UserID = ?", user.id)
					#	role_1 = gen_role_checker(luc)
					#	role_2 = mem_role_checker(guc)
					#	if role_1 is not None:
					#		await user.add_roles(role_1)
					#	if role_2 is not None:
					#		await user.add_roles(role_2)
					async with aiohttp.ClientSession() as session:
						async with session.get(random.choice(welcome_list)) as response:
							data = await response.read()
					img = BytesIO(data)
					emb_img = random.choice(welcome_list)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					m = check_new_username(user)
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2, role3, role4) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
					embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
					await ctx.send(content=f"{user.mention}", embed=embed)
					try:
						channel = await self.client.fetch_channel(961504364269301764)
						await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
					except:
						pass
					try:
						embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server")
						embed_.set_image(url=f"{random.choice(welcome_list)}")
						await user.send(embed=embed_)
					except:
						pass
					return
				elif suffix.lower() == "--fix":
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					if r_role in user.roles:
						await ctx.send(f"{user.mention} is not yet verified! You can't use `--fix` extension with unverified user!")
					else:
						col_list = [bg_role.id, r_role.id, age_role.id, sedula.id, role1.id, role2.id, role3.id, role4.id]
						for role in user.roles:
							if role.id in col_list:
								await user.remove_roles(role)
						m = check_new_username(user)
						await user.add_roles(bg_role, age_role, sedula, role1, role2, role3, role4) # add role
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
						embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
						await ctx.send(content=f"{user.mention}", embed=embed)
						try:
							channel = await self.client.fetch_channel(961504364269301764)
							await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
						except:
							pass
				else:
					await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def ba(self, ctx, user: Member=None, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.ba [user]`.\nE.g; `.ba @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			if role.id == 1001430287143669800:
				if suffix == None:
					#reg = db.record("SELECT * FROM main WHERE UserID = ?", user.id)
					#if reg is None:
					#	db.execute("INSERT INTO main (UserID) VALUES (?)", user.id)
					#else:
					#	luc = db.field("SELECT MemLevelUpChecker FROM main WHERE UserID = ?", user.id)
					#	role = mem_role_checker(luc)
					#	if role is not None:
					#		await user.add_roles(role)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169029601144862), Object(961969926279659560)
					role1, role2 = Object(962161356486901770), Object(962164001419173888) # LAPAGAN, PAYASO
					members = [user.id for user in ctx.guild.members if bg_role in user.roles]
					m = check_new_username(user)
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
					embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
					await ctx.send(content=f"{user.mention}", embed=embed)
					try:
						embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server")
						embed_.set_image(url=f"{random.choice(welcome_list)}")
						await user.send(embed=embed_)
					except:
						pass
					return
				elif suffix.lower() == "--fix":
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169029601144862), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					members = [user.id for user in ctx.guild.members if bg_role in user.roles]
					if r_role in user.roles:
						await ctx.send(f"{user.mention} is not yet verified! You can't use `--fix` extension with unverified user!")
					else:
						col_list = [bg_role.id, r_role.id, age_role.id, sedula.id, role1.id, role2.id, role3.id, role4.id]
						for role in user.roles:
							if role.id in col_list:
								await user.remove_roles(role)
						await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
						m = check_new_username(user)
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
						embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
						await ctx.send(content=f"{user.mention}", embed=embed)
						try:
							embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server")
							embed_.set_image(url=f"{random.choice(welcome_list)}")
							await user.send(embed=embed_)
						except:
							pass
						return
				else:
					await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def bb(self, ctx, user: Member=None, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.bb [user]`.\nE.g; `.bb @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			if role.id == 1001430287143669800:
				if suffix == None:
					#reg = db.record("SELECT * FROM main WHERE UserID = ?", user.id)
					#if reg is None:
					#	db.execute("INSERT INTO main (UserID) VALUES (?)", user.id)
					#else:
					#	luc = db.field("SELECT GenLevelUpChecker FROM main WHERE UserID = ?", user.id)
					#	role = gen_role_checker(luc)
					#	if role is not None:
					#		await user.add_roles(role)
					async with aiohttp.ClientSession() as session:
						async with session.get(random.choice(welcome_list)) as response:
							data = await response.read()
					img = BytesIO(data)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169029601144862), Object(961969926279659560)
					role1, role2 = Object(962161205106069624), Object(962166066455384116) # LIPUNAN, BULWAGAN
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
					m = check_new_username(user)
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
					embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
					await ctx.send(content=f"{user.mention}", embed=embed)
					try:
						channel = await self.client.fetch_channel(961504364269301764)
						await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
					except:
						pass
					try:
						embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server")
						embed_.set_image(url=f"{random.choice(welcome_list)}")
						await user.send(embed=embed_)
					except:
						pass
					return
				elif suffix.lower() == "--fix":
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169029601144862), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					if r_role in user.roles:
						await ctx.send(f"{user.mention} is not yet verified! You can't use `--fix` extension with unverified user!")
					else:
						col_list = [bg_role.id, r_role.id, age_role.id, sedula.id, role1.id, role2.id, role3.id, role4.id]
						m = check_new_username(user)
						for role in user.roles:
							if role.id in col_list:
								await user.remove_roles(role)
						await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
						embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
						await ctx.send(content=f"{user.mention}", embed=embed)
						try:
							channel = await self.client.fetch_channel(961504364269301764)
							await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
						except:
							pass
						try:
							embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server")
							embed_.set_image(url=f"{random.choice(welcome_list)}")
							await user.send(embed=embed_)
						except:
							pass
						return
				else:
					await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def bc(self, ctx, user: Member=None, suffix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.bc [user]`.\nE.g; `.bc @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			if role.id == 1001430287143669800:
				if suffix == None:
					reg = db.record("SELECT * FROM main WHERE UserID = ?", user.id)
					if reg is None:
						db.execute("INSERT INTO main (UserID) VALUES (?)", user.id)
					else:
						luc, guc = db.record("SELECT GenLevelUpChecker, MemLevelUpChecker FROM main WHERE UserID = ?", user.id)
						role_1 = gen_role_checker(luc)
						role_2 = mem_role_checker(guc)
						if role_1 is not None:
							await user.add_roles(role_1)
						if role_2 is not None:
							await user.add_roles(role_2)
					async with aiohttp.ClientSession() as session:
						async with session.get(random.choice(welcome_list)) as response:
							data = await response.read()
					img = BytesIO(data)
					emb_img = random.choice(welcome_list)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169029601144862), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2, role3, role4) # add role
					m = check_new_username(user)
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
					embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
					await ctx.send(content=f"{user.mention}", embed=embed)
					try:
						channel = await self.client.fetch_channel(961504364269301764)
						await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
					except:
						pass
					try:
						embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server")
						embed_.set_image(url=f"{random.choice(welcome_list)}")
						await user.send(embed=embed_)
					except:
						pass
					return
				elif suffix.lower() == "--fix":
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169029601144862), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					if r_role in user.roles:
						await ctx.send(f"{user.mention} is not yet verified! You can't use `--fix` extension with unverified user!")
					else:
						col_list = [bg_role.id, r_role.id, age_role.id, sedula.id, role1.id, role2.id, role3.id, role4.id]
						for role in user.roles:
							if role.id in col_list:
								await user.remove_roles(role)
						await user.add_roles(bg_role, age_role, sedula, role1, role2, role3, role4) # add role
						m = check_new_username(user)
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {m}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
						embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
						await ctx.send(content=f"{user.mention}", embed=embed)
						try:
							channel = await self.client.fetch_channel(961504364269301764)
							await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
						except:
							pass
						try:
							embed_ = Embed(color=0x2f3136, description=f"**Maligayang pagdating sa KBL! Narito ang mga channels na pwede mong puntahan:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server")
							embed_.set_image(url=f"{random.choice(welcome_list)}")
							await user.send(embed=embed_)
						except:
							pass
						return
				else:
					await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command(aliases=["alvl", "add-level"])
	async def addlevel(self, ctx, user: Member=None, amount: Union[int, str]=None, prefix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help add-level` to guide you in adding levels!")
			else:
				if isinstance(amount, int):
					if prefix in ["--memes", "--meme", "--m"]:
						amt = db.field("SELECT MemesLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET MemesXP = 0, MemesLevel = MemesLevel + ?, MemLevelLimit = ? WHERE UserID = ?", amount, (amt+amount)*100, user.id)
						await ctx.send(f"{user.mention} was added by **{amount:,}** in Lapagan Category.\n\n{user.mention}'s level: {amt+amount:,}")
					else:
						amt = db.field("SELECT GeneralLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = GeneralLevel + ?, GenLevelLimit = ? WHERE UserID = ?", amount, (amt+amount)*100, user.id)
						await ctx.send(f"{user.mention} was added by **{amount:,}** in Lipunan Category.\n\n{user.mention}'s level: {amt+amount:,}")
				else:
					if amount in ["--memes", "--meme", "--m"]:
						amt = db.field("SELECT MemesLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET MemesXP = 0, MemesLevel = MemesLevel + 1, MemLevelLimit = ? WHERE UserID = ?", (amt+1)*100, user.id)
						await ctx.send(f"{user.mention} was added by **1** in Lapagan Category.\n\n{user.mention}'s level: {amt+1:,}")
					else:
						amt = db.field("SELECT GeneralLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = GeneralLevel + 1, GenLevelLimit = ? WHERE UserID = ?", (amt+1)*100, user.id)
						await ctx.send(f"{user.mention} was added by **1** in Lipunan Category.\n\n{user.mention}'s level: {amt+1:,}")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["rlvl", "remove-level"])
	async def removelevel(self, ctx, user: Member=None, amount: Union[int, str]=None, prefix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help remove-level` to guide you in removing levels!")
			else:
				if isinstance(amount, int):
					if prefix in ["--memes", "--meme", "--m"]:
						amt = db.field("SELECT MemesLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET MemesXP = 0, MemesLevel = MemesLevel - ?, MemLevelLimit = ? WHERE UserID = ?", amount, (amt-amount)*100, user.id)
						await ctx.send(f"{user.mention}'s current level was decreased by **{amount:,}** in Lapagan Category.\n\n{user.mention}'s level: {amt-amount}")
					else:
						amt = db.field("SELECT GeneralLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = GeneralLevel - ?, GenLevelLimit = ? WHERE UserID = ?", amount, (amt-amount)*100, user.id)
						await ctx.send(f"{user.mention}'s current level was decreased by **{amount:,}** in Lipunan Category.\n\n{user.mention}'s level: {amt-amount}")
				else:
					if amount in ["--memes", "--meme", "--m"]:
						amt = db.field("SELECT MemesLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET MemesXP = 0, MemesLevel = MemesLevel - 1, MemLevelLimit = ? WHERE UserID = ?", (amt-1)*100, user.id)
						await ctx.send(f"{user.mention}'s current level was decreased by **1** in Lapagan Category.\n\n{user.mention}'s level: {amt-1}")
					else:
						amt = db.field("SELECT GeneralLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = GeneralLevel - 1, GenLevelLimit = ? WHERE UserID = ?", (amt-1)*100, user.id)
						await ctx.send(f"{user.mention}'s current level was decreased by **1** in Lipunan Category.\n\n{user.mention}'s level: {amt-1}")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["slvl", "set-level"])
	async def setlevel(self, ctx, user: Member=None, amount: Union[int, str]=None, prefix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help set-level` to guide you in setting levels!")
			else:
				if isinstance(amount, int):
					if prefix in ["--memes", "--meme", "--m"]:
						amt = db.field("SELECT MemesLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET MemesXP = 0, MemesLevel = ?, MemLevelLimit = ? WHERE UserID = ?", amount, amt*100, user.id)
						await ctx.send(f"{user.mention}'s level was set to **Level {amount:,}** in Lapagan Category.\n\n{user.mention}'s level: {amt+amount:,}")
					else:
						amt = db.field("SELECT GeneralLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = ?, GenLevelLimit = ? WHERE UserID = ?", amount, amt*100, user.id)
						await ctx.send(f"{user.mention}'s level was set to **Level {amount:,}** in Lipunan Category.\n\n{user.mention}'s level: {amount:,}")
				else:
					if amount in ["--memes", "--meme", "--m"]:
						amt = db.field("SELECT MemesLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET MemesXP = 0, MemesLevel = 1, MemLevelLimit = ? WHERE UserID = ?", 100, user.id)
						await ctx.send(f"{user.mention}'s level was set to **Level 1** in Lapagan Category.\n\n{user.mention}'s level: 1")
					else:
						amt = db.field("SELECT GeneralLevel FROM main WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = 1, GenLevelLimit = ? WHERE UserID = ?", 100, user.id)
						await ctx.send(f"{user.mention}'s level was set to **Level 1** in Lipunan Category.\n\n{user.mention}'s level: 1")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["sxp", "set-xp"])
	async def setxp(self, ctx, user: Member=None, amount: Union[int, str]=None, prefix=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help set-xp` to guide you in setting level xps!")
			else:
				if isinstance(amount, int):
					if prefix in ["--memes", "--meme", "--m"]:
						amt = db.field("SELECT MemLevelLimit FROM main WHERE UserID = ?", user.id)
						if amount > amt:
							await ctx.send(f"You've reached above {user.mention}'s maximum xp. Check their `.rank` first before continuing.")
						else:
							db.execute("UPDATE main SET MemesXP = ? WHERE UserID = ?", amount, user.id)
							await ctx.send(f"{user.mention}'s xp was set to **{amount:,}** in Lapagan Category.\n\n{user.mention}'s XP: {amount:,}")
					else:
						amt = db.field("SELECT GenLevelLimit FROM main WHERE UserID = ?", user.id)
						if amount > amt:
							await ctx.send(f"You've reached above {user.mention}'s maximum xp. Check their `.rank` first before continuing.")
						else:
							db.execute("UPDATE main SET GeneralXP = ? WHERE UserID = ?", amount, user.id)
							await ctx.send(f"{user.mention}'s xp was set to **{amount:,}** in Lipunan Category.\n\n{user.mention}'s XP: {amount:,}")
				else:
					if amount in ["--memes", "--meme", "--m"]:
						amt = db.field("SELECT MemLevelLimit FROM main WHERE UserID = ?", user.id)
						if amount > amt:
							await ctx.send(f"You've reached above {user.mention}'s maximum xp. Check their `.rank` first before continuing.")
						else:
							db.execute("UPDATE main SET MemesXP = ? WHERE UserID = ?", amt, user.id)
							await ctx.send(f"{user.mention}'s xp was set to its Maximum Limit in Lapagan Category.\n\n{user.mention}'s XP: {amt:,}")
					else:
						amt = db.field("SELECT GenLevelLimit FROM main WHERE UserID = ?", user.id)
						if amount > amt:
							await ctx.send(f"You've reached above {user.mention}'s maximum xp. Check their `.rank` first before continuing.")
						else:
							db.execute("UPDATE main SET GeneralXP = ? WHERE UserID = ?", amt, user.id)
							await ctx.send(f"{user.mention}'s xp was set to its Maximum Limit in Lipunan Category.\n\n{user.mention}'s XP: {amt:,}")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["slp", "set-lp"])
	async def setlp(self, ctx, user: Member=None, amount: int=1):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help set-lp` to guide you in setting LPs!")
			else:
				db.execute("UPDATE main SET LigtasPoints = ? WHERE UserID = ?", amount, user.id)
				await ctx.send(f"{user.mention}'s LP was set to **{amount:,}**.\n\n{user.mention}'s XP: {amount:,}")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["clp", "clear-lp"])
	async def clearlp(self, ctx, user: Union[Member, str]=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help clear-lp` to guide you in clearing LPs!")
			else:
				db.execute("UPDATE main SET LigtasPoints = 0 WHERE UserID = ?", user.id)
				await ctx.send(f"{user.mention}'s LP was successfully reset to 0.\n\n{user.mention}'s LP: 1")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["partner", "partnered"])
	async def partnership(self, ctx, user: Member=None, server_name: str=None, server_link: str=None, *, description: str=None):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			new_list = []
			partners = db.records("SELECT UserID, ServerPartnership, ServerPartnerName, ServerPartnerLink, ServerPartnerDesc FROM main WHERE ServerPartnership > 0 AND ServerPartnerName != ? AND ServerPartnerLink != ? AND ServerPartnerDesc != ? ORDER BY ServerPartnership DESC", "None", "None", "None")
			if len(partners) == 0:
				await ctx.send("There are no current partnered servers...yet.")
			else:
				for partner in partners:
					new_list.append(f"• [{partner[2]}]({partner[3]}) — <@{partner[0]}>\n<:replycontinued:1094562362624856084> Added <t:{partner[1]}:R>\n<:reply:1094561143911100447> {partner[4]}")
				paginator = PartnershipPages(entries=new_list, ctx=ctx)
				await paginator.run()
		elif server_name is None:
			partner_time, partner_name, partner_link, partner_desc = db.record("SELECT ServerPartnership, ServerPartnerName, ServerPartnerLink, ServerPartnerDesc FROM main WHERE UserID = ?", user.id)
			if partner_time == 0 and partner_name == "None" and partner_link == None and partner_desc == None:
				await ctx.send(f"{user.mention} is not currently a partnered user...yet.")
			else:
				embed=Embed(color=0x2f3136, title=partner_name, url=partner_link, description=f"*{partner_desc}*\n\n• Added <t:{partner_time}:R>")
				await ctx.send(embed=embed)
		else:
			if ctx.author.guild_permissions.administrator:
				server_partner_name = db.field("SELECT ServerPartnerName FROM main WHERE UserID = ?", user.id)
				if server_name.lower() == "--remove":
					if server_partner_name == "None":
						await ctx.send(f"{user.mention} is currently not an official partnered user.")
					else:
						lp = db.field("SELECT LigtasPoints FROM main WHERE UserID = ?", user.id)
						if lp < 100:
							db.execute("UPDATE main SET LigtasPoints = 0 WHERE UserID = ?", user.id)
						else:
							db.execute("UPDATE main SET LigtasPoints = LigtasPoints - 100 WHERE UserID = ?", user.id)
						db.execute("UPDATE main SET ServerPartnership = 0, ServerPartnerName = ?, ServerPartnerLink = ? WHERE UserID = ?", "None", "None", user.id)
						await ctx.send(f"Successfully removed {user.mention}'s partnership status.")
				else:
					if server_partner_name == "None":
						if server_link is None:
							await ctx.send("Please provide a valid `discord.gg` link!")
						else:
							if description is None:
								await ctx.send("Please provide a valid **description** first! A good server has its description of what does it do/offer.")
							else:
								try:
									inv = await self.client.fetch_invite(server_link)
									db.execute("UPDATE main SET ServerPartnership = ?, ServerPartnerName = ?, ServerPartnerLink = ?, ServerPartnerDesc = ?, LigtasPoints = LigtasPoints + 100 WHERE UserID = ?", int(time.time()), server_name, server_link, description, user.id)
									await ctx.send(f"Successfully set {user.mention} as the official partnered user between **Bobong Lipunan** and **{server_name}**!\n\nDiscord Link: {server_link}")
								except:
									await ctx.send(f"The server link you provided ({server_link}) might be invalid, expired, or cannot be found by the bot. Please ensure that the invite link is set in public then try again.")
					else:
						await ctx.send(f"{user.mention} is already added as representative of **{server_partner_name}**! Try adding another representative instead.")
			else:
				await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["approved", "apr"])
	async def approve(self, ctx, key: str=None, *, remarks="No remarks."):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if key is None:
				await ctx.send("You can't approve an empty key! Please provide a key first! It can be seen via `.astarboard`")
			else:
				try:
					starboard_list = db.field("SELECT StarboardList FROM global")
					starboard = ast.literal_eval(starboard_list)
					id_ = starboard[key][0]
					msg = await ctx.channel.fetch_message(id_)
					user_starboard = db.field("SELECT StarboardList FROM main WHERE UserID = ?", msg.author.id)
					_starboard = ast.literal_eval(user_starboard)
					_starboard[key][1] = "🟢 Approved"
					_starboard[key][2] = remarks
					del starboard[key]
					db.execute("UPDATE global SET StarboardList = ?", f"{starboard}")
					db.execute("UPDATE main SET StarboardList = ? WHERE UserID = ?", f"{_starboard}", msg.author.id)
					post = self.client.get_channel(1048837480700465202)
					m = check_new_username(msg.author)
					try:
						await msg.author.send(f"Your entry/post ({msg.jump_url}) has been **Approved**! It can now be seen in <#1048837480700465202>.\n\nAdmin Remarks: {remarks}")
					except:
						pass
					try:
						await post.send(content=f"Posted by: {m}\n\n{msg.content}", attachments=msg.attachments)
					except:
						await post.send(content=f"Posted by: {m}\n\n{msg.content}")
					await ctx.send(f"Succesfully posted on {post.mention}.")
				except:
					await ctx.send("Invalid key. Please try again.")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["rejected", "rej"])
	async def reject(self, ctx, key: str=None, *, remarks="No remarks."):
		await ctx.trigger_typing()
		m, md = db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if key is None:
				await ctx.send("You can't approve an empty key! Please provide a key first! It can be seen via `.astarboard`")
			else:
				try:
					starboard_list = db.field("SELECT StarboardList FROM global")
					starboard = ast.literal_eval(starboard_list)
					id_ = starboard[key][0]
					msg = await ctx.channel.fetch_message(id_)
					user_starboard = db.field("SELECT StarboardList FROM main WHERE UserID = ?", msg.author.id)
					_starboard = ast.literal_eval(user_starboard)
					_starboard[key][1] = "🔴 Rejected"
					_starboard[key][2] = remarks
					del starboard[key]
					db.execute("UPDATE global SET StarboardList = ?", f"{starboard}")
					db.execute("UPDATE main SET StarboardList = ? WHERE UserID = ?", f"{_starboard}", msg.author.id)
					m = check_new_username(msg.author)
					try:
						await msg.author.send(f"Your entry/post ({msg.jump_url}) has been **Rejected**!.\n\nAdmin Remarks: {remarks}")
					except:
						pass
				except:
					await ctx.send("Invalid key. Please try again.")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

def setup(client):
	client.add_cog(kbl_1(client))