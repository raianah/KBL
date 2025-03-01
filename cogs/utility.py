import time, datetime, humanize, aiohttp, pytz
from disnake.ext import commands
from disnake import Embed, Color, Member, Game, Streaming, Spotify, CustomActivity, File, Role
from disnake.errors import NotFound
from kbl.db import db
from typing import Union
from io import BytesIO

from properties.funcs import ShortPagination


"""

	Please check IMPORTANT.md for the layout and descriptions of other commands. Some are very simple, and some are complex.
	For existing errors, check ERRORS.md.
	For overall and general information about this project, database schema, and more, check README.md.

	Goodluck to those who will use this once-so-called 'masterpiece' for their discord server.

	Sincerely,
		raianxh_

		
	PS: Commands (botstats, channels, minecraft) are all catered to KBL Discord Server. If you wish to use this in your own server, you need to tweak it a little and replace some objects with your own.
		You must be fluent to read Python and Discord Developer. Otherwise, feel free to remove/comment it.

	PPS: Channels command is initially commented due to the fact that it generates too much process, drowning your server/computer you're running in.
		 Re-enabling this might crash your computer, use it with caution.

"""

class utility(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("KBL (Utility) is loaded.")

	@commands.command(aliases=['ui', 'ako'])
	async def userinfo(self, ctx, user: Member=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		user = user or ctx.author
		new_list = []
		for activity in user.activities:
			if isinstance(activity, Game):
				try:
					act_timestamp = activity.start.timestamp()
					act_relative = datetime.timedelta(seconds=int(time()) - act_timestamp)
					act_humanize = humanize.naturaldelta(act_relative)
					new_list.append(f"• Playing {activity.name} {act_humanize} ago.")
				except:
					pass
			if isinstance(activity, Streaming):
				try:
					new_list.append(f"• Streaming LIVE on Twitch @ [{activity.twitch_name}]({activity.url}) playing {activity.game}.")
				except:
					pass
			if isinstance(activity, Spotify):
				try:
					new_list.append(f"• Listening to [{activity.artist} - {activity.title}]({activity.track_url})")
				except:
					pass
			if isinstance(activity, CustomActivity):
				try:
					new_list.append(f"• Custom Status: {activity.name}")
				except:
					pass
		if len(new_list) > 0:
			activities = "\n".join([f"{item}" for item in new_list])
		else:
			activities = "-"
		embed=Embed(color=0x2f3136).set_author(name=f"User Information | {user.name}", icon_url=user.display_avatar.url)
		if user.avatar != user.display_avatar:
			avatar = f"[{user.name}'s avatar]({user.avatar.url})\n[{user.name}'s server avatar]({user.display_avatar.url})"
		else:
			avatar = f"[{user.name}'s avatar]({user.avatar.url})"
		if user.id != ctx.author.id:
			embed.set_footer(text=f"Command executed by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
		else:
			embed.set_footer(text="Viewing your user information.", icon_url=user.display_avatar.url)
		member_join = int(user.joined_at.timestamp())
		member_create = int(user.created_at.timestamp())
		join_relative = datetime.timedelta(seconds=int(time.time() - member_join))
		create_relative = datetime.timedelta(seconds=int(time.time() - member_create))
		join_hum = humanize.naturaldelta(join_relative)
		create_hum = humanize.naturaldelta(create_relative)
		if bool(user.premium_since) == True:
			p_since = int(user.premium_since.timestamp())
			p_relative = datetime.timedelta(seconds=int(time.time()) - p_since)
			boost = f"{user.premium_since.date()}\n{humanize.naturaldelta(p_relative)} ago"
		else:
			boost = "Not yet boosted."
		embed.add_field(name="Name", value=f"{user.name}").add_field(name="Nickname", value=f"{user.mention}").add_field(name="Avatar", value=f"{avatar}")
		embed.add_field(name="Joined at", value=f"{user.joined_at.date()}\n{join_hum} ago").add_field(name="Created at", value=f"{user.created_at.date()}\n{create_hum} ago")
		embed.add_field(name="Boosted since", value=f"{boost}").add_field(name="Activities", value=f"{activities}", inline=False).set_thumbnail(url=user.avatar.url)
		await ctx.send(embed=embed)

	@commands.command(aliases=['mcc', 'mca'])
	async def minecraft(self, ctx, suffix=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		# return await ctx.send("**KBLCraft** will end for the meantime. You can reminisce your memories with your experience with KBLCraft here.\n\n- KBLCraft will return soon, via Season 4 with better gameplay to cater your creativity and competitiveness! Please wait for further announcements regarding KBLCraft Season 4.")
		if suffix is None:
			embed0=Embed(color=0x2f3136, description="**IP**: hardcore.kblcraft.xyz\n**Port**: 26542\n**Platform**: Java & Bedrock").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			embed1=Embed(color=0x2f3136, description="**IP**: smp.kblcraft.xyz\n**Port**: ?????\n**Platform**: Java & Bedrock").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			embed2=Embed(color=0x2f3136, description="**IP**: creative.kblcraft.xyz\n**Port**: ?????\n**Platform**: Java & Bedrock").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			embeds = [embed0, embed1, embed2]
			await ctx.send(embed=embed0, view=ShortPagination(ctx, embeds))
		elif suffix.lower() == "--start":
			embed=Embed(color=0x2f3136, description="- Login to your Minecraft Account (Cracked or Official)\n- Upon joining for the first time, a message containing random digits will appear in your screen. **DO NOT IGNORE IT**, as it will be your OTP to enter the server. **DO NOT SHARE YOUR OTP TO ANYONE!**\n  - Note that this process is ONE-TIME only. The second time you enter the server you are no longer needed to repeat this process.\n- Enter the code via <@830105506408169535>'s private message (DM) and wait for the response.\n\nIf something occurs, report it to the developer (@raianxh_)\n\n**NOTE**: If you verify your Discord account in Java, joining Bedrock will generate you another set of OTP, which will be denied by the bot due to limits. To unlink your account, use `/discord unlink` or contact the developer (@raianxh_)").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			await ctx.send(embed=embed)
		elif suffix.lower() == "--version":
			embed=Embed(color=0x2f3136, description="**__KBLCRAFT RECOMMENDED VERSIONS__**\n**JAVA**:\n- 1.21.x (current: 1.21.4)\n\n**BEDROCK**:\n- 1.21.x").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			embed.set_footer(text="Versions are updated as of January 2025.", icon_url=ctx.guild.me.avatar)
			await ctx.send(embed=embed)
		elif suffix.lower() == "--plugin":
			embed=Embed(color=0x2f3136, description="**__KBLCRAFT PLUGINS__**\n- [Clearlag 3.2.2](https://www.spigotmc.org/resources/clearlagg.68271/)\n- [CoreProtect 22.4](https://www.patreon.com/posts/104200466)\n- [DiscordSRV 1.28.0](https://modrinth.com/plugin/discordsrv/version/1.28.0)\n- [EssentialsX 2.21.0](https://essentialsx.net/downloads.html)\n- [Floodgate (Build#112)](https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot)\n- [Geyser (Build#629)](https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot)\n- [LuckPerms 5.4.141](https://download.luckperms.net/1556/bukkit/loader/LuckPerms-Bukkit-5.4.141.jar)\n- [MOTD 2.3.11](https://www.spigotmc.org/resources/motd-1-8-1-20.8390/download?version=530858)\n- [NoCheatPlus 3.16.0](https://www.spigotmc.org/resources/nocheatplus.26/download?version=202806)\n- [ViaBackwards 5.0.4](https://hangar.papermc.io/ViaVersion/ViaBackwards/versions/5.0.4)\n- [ViaVersion 5.0.5](https://hangar.papermc.io/ViaVersion/ViaVersion/versions/5.0.5)\n- [WorldEdit 7.3.7](https://dev.bukkit.org/projects/worldedit/files/latest)\n- [WorldGuard 7.0.12](https://dev.bukkit.org/projects/worldguard/files/latest)").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			embed.set_footer(text="Minecraft Server: Paper +1.21.4 | Plugins are updated as of October 19, 2024.", icon_url=ctx.guild.me.avatar)
			await ctx.send(embed=embed)
		elif suffix.lower() == "--status":
			async with aiohttp.ClientSession() as session:
				async with session.get("https://api.mcstatus.io/status/java/hardcore.kblcraft.xyz:26542") as data:
					dt = await data.json(content_type=None)
			ping_checker = {True: "🟢 **Online**", False: "🔴 **Offline**"}
			embed=Embed().set_author(name="KBLCRAFT STATUS", icon_url="https://i.imgur.com/X2FwCtu.png")
			try:
				embed.color = Color.green()
				embed.description = f"**Status**: {ping_checker[dt['online']]}\n**IP**: hardcore.kblcraft.xyz\n**Port**: {dt['port']}\n**Platform**: Java & Bedrock\n**Players:** {dt['players']['online']} / {dt['players']['max']}\n\nStatus retrieved <t:{int(dt['retrieved_at'] // 1000)}:R>"
				await ctx.send(embed=embed)
			except KeyError:
				embed.color = Color.red()
				embed.description = f"**Status**: {ping_checker[dt['online']]}\n**IP**: hardcore.kblcraft.xyz\n**Port**: {dt['port']}\n**Platform**: Java & Bedrock\n**Players:** Cannot retrieve.\n\nStatus retrieved <t:{int(dt['retrieved_at'] // 1000)}:R>"
				await ctx.send(embed=embed)
		else:
			embed0=Embed(color=0x2f3136, description="**IP**: hardcore.kblcraft.xyz\n**Port**: 26542\n**Platform**: Java & Bedrock").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			embed1=Embed(color=0x2f3136, description="**IP**: smp.kblcraft.xyz\n**Port**: ?????\n**Platform**: Java & Bedrock").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			embed2=Embed(color=0x2f3136, description="**IP**: creative.kblcraft.xyz\n**Port**: ?????\n**Platform**: Java & Bedrock").set_author(name="KBLCRAFT INFO", icon_url="https://i.imgur.com/X2FwCtu.png")
			embeds = [embed0, embed1, embed2]
			await ctx.send(embed=embed0, view=ShortPagination(ctx, embeds))

	@commands.command(aliases=['av'])
	async def avatar(self, ctx, user: Member=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		new_list = []
		user = user or ctx.author
		if user.avatar is None:
			data = BytesIO(await user.display_avatar.read())
			await ctx.send(content=f"Narito ang avatar ni {user.mention}.", file=File(data, f"avatar.png"))
		elif user.avatar is not None and user.avatar != user.display_avatar:
			data0, data1 = BytesIO(await user.avatar.read()), BytesIO(await user.display_avatar.read())
			if user.avatar.is_animated():
				file0 = File(data0, "avatar.gif")
			else:
				file0 = File(data0, "avatar.png")
			if user.display_avatar.is_animated():
				file1 = File(data1, "avatar.gif")
			else:
				file1 = File(data1, "avatar.png")
			new_list = [file0, file1]
			await ctx.send(content=f"Narito ang mga avatar ni {user.mention}.", files=new_list)
		else:
			data = BytesIO(await user.avatar.read())
			await ctx.send(content=f"Narito ang avatar ni {user.mention}.", file=File(data, f"avatar.png"))

	@commands.command(aliases=['event'])
	async def events(self, ctx, num: int=None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if int(time.time()) >= 1672502400 or ctx.author.id in [603256030742183959, 697129372867625054]:
			if len(ctx.guild.scheduled_events) == 0:
				return await ctx.send("There are no events to view. If you think this is an error, submit a ticket at <#961805879680839741>.")
			if num == None:
				new_list = []
				for i, event in enumerate(ctx.guild.scheduled_events):
					event_name, event_url, event_creator, event_usercount = event.name, event.url, event.creator, await event.fetch_users().flatten()
					event_description, event_image = event.description, event.image
					try:
						event_start_time, event_end_time = f"{event.scheduled_start_time.date()} (<t:{int(event.scheduled_start_time.timestamp())}:R>)", f"{event.scheduled_end_time.date()} (<t:{int(event.scheduled_end_time.timestamp())}:R>)"
					except AttributeError:
						event_start_time, event_end_time = f"{event.scheduled_start_time.date()} (<t:{int(event.scheduled_start_time.timestamp())}:R>)", "Not applicable"
					new_list.append(f"{i+1}. [{event.name}]({event.url}) • {len(event_usercount)} interested • {event_start_time} - {event_end_time}")
				event_list = f"\n".join([f"{item}" for item in new_list])
				embed=Embed(color=0x2f3136, title=f"{ctx.guild.name}'s Events", description=event_list).set_footer(text="To view an event in detail, use .event <num>.", icon_url=ctx.author.display_avatar.url)
				await ctx.send(embed=embed)
			else:
				event_list = ctx.guild.scheduled_events
				try:
					event = event_list[num-1]
					if event.channel == None:
						event_channel = event.entity_metadata.location
					else:
						event_channel = event.channel.mention
					event_name, event_url, event_creator, event_usercount = event.name, event.url, event.creator_id, await event.fetch_users().flatten()
					event_description, event_image = event.description, event.image
					try:
						event_start_time, event_end_time = f"{event.scheduled_start_time.date()}\n<t:{int(event.scheduled_start_time.timestamp())}:R>", f"{event.scheduled_end_time.date()}\n<t:{int(event.scheduled_end_time.timestamp())}:R>"
					except AttributeError:
						event_start_time, event_end_time = f"{event.scheduled_start_time.date()}\n<t:{int(event.scheduled_start_time.timestamp())}:R>", "Not applicable"
					embed=Embed(color=0x2f3136, title=f"Event - {event_name}", description=f"```yaml\n{event_description}```").set_image(url=event_image)
					embed.add_field(name="Creator", value=f"<@{event_creator}>").add_field(name="Interested", value=f"{len(event_usercount)}").add_field(name="Event Link", value=f"[Click here!]({event_url})")
					embed.add_field(name="Starts", value=f"{event_start_time}").add_field(name="Ends", value=f"{event_end_time}")
					embed.add_field(name="Channel/Location", value=event_channel)
					await ctx.send(embed=embed)
				except IndexError:
					await ctx.send("Wrong input. Please check the number aligned to the event. Use `.events` to view it in a list. If you think this is an error, submit a ticket at <#961805879680839741>.")
		else:
			await ctx.send(f"This feature is not yet open. Please wait <t:1672502400:R>.")

	@commands.command(aliases=['si'])
	async def serverinfo(self, ctx):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		guild_create = int(ctx.guild.created_at.timestamp())
		guild_relative = datetime.timedelta(seconds=int(time.time() - guild_create))
		guild_hum = humanize.naturaldelta(guild_relative)
		embed = Embed(color=0x2f3136).set_author(name=f"{ctx.guild.name.upper()}", icon_url=ctx.guild.icon).add_field(name="Server Owner", value=f"{ctx.guild.owner.mention}")
		embed.add_field(name="Server ID", value=f"{ctx.guild.id}").add_field(name="Server Icon", value=f"[Click here!]({ctx.guild.icon.url})").add_field(name="Server Created", value=f"{ctx.guild.created_at.date()}\n({guild_hum})")
		embed.add_field(name="Total Roles", value=f"{len(ctx.guild.roles)}").add_field(name="Total Emojis", value=f"{len(ctx.guild.emojis)}").add_field(name="Server Boost", value=f"{ctx.guild.premium_subscription_count} / 14")
		embed.add_field(name="Level Boost", value=f"Level {ctx.guild.premium_tier}").add_field(name="Channels", value=f"<:channel:972128066807668776> {len(ctx.guild.text_channels)} Text Channels\n<:voice_channel:973582959816867880> {len(ctx.guild.voice_channels)} Voice Channels\n<:stage_channel:973582936081317888> {len(ctx.guild.stage_channels)} Stage Channels")
		embed.add_field(name="Server Description", value=f"```yaml\n{ctx.guild.description}```", inline=False).set_thumbnail(url=ctx.guild.icon)
		await ctx.send(embed=embed)

	# @commands.command(aliases=['ch', 'channel'])
	# async def channels(self, ctx, channel: Union[TextChannel, VoiceChannel, ForumChannel, int, str] = None):
	# 	await ctx.trigger_typing()
	# 	m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
	# 	if m == 1:
	# 		return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
	# 	if channel is None:
	# 		await ctx.send("No input detected. Please input something.\n\n**Usage:**\n`.channel <channel>` / `.channel lapagan/lipunan/atbp`.")
	# 	if isinstance(channel, str):
	# 		if channel.lower() in ["lapagan", "channels", "channel", "channels role", "channel role", "lapagan roles", "lapagan role"]:
	# 			embed=Embed(color=0x2f3136, title="Lapagan (Memes)", description="Kategorya na kung saan makikita ang mga memes (oc/nakaw), at maghanap ng meme templates. Makukuha ang ganitong kategorya sa pagpasok dito sa server (pakilala).")
	# 			embed.add_field(name="Available Channels", value="<#1026473207995305984>\n<#961504084391772160>\n<#1045888798791323762>\n<#961504020508340294>").add_field(name="Category", value="Memes")
	# 			await ctx.send(embed=embed)
	# 		elif channel.lower() == "lipunan":
	# 			embed=Embed(color=0x2f3136, title="Lipunan (General)", description="Kategorya na kung saan maaari kang makipagkwentuhan kasama ang iba't-ibang miyembro ng server, makakuha ng manlalaro sa inyong mga laro, at magamit ang mga bots dito. Makukuha ang ganitong kategorya sa pagpasok dito sa server (pakilala).")
	# 			embed.add_field(name="Available Channels", value="<#961504364269301764>\n<#961504384636846090>\n<#961504419151745084>\n<#961504460008489022>").add_field(name="Category", value="General Chat\nPlayer Invites\nBot Usages")
	# 			await ctx.send(embed=embed)
	# 		elif channel.lower() == "atbp":
	# 			embed=Embed(color=0x2f3136, title="Lipunan (Leveled Up/Booster Channels)", description="Kategorya na kung saan maaari kang maglahad ng iyong hinanakit sa buhay (vent), i-share ang iyong life achievement, maliit man yan o malaki, makipag-usap sa mga miyembro sa larangan ng pulitika, o mga vids na hindi angkop sa edad 17 pababa. Makukuha ang ganitong kategorya sa sa pag-level up (Level 35) o sa pamamagitan ng pag-boost sa server.")
	# 			embed.add_field(name="Available Channels", value="<#961504917271478302>\n<#961504892298616842>\n<#961504983482785842>\n<#961505026747031572>\n<#961503708867330058> (Booster Channel)").add_field(name="Category", value="General Chat\nPlayer Invites\nBot Usages")
	# 			await ctx.send(embed=embed)
	# 		else:
	# 			await ctx.send("Invalid input. Please choose from the following prompts:\nlapagan, lipunan, atbp\n\n**Usage**:\n`.channel atbp`")
	# 	if isinstance(channel, int):
	# 		try:
	# 			channel = await self.client.fetch_channel(channel)
	# 		except NotFound:
	# 			return await ctx.send("Invalid `channel` input. Are you sure it is a channel (Text Channel, Voice Channel, Forum Channel)?")
	# 	if isinstance(channel, TextChannel):
	# 		await ctx.send("Please wait as this will take huge amount of time and resources to create...")
	# 		counter = 0
	# 		async for message in channel.history(limit=None):
	# 			if message.author == ctx.author:
	# 				counter += 1
	# 		await ctx.send(content="Done parsing your messages...")
	# 		msg_count = await channel.history(limit=None).flatten()
	# 		await ctx.send(content="Done parsing channel messages...")
	# 		msg_pins = await channel.pins()
	# 		try:
	# 			p_since = int(channel.created_at.timestamp())
	# 			p_tdelta = datetime.timedelta(seconds=int(time.time()) - p_since)
	# 			p_relative = f"{channel.created_at.date()}\n{p_relative} ago"
	# 		except:
	# 			p_relative = "Cannot retrieve channel creation."
	# 		embed=Embed(color=0x2f3136, title=f"{channel.name} (Text Channel)", url=channel.jump_url, description=f"{channel.topic}")
	# 		embed.add_field(name="Name", value=f"{channel.mention}").add_field(name="Channel ID", value=f"{channel.id}").add_field(name="Created at", value=f"{p_relative}")
	# 		embed.add_field(name="Messages", value=f"Global Count: {len(msg_count):,}\nYour Messages: {counter:,} ({(counter/len(msg_count))*100}%)").add_field(name="Pinned Messages", value=f"{len(msg_pins)}").add_field(name="Threads", value=f"{len(channel.threads)}")
	# 		embed.add_field(name="NSFW Flag", value=f"{channel.is_nsfw()}").add_field(name="Member List", value=f"{len(channel.members)}").add_field(name="Channel Hierarchy", value=f"{channel.position+1}")
	# 		try:
	# 			embed.add_field(name="Last Message", value=f"> {msg_count[1].author}: {msg_count[1].content}")
	# 		except:
	# 			embed.add_field(name="Last Message", value=f"> *No messages yet, or cannot retrieve message cache...*")
	# 		await ctx.send(content="Done! Sending next message...")
	# 		await ctx.send(embed=embed)
	# 	elif isinstance(channel, GuildChannel):
	# 		try:
	# 			p_since = int(channel.created_at.timestamp())
	# 			p_tdelta = datetime.timedelta(seconds=int(time.time()) - p_since)
	# 			p_relative = f"{channel.created_at.date()}\n{p_relative} ago"
	# 		except:
	# 			p_relative = "Cannot retrieve channel creation."
	# 		embed=Embed(color=0x2f3136, title=f"{channel.name} (Text Channel)", url=channel.jump_url, description=f"{channel.topic}")
	# 		embed.add_field(name="Name", value=f"{channel.mention}").add_field(name="Channel ID", value=f"{channel.id}").add_field(name="Created at", value=f"{p_relative}")
	# 		await ctx.send(embed=embed)
	# 	elif isinstance(channel, VoiceChannel):
	# 		await ctx.send("Please wait as this will take huge amount of time and resources to create...")
	# 		counter = 0
	# 		async for message in channel.history(limit=None):
	# 			if message.author == ctx.author:
	# 				counter += 1
	# 		await ctx.send(content="Done parsing your messages...")
	# 		msg_count = await channel.history(limit=None).flatten()
	# 		await ctx.send(content="Done parsing channel messages...")
	# 		msg_pins = await channel.pins()
	# 		try:
	# 			p_since = int(channel.created_at.timestamp())
	# 			p_tdelta = datetime.timedelta(seconds=int(time.time()) - p_since)
	# 			p_relative = f"{channel.created_at.date()}\n{p_relative} ago"
	# 		except:
	# 			p_relative = "Cannot retrieve channel creation."
	# 		embed=Embed(color=0x2f3136, title=f"{channel.name} (Voice Channel)", url=channel.jump_url)
	# 		embed.add_field(name="Name", value=f"{channel.mention}").add_field(name="Channel ID", value=f"{channel.id}").add_field(name="Created at", value=f"{p_relative}")
	# 		embed.add_field(name="Messages", value=f"Global Count: {len(msg_count):,}\nYour Messages: {counter:,}").add_field(name="Pinned Messages", value=f"{len(msg_pins)}").add_field(name="Bitrate", value=f"{int(channel.bitrate/1000)} kbps")
	# 		embed.add_field(name="NSFW Flag", value=f"{channel.is_nsfw()}").add_field(name="Joined Members", value=f"{len(channel.members)} / {channel.user_limit}").add_field(name="Channel Hierarchy", value=f"{channel.position+1}")
	# 		try:
	# 			embed.add_field(name="Last Message", value=f"> {msg_count[1].author}: {msg_count[1].content}")
	# 		except:
	# 			embed.add_field(name="Last Message", value=f"> *No messages yet, or cannot retrieve message cache...*")
	# 		await ctx.send(content="Done! Sending next message...")
	# 		await ctx.send(embed=embed)
	# 	elif isinstance(channel, ForumChannel):
	# 		await ctx.send("Please wait as this will take huge amount of time and resources to create...")
	# 		tags = channel.available_tags
	# 		try:
	# 			p_since = int(channel.created_at.timestamp())
	# 			p_tdelta = datetime.timedelta(seconds=int(time.time()) - p_since)
	# 			p_relative = f"{channel.created_at.date()}\n{p_relative} ago"
	# 		except:
	# 			p_relative = "Cannot retrieve channel creation."
	# 		tags_j = ", ".join([f"{tag.emoji} **{tag.name}**" for tag in tags])
	# 		embed=Embed(color=0x2f3136, title=f"{channel.name} (Forum Channel)", url=channel.jump_url, description=f"{channel.topic}")
	# 		embed.add_field(name="Name", value=f"{channel.mention}").add_field(name="Channel ID", value=f"{channel.id}").add_field(name="Created at", value=f"{p_relative}")
	# 		embed.add_field(name="NSFW Flag", value=f"{channel.is_nsfw()}").add_field(name="Threads", value=f"{len(channel.threads)}").add_field(name="Channel Hierarchy", value=f"{channel.position+1}")
	# 		embed.add_field(name="Last Thread", value=f"{channel.last_thread.mention}").add_field(name="Member Count", value=f"{channel.last_thread.member_count}").add_field(name="Message (approx)", value=f"{channel.last_thread.message_count}")
	# 		embed.add_field(name="Available Tags", value=f"{tags_j}", inline=False)
	# 		await ctx.send(embed=embed)

	@commands.command(aliases=['role'])
	async def roles(self, ctx, role: Union[Role, int, str] = None):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		if isinstance(role, str):
			if role.lower() in ["lapagan", "memes", "meme", "memes role", "meme role", "lapagan roles", "lapagan role"]:
				embed=Embed(color=0x2f3136, title="Lapagan Roles (Memes Category)", description="```yaml\nSending messages grants you XP. Gaining enough XP levels you up. Your current role changes as you progress further. See roles and corresponding level needed below. This only works on meme-tagged category. Use .channel lapagan for more information```")
				embed.add_field(name="Role Lists", value="<@&962162467520262154> (Level 50) - Free <@&962162340579647549> role.\n<@&962162402613420062> (Level 33) - Create public thread perms.\n<@&962162495290757120> (Level 18) - Same perks as <@&962162588936962089>.\n<@&962162588936962089> (Level 8) - Access to <#1045888798791323762> (Dumihan)\n<@&962162588936962089> (Level 3) - Embed & Send File Permission\n<@&962164001419173888> (Default Role)")
				await ctx.send(embed=embed)
			elif role.lower() in ["lipunan", "general", "general role", "general roles", "lipunan roles", "lipunan role"]:
				embed=Embed(color=0x2f3136, title="Lipunan Roles (General Category)", description="```yaml\nSending messages grants you XP. Gaining enough XP levels you up. Your current role changes as you progress further. See roles and corresponding level needed below. This only works on general-tagged category. Use .channel lipunan for more information```")
				embed.add_field(name="Role Lists", value="<@&962202144956637215> (Can be acquired by being nice and being active) - Access to all channels.\n<@&962164718846500886> (Level 70) - Create thread permission, has high chance of getting <@&962202144956637215>.\n<@&962164765654908929> (Level 60) - Same perks as <@&962164802275385355>.\n<@&962164802275385355> (Level 18) - Send TTS permission.\n<@&962164856151236618> (Level 35) - Access to Lipunan: Senado & Custom VC permission (Join to Create).\n<@&962164898866036796> (Level 25) - Same perks as <@&962164955585589310>\n<@&962164955585589310> (Level 10) - DJ Role (see `.role utility`), change nickname permission.\n<@&962164982353641512> (Level 5) - Send embed/file permission.\n<@&962166066455384116> **Daldalero** (Default Role)")
				await ctx.send(embed=embed)
			elif role.lower() in ["mod", "mods", "moderator", "moderators", "admin", "admins", "administrator", "administrators", "kawani", "tenyente", "heneral", "pasista"]:
				embed=Embed(color=0x2f3136, title="Kawani Roles (Staff Category)", description="```yaml\nGeneral roles for server staffs. They maintain orderliness in every channel, has the ability to mute/ban people, and has the power to accept new members.```")
				embed.add_field(name="Role Lists (Server Staffs)", value="<@&962200798564065321> (Overseer)\n<@&962200966906650646> (Organizes server events, moderator, etc.)\n<@&1001430287143669800> (Taga-tanggap ng New Members)\n<@&962539589338275900> (Staff General Role)")
				embed.add_field(name="Role Lists (Social Media Staffs)", value="<@&1001427382680424548> (Handler for KBL FB Page)\n<@&1001427742220369951> (Handler for YT KBL Channel)\n<@&1001427940845830164> (Handler for KBL Discord Server)\n<@&1001428516950245376> (Handler for KBL Tiktok)")
				embed.add_field(name="Role Lists (Others)", value="<@&1001430726471843951> (Greets newly accepted members)\n<@&1001431266748530749> (Visual Organizers)\n<@&1001431267318968360> (Designers)\n<@&1001433935345090681> (Podcast Jockey)")
				await ctx.send(embed=embed)
			elif role.lower() in ["gaming night", "gnl"]:
				embed=Embed(color=0x2f3136, title="GNL Roles (Gaming Category)", description="```yaml\nRoles made specifically for GNL events. You can acquire this by participating in certain events categorized according to games.```")
				embed.add_field(name="Role Lists (Individual)", value="<@&962201494692712458> (Given to those winners)\n<@&979974825147764746> (YAGPDB CAH)\n<@&989951294842237008> (Chess)\n<@&1023178531645182112> (Call of Duty: Mobile)\n<@&1002649820588146698> (Mobile Legends)\n<@&1002649828834164797> (Pokemon Unite)\n<@&1002647340802396170> (Puzzle Games)\n<@&1034003016107438110> (Tetris)\n<@&979971520904445983> (Valorant)\n<@&1002646869840769065> (Yggdrasil's Horse Racing)\n<@&979971238887849984> (Wild Rift)\n<@&1010527186723291256> (Pinoy Henyo)")
				embed.add_field(name="Role Lists (Team)", value="<@&987689221747789854>\n<@&987691792260554782>\n<@&1013070799814533201>\n<@&1013323629083238430>")
				await ctx.send(embed=embed)
			elif role.lower() in ["custom roles", "custom role"]:
				embed=Embed(color=0x2f3136, title="Custom Roles (Booster Category)", description="```yaml\nBoosters can have their own roles and display on their userinfo, and is prioritized above all roles. To have their role you must ask their permission first.```")
				embed.add_field(name="Role Count", value="19 (as of 8:02pm, January 16, 2023)\n<@&964180652138323968> (Given to those who boosted the server)")
				await ctx.send(embed=embed)
			elif role.lower() in ["subject roles", "subject", "subjects", "subjects role", "subjects roles", "subject role"]:
				embed=Embed(color=0x2f3136, title="Subject Roles (Utility Category)", description="```yaml\nSpecific roles for academic purposes. You can ping these roles according to what you need. Prevent pinging unnecessary roles to your academic queries. You can acquire these roles via #『📜』papel```")
				embed.add_field(name="Role Lists", value="<@&962168448878772245>\n<@&962168447540805652>\n<@&962168405287399425>\n<@&962168411406864465>\n<@&962168399339864064>\n<@&962168408466677760>")
				await ctx.send(embed=embed)
			elif role.lower() in ["gaming roles", "gaming role", "game roles", "game role", "games", "game"]:
				embed=Embed(color=0x2f3136, title="Gaming Roles (Utility Category)", description="```yaml\nSpecific roles for certain games. You can acquire these roles via #『📜』papel.```")
				embed.add_field(name="Role Lists", value="<@&995251948699791370>\n<@&965430639480438854>\n<@&965775596238024804>\n<@&962199389529571348>\n<@&962199393157677056>\n<@&962199396613758976>\n<@&1034002979256274965>\n<@&962199400145358858>")
				embed.add_field(name="\u200b", value="<@&962199409465126973>\n<@&962199412724097034>\n<@&1034002559213502524>\n<@&962199416058560523>\n<@&962199419816656936>\n<@&1041701964372791306>\n<@&962199422886879293>\n<@&962199426028412950>")
				await ctx.send(embed=embed)
			elif role.lower() in ["interest", "interests", "interest role", "interest roles", "interests role", "interests roles"]:
				embed=Embed(color=0x2f3136, title="Interest Roles (Utility Category)", description="```yaml\nSpecific roles for certain interests. You can acquire these roles via #『📜』papel.```")
				embed.add_field(name="Role Lists", value="<@&992723399015145562>\n<@&993687092972486746>\n<@&975214297712033834>\n<@&962957455061581874>\n<@&964774806841077770>\n<@&963050869367128094>")
				embed.add_field(name="\u200b", value="<@&962985926827573339>\n<@&963283951701622784>\n<@&962957622045200385>\n<@&963283282592669696>\n<@&962957561684975667>")
				await ctx.send(embed=embed)
			elif role.lower() in ["age", "age role", "age roles"]:
				embed=Embed(color=0x2f3136, title="Age Roles (Utility Category)", description="```yaml\nSeparated into two categories: Minor & Legal Age```")
				embed.add_field(name="Role Lists", value="<@&962169020151394394> (18 & above)").add_field(name="\u200b", value="<@&962169029601144862> (13 to 17 y.o)")
				await ctx.send(embed=embed)
			else:
				await ctx.send("Invalid input. Please choose from the following prompts:\nlapagan, lipunan, mod, gnl, custom roles, subject roles, gaming roles, interests, age\n\n**Usage**:\n`.role lapagan`")
		if isinstance(role, int):
			try:
				role = ctx.guild.get_role(role)
			except NotFound:
				return await ctx.send("Invalid `role` input. Are you sure it is a role?")
		if isinstance(role, Role):
			try:
				p_since = int(role.created_at.timestamp())
				p_tdelta = datetime.timedelta(seconds=int(time.time()) - p_since)
				p_relative = f"{role.created_at.date()}\n{p_relative} ago"
			except:
				p_relative = "Cannot retrieve channel creation."
			embed=Embed(color=0x2f3136, title=f"{role.name}").add_field(name="Role Name", value=f"{role.mention}").add_field(name="Role ID", value=f"{role.id}").add_field(name="Color", value=f"{role.color}")
			embed.add_field(name="Hoisted", value=f"{role.hoist}").add_field(name="Members who has the Role", value=f"{len(role.members)}").add_field(name="Mentionable", value=f"{role.mentionable}")
			try:
				embed.set_thumbnail(url=role.icon.url)
			except:
				pass
			await ctx.send(embed=embed)

	@commands.command(aliases=['botstat'])
	async def botstats(self, ctx):
		await ctx.trigger_typing()
		m, md = await db.record("SELECT Maintenance, MaintenanceDuration FROM global")
		if m == 1:
			return await ctx.send(f"<@1050024676627320872> is currently in maintenance! Try again later.\n\nETA: <t:{md+3600}:R>")
		member_list = []
		generated_time = datetime.datetime.now(tz=pytz.timezone('Asia/Manila')).strftime("%Y/%m/%d, %I:%M %p")
		gen_role, matanda, bata = ctx.guild.get_role(961967298955079740), ctx.guild.get_role(962169020151394394), ctx.guild.get_role(962169029601144862)
		lap_a, lap_b, lap_c, lap_d, lap_e, lap_f = ctx.guild.get_role(962162467520262154), ctx.guild.get_role(962162402613420062), ctx.guild.get_role(962162495290757120), ctx.guild.get_role(962162588936962089), ctx.guild.get_role(962162865182216235), ctx.guild.get_role(962164001419173888)
		lip_a, lip_b, lip_c, lip_d, lip_e, lip_f, lip_g, lip_h = ctx.guild.get_role(962164718846500886), ctx.guild.get_role(962164765654908929), ctx.guild.get_role(962164802275385355), ctx.guild.get_role(962164856151236618), ctx.guild.get_role(962164898866036796), ctx.guild.get_role(962164955585589310), ctx.guild.get_role(962164982353641512), ctx.guild.get_role(962166066455384116)
		everyone_role, booster_role, baguhan_role = ctx.guild.get_role(961502956195303494), ctx.guild.get_role(964180652138323968), ctx.guild.get_role(961964769772961822)
		for member in ctx.guild.members:
			member_join = int(member.joined_at.timestamp())
			if (int(time.time()) - member_join) < 1209600 and gen_role in member.roles:
				join_relative = datetime.timedelta(seconds=int(time.time() - member_join))
				join_hum = humanize.naturaldelta(join_relative)
				member_list.append(f"{member.name} - {join_hum} ago")
		if len(member_list) <= 6:
			member_lists = "\n".join([item for item in member_list])
		elif len(member_list) > 6:
			memberlists = "\n".join([item for item in member_list[:6]])
			member_lists = f"{memberlists}\nAND {len(member_list)-6} MORE"
		else:
			member_lists = "-- EMPTY --"
		desc0 = f"```yaml\n-- MEMBER COUNT --\n{gen_role.name.upper()} - {len(gen_role.members)} ({round((len(gen_role.members)/len(everyone_role.members))*100, 2)}%)\n{baguhan_role.name.upper()} - {len(baguhan_role.members)} ({round((len(baguhan_role.members)/len(everyone_role.members))*100, 2)}%)\n\n-- AGE STATISTICS --\n{matanda.name.upper()} - {len(matanda.members)} ({round((len(matanda.members)/len(everyone_role.members))*100, 2)}%)\n{bata.name.upper()} - {len(bata.members)} ({round((len(bata.members)/len(everyone_role.members))*100, 2)}%)\n\n```"
		desc1 = f"```yaml\n-- LAPAGAN STATISTICS --\n{lap_a.name.upper()} - {len(lap_a.members)} ({round((len(lap_a.members)/len(everyone_role.members))*100, 2)}%)\n{lap_b.name.upper()} - {len(lap_b.members)} ({round((len(lap_b.members)/len(everyone_role.members))*100, 2)}%)\n{lap_c.name.upper()} - {len(lap_c.members)} ({round((len(lap_c.members)/len(everyone_role.members))*100, 2)}%)\n{lap_d.name.upper()} - {len(lap_d.members)} ({round((len(lap_d.members)/len(everyone_role.members))*100, 2)}%)\n{lap_e.name.upper()} - {len(lap_e.members)} ({round((len(lap_e.members)/len(everyone_role.members))*100, 2)}%)\n{lap_f.name.upper()} - {len(lap_f.members)} ({round((len(lap_f.members)/len(everyone_role.members))*100, 2)}%)```"
		desc2 = f"```yaml\n-- LIPUNAN STATISTICS --\n{lip_a.name.upper()} - {len(lip_a.members)} ({round((len(lip_a.members)/len(everyone_role.members))*100, 2)}%)\n{lip_b.name.upper()} - {len(lip_b.members)} ({round((len(lip_b.members)/len(everyone_role.members))*100, 2)}%)\n{lip_c.name.upper()} - {len(lip_c.members)} ({round((len(lip_c.members)/len(everyone_role.members))*100, 2)}%)\n{lip_d.name.upper()} - {len(lip_d.members)} ({round((len(lip_d.members)/len(everyone_role.members))*100, 2)}%)\n{lip_e.name.upper()} - {len(lip_e.members)} ({round((len(lip_e.members)/len(everyone_role.members))*100, 2)}%)\n{lip_f.name.upper()} - {len(lip_f.members)} ({round((len(lip_f.members)/len(everyone_role.members))*100, 2)}%)\n{lip_g.name.upper()} - {len(lip_g.members)} ({round((len(lip_g.members)/len(everyone_role.members))*100, 2)}%)\n{lip_h.name.upper()} - {len(lip_h.members)} ({round((len(lip_h.members)/len(everyone_role.members))*100, 2)}%)```"
		desc3 = f"```yaml\n-- OTHER STATISTICS --\n{booster_role.name.upper()} - {len(booster_role.members)} ({round((len(booster_role.members)/len(everyone_role.members))*100, 2)}%)\n\n-- NEW JOINED MEMBERS --\n{member_lists}```"
		desc4 = f"```yaml\nstats generated as of {generated_time}```"
		await ctx.send(f"{desc0}\n{desc1}\n{desc2}\n{desc3}\n{desc4}")

def setup(client):
	client.add_cog(utility(client))