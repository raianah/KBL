import time, ast, datetime, random, string
from disnake.ext import commands, tasks
from disnake import Client, Embed, Message
from disnake.errors import NotFound
from disnake.utils import get
from mizuki.db import db

def gen_level_up(message, level):
	ambot = get(message.guild.roles, id=962164982353641512)
	bugok = get(message.guild.roles, id=962164955585589310)
	kumag = get(message.guild.roles, id=962164898866036796)
	deputa = get(message.guild.roles, id=962164856151236618)
	engot = get(message.guild.roles, id=962164802275385355)
	gago = get(message.guild.roles, id=962164765654908929)
	hangal = get(message.guild.roles, id=962164718846500886)
	success, msg = False, ""
	lvlchecker = db.field("SELECT GenLevelUpChecker FROM main WHERE UserID = ?", message.author.id)
	if level >= 10 and level < 20 and lvlchecker != 1:
		db.execute("UPDATE main SET GenLevelUpChecker = 1 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{ambot.name}`!"
		success = True
	elif level >= 20 and level < 30 and lvlchecker != 2:
		db.execute("UPDATE main SET GenLevelUpChecker = 2 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{bugok.name}`!"
		success = True
	elif level >= 30 and level < 40 and lvlchecker != 3:
		db.execute("UPDATE main SET GenLevelUpChecker = 3 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{kumag.name}`!"
		success = True
	elif level >= 40 and level < 50 and lvlchecker != 4:
		db.execute("UPDATE main SET GenLevelUpChecker = 4 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{deputa.name}`!"
		success = True
	elif level >= 50 and level < 60 and lvlchecker != 5:
		db.execute("UPDATE main SET GenLevelUpChecker = 5 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{engot.name}`!"
		success = True
	elif level >= 60 and level < 70 and lvlchecker != 6:
		db.execute("UPDATE main SET GenLevelUpChecker = 6 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{gago.name}`!"
		success = True
	elif level >= 70 and level < 80 and lvlchecker != 7:
		db.execute("UPDATE main SET GenLevelUpChecker = 7 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{hangal.name}`!"
		success = True
	#elif level >= 80 and level < 90 and lvlchecker != 8:
	#	db.execute("UPDATE main SET GenLevelUpChecker = 8 WHERE UserID = ?", message.author.id)
	#	msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{impakto.name}`!"
	#	success = True
	#elif level >= 90 and level < 100 and lvlchecker != 9:
	#	db.execute("UPDATE main SET GenLevelUpChecker = 9 WHERE UserID = ?", message.author.id)
	#	msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{lukayo.name}`!"
	#	success = True
	return success, msg

def mem_level_up(message, level):
	egul = get(message.guild.roles, id=962162865182216235)
	dumi = get(message.guild.roles, id=962162588936962089)
	cykat = get(message.guild.roles, id=962162495290757120)
	banal = get(message.guild.roles, id=962162402613420062)
	alamat = get(message.guild.roles, id=962162467520262154)
	success, msg = False, ""
	lvlchecker = db.field("SELECT MemLevelUpChecker FROM main WHERE UserID = ?", message.author.id)
	if level >= 3 and level < 8 and lvlchecker != 1:
		db.execute("UPDATE main SET MemLevelUpChecker = 1 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{egul.name}`!"
		success = True
	elif level >= 8 and level < 18 and lvlchecker != 2:
		db.execute("UPDATE main SET MemLevelUpChecker = 2 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{dumi.name}`!"
		success = True
	elif level >= 18 and level < 33 and lvlchecker != 3:
		db.execute("UPDATE main SET MemLevelUpChecker = 3 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{cykat.name}`!"
		success = True
	elif level >= 33 and level < 50 and lvlchecker != 4:
		db.execute("UPDATE main SET MemLevelUpChecker = 4 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{banal.name}`!"
		success = True
	elif level >= 50 and lvlchecker != 5: # and level < 60 and lvlchecker != 5:
		db.execute("UPDATE main SET MemLevelUpChecker = 5 WHERE UserID = ?", message.author.id)
		msg = f"Mahusay, {message.author.mention}! Isa ka nang ganap na `{alamat.name}`!"
		success = True
	return success, msg

def bonus_coins_conversion(bonus_coins):
	if bonus_coins < 10:
		bonus = 0
	elif bonus_coins >= 10 and bonus_coins < 40:
		bonus = 1
	elif bonus_coins >= 40 and bonus_coins < 70:
		bonus = 2
	elif bonus_coins >= 70 and bonus_coins < 100:
		bonus = 3
	elif bonus_coins >= 100 and bonus_coins < 50:
		bonus = 4
	elif bonus_coins >= 150 and bonus_coins < 210:
		bonus = 5
	elif bonus_coins >= 210:
		bonus = 7
	return bonus

class kbl_4(commands.Cog):
	def __init__(self, client: Client):
		self.client = client
		self.voting_check.start()

	async def gen_process_xp(self, message):
		gen_xp, gen_lvl, gen_xplock = db.record("SELECT GeneralXP, GeneralLevel, GenLevelRest FROM main WHERE UserID = ?", message.author.id)

		if int(time.time()) > gen_xplock:
			await self.gen_add_xp(message, gen_xp, gen_lvl)

	async def mem_process_xp(self, message):
		mem_xp, mem_lvl, mem_xplock = db.record("SELECT MemesXP, MemesLevel, MemLevelRest FROM main WHERE UserID = ?", message.author.id)

		if int(time.time()) > mem_xplock:
			await self.mem_add_xp(message, mem_xp, mem_lvl)

	async def both_process_xp(self, message):
		gen_xp, gen_lvl, gen_xplock = db.record("SELECT GeneralXP, GeneralLevel, GenLevelRest FROM main WHERE UserID = ?", message.author.id)
		mem_xp, mem_lvl, mem_xplock = db.record("SELECT MemesXP, MemesLevel, MemLevelRest FROM main WHERE UserID = ?", message.author.id)

		if int(time.time()) > mem_xplock:
			await self.mem_add_xp(message, mem_xp, mem_lvl)

		if int(time.time()) > gen_xplock:
			await self.gen_add_xp(message, gen_xp, gen_lvl)

	async def gen_add_xp(self, message, xp, lvl):
		xp_to_add = random.randint(10, 15)
		coin_to_add = random.randint(4, 8)
		lvl_limit = db.field("SELECT GenLevelLimit FROM main WHERE UserID = ?", message.author.id)

		db.execute("UPDATE main SET GeneralXP = GeneralXP + ?, GenLevelRest = ? WHERE UserID = ?", xp_to_add, int(time.time()+60), message.author.id)
		db.execute("UPDATE main SET GlobalXP = GlobalXP + ?, Points = Points + ? WHERE UserID = ?", xp_to_add, coin_to_add, message.author.id)

		if xp+xp_to_add >= lvl_limit:
			db.execute("UPDATE main SET GenLevelLimit = GenLevelLimit + 100, GeneralXP = 0, GeneralLevel = GeneralLevel + 1 WHERE UserID = ?", message.author.id)
			await self.gen_levelup_send(message)

	async def mem_add_xp(self, message, xp, lvl):
		xp_to_add = random.randint(10, 15)
		coin_to_add = random.randint(4, 8)
		lvl_limit = db.field("SELECT MemLevelLimit FROM main WHERE UserID = ?", message.author.id)

		db.execute("UPDATE main SET MemesXP = MemesXP + ?, MemLevelRest = ? WHERE UserID = ?", xp_to_add, int(time.time()+60), message.author.id)
		db.execute("UPDATE main SET GlobalXP = GlobalXP + ?, Points = Points + ? WHERE UserID = ?", xp_to_add, coin_to_add, message.author.id)

		if xp+xp_to_add >= lvl_limit:
			db.execute("UPDATE main SET MemLevelLimit = MemLevelLimit + 100, MemesXP = 0, MemesLevel = MemesLevel + 1 WHERE UserID = ?", message.author.id)
			await self.mem_levelup_send(message)

	async def both_add_xp(self, message, xp, lvl):
		xp_to_add_0, xp_to_add_1 = random.randint(10, 15), random.randint(10, 15)
		coin_to_add_0 = random.randint(4, 8), random.randint(4, 8)
		lvl_limit_0, lvl_limit_1, = db.record("SELECT GenLevelLimit, MemLevelLimit FROM main WHERE UserID = ?", message.author.id)

		db.execute("UPDATE main SET GeneralXP = GeneralXP + ?, GenLevelRest = ? WHERE UserID = ?", xp_to_add_0, int(time.time()+60), message.author.id)
		db.execute("UPDATE main SET MemesXP = MemesXP + ?, MemLevelRest = ? WHERE UserID = ?", xp_to_add_1, int(time.time()+60), message.author.id)
		db.execute("UPDATE main SET GlobalXP = GlobalXP + ?, Points = Points + ? WHERE UserID = ?", xp_to_add_0+xp_to_add_1, coin_to_add_0, message.author.id)

		if xp+xp_to_add_1 >= lvl_limit_1:
			db.execute("UPDATE main SET MemLevelLimit = MemLevelLimit + 100, MemesXP = 0, MemesLevel = MemesLevel + 1 WHERE UserID = ?", message.author.id)
			await self.mem_levelup_send(message)

		if xp+xp_to_add_0 >= lvl_limit_0:
			db.execute("UPDATE main SET GenLevelLimit = GenLevelLimit + 100, GeneralXP = 0, GeneralLevel = GeneralLevel + 1 WHERE UserID = ?", message.author.id)
			await self.gen_levelup_send(message)

	async def gen_levelup_send(self, message: Message):
		# 0 - text, 1 - embed, 2 - image
		lvltype, lvl = db.record("SELECT LevelUpType, GeneralLevel FROM main WHERE UserID = ?", message.author.id)
		success, msg = gen_level_up(message, lvl)
		if lvltype == 0:
			#if success == True:
			#	await message.channel.send(msg)
			#else:
			await message.channel.send(f"Mahusay, {message.author.mention}! Ikaw ay nag-level up na **(Level {lvl}!)**")
		elif lvltype == 1:
			#if success == True:
			#	embed=Embed(title=f"Mahusay, {message.author}!", timestamp=datetime.datetime.now(), description=msg, color=0x2f3136)
			#else:
			embed=Embed(title=f"Mahusay, {message.author}!", timestamp=datetime.datetime.now(), description=f"Mahusay, {message.author.mention}! Ikaw ay nag-level up na **(Level {lvl}!)**", color=0x2f3136)
			await message.channel.send(embed=embed)

	async def mem_levelup_send(self, message: Message):
		# 0 - text, 1 - embed, 2 - image
		lvltype, lvl = db.record("SELECT LevelUpType, MemesLevel FROM main WHERE UserID = ?", message.author.id)
		success, msg = mem_level_up(message, lvl)
		if lvltype == 0:
			#if success == True:
			#	await message.channel.send(msg)
			#else:
			await message.channel.send(f"Mahusay, {message.author.mention}! Ikaw ay nag-level up na **(Level {lvl}!)**")
		elif lvltype == 1:
			#if success == True:
			#	embed=Embed(title=f"Mahusay, {message.author}!", timestamp=datetime.datetime.now(), description=msg, color=0x2f3136)
			#else:
			embed=Embed(title=f"Mahusay, {message.author}!", timestamp=datetime.datetime.now(), description=f"Mahusay, {message.author.mention}! Ikaw ay nag-level up na **(Level {lvl}!)**", color=0x2f3136)
			await message.channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_ready(self):
		print("KBL (Vote) is loaded.")

	@tasks.loop(seconds=1)
	async def voting_check(self):
		members = db.column("SELECT UserID FROM main")
		for member in members:
			votes, duration = db.record("SELECT MonthlyBonusPoints, VotingDuration FROM main WHERE UserID = ?", member)
			if int(time.time()) >= duration and duration > 0:
				if votes < 70.0:
					db.execute("UPDATE main SET VotingDuration = 0, MonthlyBonusPoints = 0.0 WHERE UserID = ?", member)
				else:
					db.execute("UPDATE main SET VotingDuration = 0, MonthlyBonusPoints = MonthlyBonusPoints - 70.0 WHERE UserID = ?", member)

	@commands.Cog.listener("on_message")
	async def leveling_checks(self, message):
		m = db.field("SELECT Maintenance FROM global")
		if m == 1:
			return
		if not message.author.bot:
			reg = db.record("SELECT * FROM main WHERE UserID = ?", message.author.id)
			if reg is None:
				db.execute("INSERT INTO main (UserID) VALUES (?)", message.author.id)
			db.execute("UPDATE main SET Messages = Messages + 1 WHERE UserID = ?", message.author.id)
			if len(message.mentions) == 1:
				check = any(ele.lower() in message.content for ele in ["thanks", "thank you", "thanks you", "thank", "salamat", "slmat", "slmt"])
				if check:
					msg = message.mentions[0]
					if not msg.bot and not message.author.id == msg.id:
						_reg = db.record("SELECT * FROM main WHERE UserID = ?", msg.id)
						if _reg is None:
							db.execute("INSERT INTO main (UserID) VALUES (?)", msg.id)
						cooldown = db.field("SELECT LPCooldown FROM main WHERE UserID = ?", message.author.id)
						if int(time.time()) > cooldown:
							db.execute("UPDATE main SET LigtasPoints = LigtasPoints + 1 WHERE UserID = ?", msg.id)
							db.execute("UPDATE main SET LPCooldown = ? WHERE UserID = ?", int(time.time())+43200, message.author.id)
							_lp = db.field("SELECT LigtasPoints FROM main WHERE UserID = ?", msg.id)
							_lb = db.records("SELECT UserID, LigtasPoints FROM main ORDER BY LigtasPoints DESC")
							embed=Embed(color=0x2f3136, description=f"　Dahil ikaw ay nakatulong, gagantimpalaan kita ng **__+1 Ligtas Points__**!\n\n　　**Rank:** #{_lb.index((msg.id, _lp))+1:,}\n　　**LP:** {_lp:,}").set_author(name=f"{msg}", icon_url=msg.display_avatar)
							await message.channel.send(content=f"Maraming salamat sa pagtulong, {msg.mention}!", embed=embed)
			elif message.reference is not None and not message.is_system:
				check = any(ele.lower() in message.content for ele in ["thanks", "thank you", "thanks you", "thank", "salamat", "slmat", "slmt"])
				if check:
					msg = await message.channel.fetch_message(message.reference.message_id)
					if not msg.author.bot and not message.author.id == msg.author.id:
						_reg = db.record("SELECT * FROM main WHERE UserID = ?", msg.author.id)
						if _reg is None:
							db.execute("INSERT INTO main (UserID) VALUES (?)", msg.author.id)
						cooldown = db.field("SELECT LPCooldown FROM main WHERE UserID = ?", message.author.id)
						if int(time.time()) > cooldown:
							db.execute("UPDATE main SET LigtasPoints = LigtasPoints + 1 WHERE UserID = ?", msg.author.id)
							db.execute("UPDATE main SET LPCooldown = ? WHERE UserID = ?", int(time.time())+43200, message.author.id)
							_lp = db.field("SELECT LigtasPoints FROM main WHERE UserID = ?", msg.author.id)
							_lb = db.records("SELECT UserID, LigtasPoints FROM main ORDER BY LigtasPoints DESC")
							embed=Embed(color=0x2f3136, timestamp=datetime.datetime.now(), description=f"　Dahil ikaw ay nakatulong, gagantimpalaan kita ng **__+1 Ligtas Points__**!\n　　**Rank:** #{_lb.index(msg.author.id)+1:,}\n　　**LP:** {_lp:,}").set_author(name=f"{msg.author}", icon_url=msg.author.display_avatar)
							embed.set_thumbnail(url=message.guild.icon.url)
							await message.channel.send(content=f"Maraming salamat sa pagtulong, {msg.author.mention}!", embed=embed)
			if message.channel.id in [961504020508340294, 1045888798791323762] and message.attachments:
				await message.add_reaction('<:wahahaha:962970864003989505>')
				await message.add_reaction('❌')
				await message.add_reaction('♻️')
			#if message.channel.id in [961504020508340294, 1045888798791323762, 1026473207995305984, 961504084391772160]:
			#	await self.mem_process_xp(message)
			#elif message.channel.id in [961503519913938984, 978606766638116864]:
			#	await self.both_process_xp(message)
			#elif message.channel.id in [961504364269301764, 961504384636846090, 961504419151745084, 961504460008489022, 969770039857270854, 966977955534356480, 961504650270502932]:
			#	await self.gen_process_xp(message)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.user_id in [1050024676627320872, 1010612812659306618]:
			return
		channel = self.client.get_channel(payload.channel_id)
		msg = await channel.fetch_message(payload.message_id)
		if payload.channel_id in [961504020508340294, 1045888798791323762] and msg.attachments:
			if payload.user_id == msg.author.id:
				await msg.remove_reaction(payload.emoji, payload.member.id)
			elif str(payload.emoji) == "<:wahahaha:962970864003989505>":
				db.execute("UPDATE main SET MonthlyBonusPoints = MonthlyBonusPoints + 1.0 WHERE UserID = ?", payload.user_id)
			elif str(payload.emoji) == "❌":
				db.execute("UPDATE main SET MonthlyBonusPoints = MonthlyBonusPoints - 0.5 WHERE UserID = ?", payload.user_id)
			elif str(payload.emoji) == "♻️":
				db.execute("UPDATE main SET MonthlyBonusPoints = MonthlyBonusPoints - 0.5 WHERE UserID = ?", payload.user_id)
			if payload.channel_id in [961504364269301764, 961503519913938984] and str(payload.emoji) == "<:wahahaha:962970864003989505>" and msg.attachments and msg.reactions[0].count == 20:
				starboard, starboard_list = db.field("SELECT StarboardList, StarboardPList FROM global")
				user_starboard = db.field("SELECT StarboardList FROM main WHERE UserID = ?", msg.author.id)
				_starboard, _user_starboard = ast.literal_eval(starboard), ast.literal_eval(user_starboard)
				_starboard_list = ast.literal_eval(starboard_list)
				if payload.message_id not in _starboard_list:
					if len(list(_starboard.keys())) == 0:
						code = "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(5)])
					else:
						while True:
							code = "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(5)])
							if not code in list(_starboard.keys()) and not code in list(_user_starboard.keys()):
								break
					_starboard_list.append(payload.message_id)
					_starboard[code] = payload.message_id
					_user_starboard[code] = [payload.message_id, "🟡 Pending", "No remarks.", 0]
					db.execute("UPDATE global SET StarboardList = ?, StarboardPList = ?", f"{_starboard}", f"{_starboard_list}")
					db.execute("UPDATE main SET StarboardList = ? WHERE UserID = ?", f"{_user_starboard}", msg.author.id)
					await channel.send(f"{msg.author.mention}, your post ({msg.jump_url}) has reached **20** <:wahahaha:962970864003989505> reacts! Congratulations on your milestone!\n\nYour post will now be reviewed by the admins/moderators to be posted in <#1048837480700465202>.")
			elif payload.channel_id in [1045888798791323762, 1045888798791323762] and str(payload.emoji) == "<:wahahaha:962970864003989505>" and msg.reactions[0].count == 10:
				starboard, starboard_list = db.field("SELECT StarboardList, StarboardPList FROM global")
				user_starboard = db.field("SELECT StarboardList FROM main WHERE UserID = ?", msg.author.id)
				_starboard, _user_starboard = ast.literal_eval(starboard), ast.literal_eval(user_starboard)
				_starboard_list = ast.literal_eval(starboard_list)
				if payload.message_id not in _starboard_list:
					if len(list(_starboard.keys())) == 0:
						code = "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(5)])
					else:
						while True:
							code = "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(5)])
							if not code in list(_starboard.keys()) and not code in list(_user_starboard.keys()):
								break
					_starboard_list.append(payload.message_id)
					_starboard[code] = payload.message_id
					_user_starboard[code] = [payload.message_id, "🟡 Pending", "No remarks.", 0]
					db.execute("UPDATE global SET StarboardList = ?, StarboardPList = ?", f"{_starboard}", f"{_starboard_list}")
					db.execute("UPDATE main SET StarboardList = ? WHERE UserID = ?", f"{_user_starboard}", msg.author.id)
					await channel.send(f"{msg.author.mention}, your post ({msg.jump_url}) has reached **10** <:wahahaha:962970864003989505> reacts! Congratulations on your milestone!\n\nYour post will now be reviewed by the admins/moderators to be posted in <#1048837480700465202>.")

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		if payload.user_id in [1050024676627320872, 1010612812659306618]:
			return
		channel = self.client.get_channel(payload.channel_id)
		msg = await channel.fetch_message(payload.message_id)
		if payload.channel_id in [961504020508340294, 1045888798791323762] and msg.attachments:
			if payload.user_id == msg.author.id:
				await msg.remove_reaction(payload.emoji, payload.member.id)
			elif str(payload.emoji) == "<:wahahaha:962970864003989505>":
				db.execute("UPDATE main SET MonthlyBonusPoints = MonthlyBonusPoints - 1.0 WHERE UserID = ?", payload.user_id)
			elif str(payload.emoji) == "❌":
				db.execute("UPDATE main SET MonthlyBonusPoints = MonthlyBonusPoints + 0.5 WHERE UserID = ?", payload.user_id)
			elif str(payload.emoji) == "♻️":
				db.execute("UPDATE main SET MonthlyBonusPoints = MonthlyBonusPoints + 0.5 WHERE UserID = ?", payload.user_id)

	@commands.Cog.listener("on_message")
	async def tgg_voting_rewards(self, message):
		if message.author == self.client.user:
			return
		try:
			if message.channel.id == 1085571131043483699:
				dbl_channel = self.client.get_channel(1085571131043483699)
				dbl_msg = await dbl_channel.fetch_message(dbl_channel.last_message_id)
				if dbl_msg is not None:
					m1 = int(dbl_msg.content)
					print(f"Someone voted - {m1}")
					reg = db.record("SELECT * FROM main WHERE UserID = ?", m1)
					if reg is None:
						db.execute("INSERT INTO main (UserID) VALUES (?)", m1)
					dt = datetime.datetime.now().weekday()
					if dt in [4, 5, 6]:
						amt = "**__+3 SP__**"
						db.execute("UPDATE main SET MonthlyBonusPoints = MonthlyBonusPoints + 70.0, VotingDuration = ? WHERE UserID = ?", int(time.time())+43200, m1)
					else:
						amt = "**__+3 SP__**"
						db.execute("UPDATE main SET MonthlyBonusPoints = MonthlyBonusPoints + 70.0, VotingDuration = ? WHERE UserID = ?", int(time.time())+43200, m1)
					print(f"Done distributing the rewards to {m1}.")
					try:
						user = await self.client.fetch_user(m1)
						await user.send(f"Thank you for voting, <@{m1}>! You gained {amt} for the next 12h. Enjoy your perks ;)")
					except:
						pass
					await dbl_msg.delete()
		except NotFound:
			return

def setup(client):
	client.add_cog(kbl_4(client))