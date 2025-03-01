import time, random, aiohttp
from disnake import Embed, Member, File, Object
from disnake.ext import commands
from kbl.db import db
from io import BytesIO
from typing import Union

from properties.funcs import help_, convert_duration, ping_checker

welcome_list = open("./properties/welcome_list.txt").readlines()


"""

	Please check IMPORTANT.md for the layout and descriptions of other commands. Some are very simple, and some are complex.
	For existing errors, check ERRORS.md.
	For overall and general information about this project, database schema, and more, check README.md.

	Goodluck to those who will use this once-so-called 'masterpiece' for their discord server.

	Sincerely,
		raianxh_

		
	PS: Commands (ma, mb, mc, ba, bb, bc, setlp, clearlp) are all catered to KBL Discord Server. If you wish to use this in your own server, you need to tweak it a little and replace some objects with your own.
		You must be fluent to read Python and Discord Developer. Otherwise, feel free to remove/comment it.

"""


class admin(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.client.help_command = None

	@commands.Cog.listener()
	async def on_ready(self):
		print("KBL (Admin) is loaded.")
		global startTime
		startTime = int(time.time())

	@commands.command()
	async def help(self, ctx, command=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		await help_(command, ctx)

	@commands.command()
	async def ping(self, ctx):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		new_list = convert_duration(int(round(time.time()-startTime)))
		timestamp = " ".join([item for item in new_list])
		emoj = ping_checker(round(self.client.latency * 1000))
		mm = "🟢 Enabled"
		embed=Embed(color=0x2f3136, description=f"**Ping**: {emoj} {round(self.client.latency * 1000)}ms\n**Uptime**: {timestamp}\n**Status**: {mm}")
		await ctx.send(embed=embed)

	# @commands.command()
	# async def reload(self, ctx, *, extension=None):
		"""
			This command is for reloading the file. If you know this command, uncomment it. Otherwise, reload the whole project after changes.

			Replace "603256030742183959" with your Discord ID for technical purposes.
		"""
	# 	if ctx.author.id in [603256030742183959, 697129372867625054]:
	# 		if ctx.author.id == 697129372867625054:
	# 			mem = await ctx.guild.fetch_member(603256030742183959)
	# 			await mem.send(f"thethimteam#1890 commences a maintenance mode!")
	# 		await ctx.trigger_typing()
	# 		if extension is None:
	# 			await ctx.send("Please put a `extension` name!")
	# 		else:
	# 			try:
	# 				self.client.reload_extension(f"{extension}")
	# 				await ctx.send(f"Successfully reloaded `{extension}` file.")
	# 			except:
	# 				await ctx.send(f"Incorrect extension file ({extension})")

	@commands.command()
	async def maintenance(self, ctx, command=None):
		"""
			Replace "603256030742183959" with your Discord ID for technical purposes.
		"""
		await ctx.trigger_typing()
		if ctx.author.id in [603256030742183959, 697129372867625054]:
			if ctx.author.id == 697129372867625054:
				mem = await ctx.guild.fetch_member(603256030742183959)
				await mem.send(f"thethimteam#1890 commences a maintenance mode!")
			await ctx.trigger_typing()
			if command == "--start":
				await db.execute("UPDATE global SET Maintenance = 1, MaintenanceDuration = %s", int(time.time()))
				embed=Embed(color=0x2f3136, title=f"Scheduled Maintenance (<t:{int(time.time())+3600}:R>)", description=f"Good day! <@1050024676627320872> is now in maintenance mode. During the maintenance period all commands will be disabled for a brief period of time. This is to safely deploy new updates to the bot.\n\nETA: <t:{int(time.time())+3600}:R> (<t:{int(time.time())+3600}:t>)")
				return await ctx.send(embed=embed)
			elif command == "--done":
				await db.execute("UPDATE global SET Maintenance = 0, MaintenanceDuration = 0")
				embed=Embed(color=0x2f3136, title=f"Scheduled Maintenance (Done)", description="Good evening! <@1050024676627320872>'s maintenance has been lifted and all commands are now enabled for usage.")
				return await ctx.send(embed=embed)
			else:
				md = await db.record("SELECT MaintenanceDuration FROM global")
				if md is None:
					await db.execute("UPDATE global SET MaintenanceDuration = 0")
				if md[-1] > 0:
					embed=Embed(color=0x2f3136, title=f"Scheduled Maintenance (<t:{md[-1]}:R>)", description=f"Good day! <@1050024676627320872> is scheduled for maintenance <t:{md[-1]}:R> (<t:{md[-1]}:t>). This is to safely deploy new updates to the bot.\n\nETA: <t:{md[-1]+8600}:R> (<t:{md[-1]+8600}:t>)")
					return await ctx.send(embed=embed)
				else:
					return await ctx.send(f"<@1050024676627320872> is not currently in maintenance!")
		else:
			md = await db.record("SELECT MaintenanceDuration FROM global")
			if md[-1] > 0:
				embed=Embed(color=0x2f3136, title=f"Scheduled Maintenance (<t:{md[-1]}:R>)", description=f"Good day! <@1050024676627320872> is scheduled for maintenance <t:{md[-1]}:R> (<t:{md[-1]}:t>). This is to safely deploy new updates to the bot.\n\nETA: <t:{md[-1]+8600}:R> (<t:{md[-1]+8600}:t>)")
				await ctx.send(embed=embed)
			else:
				await ctx.send(f"<@1050024676627320872> is not currently in maintenance!")

	@commands.command()
	async def ma(self, ctx, user: Member=None, suffix=None):
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.ma [user]`.\nE.g; `.ma @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			await ctx.trigger_typing()
			if role.id == 1001430287143669800:
				if suffix == None:
					reg = await db.record("SELECT * FROM main WHERE UserID = %s", user.id)
					if reg is None:
						await db.execute("INSERT INTO main (UserID) VALUES (%s)", user.id)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2 = Object(962161356486901770), Object(962164001419173888) # LAPAGAN, PAYASO
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
						await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
						embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
						return await ctx.send(content=f"{user.mention}", embed=embed)
				else:
					return await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		# await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def mb(self, ctx, user: Member=None, suffix=None):
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.mb [user]`.\nE.g; `.mb @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			await ctx.trigger_typing()
			if role.id == 1001430287143669800:
				if suffix == None:
					reg = await db.record("SELECT * FROM main WHERE UserID = %s", user.id)
					if reg is None:
						await db.execute("INSERT INTO main (UserID) VALUES (%s)", user.id)
					async with aiohttp.ClientSession() as session:
						async with session.get(random.choice(welcome_list)) as response:
							data = await response.read()
					img = BytesIO(data)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2 = Object(962161205106069624), Object(962166066455384116) # LIPUNAN, BULWAGAN
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.mc [user]`.\nE.g; `.mc @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			await ctx.trigger_typing()
			if role.id == 1001430287143669800:
				if suffix == None:
					reg = await db.record("SELECT * FROM main WHERE UserID = %s", user.id)
					if reg is None:
						await db.execute("INSERT INTO main (UserID) VALUES (%s)", user.id)
					async with aiohttp.ClientSession() as session:
						async with session.get(random.choice(welcome_list)) as response:
							data = await response.read()
					img = BytesIO(data)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169020151394394), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2, role3, role4) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
						await user.add_roles(bg_role, age_role, sedula, role1, role2, role3, role4) # add role
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
						embed.set_image(url=f"{random.choice(welcome_list)}").set_footer(text=f"Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", icon_url=user.display_avatar.url).set_thumbnail(url=user.display_avatar.url)
						await ctx.send(content=f"{user.mention}", embed=embed)
						try:
							channel = await self.client.fetch_channel(961504364269301764)
							await channel.send(f"<@&1001430726471843951> | Welcome sa ating bagong user, {user.mention} ({user.display_name})! Ikaw ang ika-{len(members)+1:,} na miyembro ng KBL!", file=File(img, "welcome.gif"))
						except:
							pass
						return
				else:
					return await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def ba(self, ctx, user: Member=None, suffix=None):
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.ba [user]`.\nE.g; `.ba @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			await ctx.trigger_typing()
			if role.id == 1001430287143669800:
				if suffix == None:
					reg = await db.record("SELECT * FROM main WHERE UserID = %s", user.id)
					if reg is None:
						await db.execute("INSERT INTO main (UserID) VALUES (%s)", user.id)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169029601144862), Object(961969926279659560)
					role1, role2 = Object(962161356486901770), Object(962164001419173888) # LAPAGAN, PAYASO
					members = [user.id for user in ctx.guild.members if bg_role in user.roles]
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
					return await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def bb(self, ctx, user: Member=None, suffix=None):
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.bb [user]`.\nE.g; `.bb @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			await ctx.trigger_typing()
			if role.id == 1001430287143669800:
				if suffix == None:
					reg = await db.record("SELECT * FROM main WHERE UserID = %s", user.id)
					if reg is None:
						await db.execute("INSERT INTO main (UserID) VALUES (%s)", user.id)
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
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
						for role in user.roles:
							if role.id in col_list:
								await user.remove_roles(role)
						await user.add_roles(bg_role, age_role, sedula, role1, role2) # add role
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
					return await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command()
	async def bc(self, ctx, user: Member=None, suffix=None):
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if user is None:
			return await ctx.send("Invalid usage of command. Do `.bc [user]`.\nE.g; `.bc @thethimteam#1890`\n\nDo take note this only works on users with `Tanod` role!")
		for role in ctx.author.roles:
			await ctx.trigger_typing()
			if role.id == 1001430287143669800:
				if suffix == None:
					reg = await db.record("SELECT * FROM main WHERE UserID = %s", user.id)
					if reg is None:
						await db.execute("INSERT INTO main (UserID) VALUES (%s)", user.id)
					async with aiohttp.ClientSession() as session:
						async with session.get(random.choice(welcome_list)) as response:
							data = await response.read()
					img = BytesIO(data)
					bg_role, r_role, age_role, sedula = Object(961967298955079740), Object(961964769772961822), Object(962169029601144862), Object(961969926279659560)
					role1, role2, role3, role4 = Object(962161356486901770), Object(962164001419173888), Object(962161205106069624), Object(962166066455384116) # BOTH
					bg_check = ctx.guild.get_role(961967298955079740)
					members = [user.id for user in ctx.guild.members if bg_check in user.roles]
					await user.remove_roles(r_role) # remove role
					await user.add_roles(bg_role, age_role, sedula, role1, role2, role3, role4) # add role
					embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
						embed=Embed(color=0x2f3136, title=f"Approved ka na, {user.name}!", description=f"**Heto ang ilan sa mga pwede mong puntahan sa server:**\n\n<#961503388401561620> for info & rules\n<#961875184703385600> for roles\n<#1026473207995305984> for forums\n<#961504020508340294> for memes\n<#961504364269301764> for general chatting\n<#961504384636846090> for games\n<#961805879680839741> for raising concerns around the server\n\nKung wala nang ibang katanungan ay maaari mo nang iclose ang ticket na ito ({ctx.channel.mention}). Enjoy po.")
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
					return await ctx.send("Wrong use of extension. The available extensions are: `--fix`.\n\nUsage: `.ma <user> --fix` (use this command if you made a mistake on placing a role)")
		await ctx.send("You cannot run this command without **Tanod** role!")

	@commands.command(aliases=["alvl", "add-level"])
	async def addlevel(self, ctx, user: Member=None, amount: int=1):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help add-level` to guide you in adding levels!")
			else:
				amt = await db.field("SELECT GeneralLevel FROM main WHERE UserID = %s", user.id)
				await db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = GeneralLevel + %s, GenLevelLimit = %s WHERE UserID = %s", amount, (amt+amount)*100, user.id)
				await ctx.send(f"{user.mention} was added by **{amount:,}**.\n\n{user.mention}'s level: {amt+amount:,}")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["rlvl", "remove-level"])
	async def removelevel(self, ctx, user: Member=None, amount: int=1):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help remove-level` to guide you in removing levels!")
			else:
				amt = await db.field("SELECT GeneralLevel FROM main WHERE UserID = %s", user.id)
				await db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = GeneralLevel - %s, GenLevelLimit = %s WHERE UserID = %s", amount, (amt-amount)*100, user.id)
				await ctx.send(f"{user.mention}'s current level was decreased by **{amount:,}**.\n\n{user.mention}'s level: {amt-amount}")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["slvl", "set-level"])
	async def setlevel(self, ctx, user: Member=None, amount: int=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help set-level` to guide you in setting levels!")
			else:
				if amount is not None:
					amt = await db.field("SELECT GeneralLevel FROM main WHERE UserID = %s", user.id)
					await db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = %s, GenLevelLimit = %s WHERE UserID = %s", amount, amt*100, user.id)
					await ctx.send(f"{user.mention}'s level was set to **Level {amount:,}**.\n\n{user.mention}'s level: {amount:,}")
				else:
					amt = await db.field("SELECT GeneralLevel FROM main WHERE UserID = %s", user.id)
					await db.execute("UPDATE main SET GeneralXP = 0, GeneralLevel = 1, GenLevelLimit = %s WHERE UserID = %s", 100, user.id)
					await ctx.send(f"{user.mention}'s level was set to **Level 1**.\n\n{user.mention}'s level: 1")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["sxp", "set-xp"])
	async def setxp(self, ctx, user: Member=None, amount: int=1):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help set-xp` to guide you in setting level xps!")
			else:
				amt = await db.field("SELECT GenLevelLimit FROM main WHERE UserID = %s", user.id)
				if amount > amt:
					await ctx.send(f"You've reached above {user.mention}'s maximum xp. Check their `.rank` first before continuing.")
				else:
					await db.execute("UPDATE main SET GeneralXP = %s WHERE UserID = %s", amt, user.id)
					await ctx.send(f"{user.mention}'s xp was set to its Maximum Limit.\n\n{user.mention}'s XP: {amt:,}")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["slp", "set-lp"])
	async def setlp(self, ctx, user: Member=None, amount: int=1):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help set-lp` to guide you in setting LPs!")
			else:
				await db.execute("UPDATE main SET LigtasPoints = %s WHERE UserID = %s", amount, user.id)
				await ctx.send(f"{user.mention}'s LP was set to **{amount:,}**.\n\n{user.mention}'s XP: {amount:,}")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

	@commands.command(aliases=["clp", "clear-lp"])
	async def clearlp(self, ctx, user: Union[Member, str]=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if ctx.author.guild_permissions.administrator:
			if user is None:
				await ctx.send(f"Use `.help clear-lp` to guide you in clearing LPs!")
			else:
				await db.execute("UPDATE main SET LigtasPoints = 0 WHERE UserID = %s", user.id)
				await ctx.send(f"{user.mention}'s LP was successfully reset to 0.\n\n{user.mention}'s LP: 1")
		else:
			await ctx.send("You cannot run this command without **Administrator** permissions!")

def setup(client):
	client.add_cog(admin(client))