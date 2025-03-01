import time, datetime, random, json
from disnake.ext import commands
from disnake import Client, Embed, Message, MessageInteraction
from disnake.ui import Button
from kbl.db import db


"""

	Please check IMPORTANT.md for the layout and descriptions of other commands. Some are very simple, and some are complex.
	For existing errors, check ERRORS.md.
	For overall and general information about this project, database schema, and more, check README.md.

	Goodluck to those who will use this once-so-called 'masterpiece' for their discord server.

	Sincerely,
		raianxh_

		
	PS: All events/background processes are all catered to KBL Discord Server. If you wish to use this in your own server, you need to tweak it a little and replace some objects with your own.
		You must be fluent to read Python and Discord Developer. Otherwise, feel free to remove/comment it.

"""


class background_process(commands.Cog):
	def __init__(self, client: Client):
		self.client = client

	async def gen_process_xp(self, message):
		gen_xp, gen_lvl, gen_xplock = await db.record("SELECT GeneralXP, GeneralLevel, GenLevelRest FROM main WHERE UserID = %s", message.author.id)

		if int(time.time()) > gen_xplock:
			await self.gen_add_xp(message, gen_xp, gen_lvl)

	async def gen_add_xp(self, message, xp, lvl):
		xp_to_add = random.randint(10, 15)
		coin_to_add = random.randint(4, 8)
		lvl_limit = await db.field("SELECT GenLevelLimit FROM main WHERE UserID = %s", message.author.id)

		await db.execute("UPDATE main SET GeneralXP = GeneralXP + %s, GenLevelRest = %s, Coins = Coins + %s WHERE UserID = %s", xp_to_add, int(time.time()+60), coin_to_add, message.author.id)

		if xp+xp_to_add >= lvl_limit:
			await db.execute("UPDATE main SET GenLevelLimit = GenLevelLimit + 100, GeneralXP = 0, GeneralLevel = GeneralLevel + 1 WHERE UserID = %s", message.author.id)
			await self.gen_levelup_send(message)

	async def gen_levelup_send(self, message: Message):
		# 0 - text, 1 - embed, 2 - image
		lvltype, lvl = await db.record("SELECT LevelUpType, GeneralLevel FROM main WHERE UserID = %s", message.author.id)
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
		print("KBL (Background Process) is loaded.")

	@commands.Cog.listener("on_message")
	async def leveling_checks(self, message: Message):
		m = await db.field("SELECT Maintenance FROM global")
		if m == 1:
			return
		if not message.author.bot:
			reg = await db.record("SELECT * FROM main WHERE UserID = %s", message.author.id)
			if reg is None:
				await db.execute("INSERT INTO main (UserID) VALUES (%s)", message.author.id)
			await db.execute("UPDATE main SET Messages = Messages + 1 WHERE UserID = %s", message.author.id)
			if len(message.mentions) == 1:
				check = any(ele.lower() in message.content.lower() for ele in ["thanks", "thank you", "thanks you", "thank", "salamat", "slmat", "slmt"])
				if check:
					msg = message.mentions[0]
					if not msg.bot and not message.author.id == msg.id:
						_reg = await db.record("SELECT * FROM main WHERE UserID = %s", msg.id)
						if _reg is None:
							await db.execute("INSERT INTO main (UserID) VALUES (%s)", msg.id)
						cooldown = await db.field("SELECT LPCooldown FROM main WHERE UserID = %s", message.author.id)
						if int(time.time()) > cooldown:
							await db.execute("UPDATE main SET LigtasPoints = LigtasPoints + 1 WHERE UserID = %s", msg.id)
							await db.execute("UPDATE main SET LPCooldown = %s WHERE UserID = %s", int(time.time())+43200, message.author.id)
							_lp = await db.field("SELECT LigtasPoints FROM main WHERE UserID = %s", msg.id)
							_lb = await db.records("SELECT UserID, LigtasPoints FROM main ORDER BY LigtasPoints DESC")
							embed=Embed(color=0x2f3136, description=f"　Dahil ikaw ay nakatulong, gagantimpalaan kita ng **__+1 Ligtas Points__**!\n\n　　**Rank:** #{_lb.index((msg.id, _lp))+1:,}\n　　**LP:** {_lp:,}").set_author(name=f"{msg}", icon_url=msg.display_avatar)
							await message.channel.send(content=f"Maraming salamat sa pagtulong, {msg.mention}!", embed=embed)
			elif message.reference is not None and not message.is_system:
				check = any(ele.lower() in message.content for ele in ["thanks", "thank you", "thanks you", "thank", "salamat", "slmat", "slmt"])
				if check:
					msg = await message.channel.fetch_message(message.reference.message_id)
					if not msg.author.bot and not message.author.id == msg.author.id:
						_reg = await db.record("SELECT * FROM main WHERE UserID = %s", msg.author.id)
						if _reg is None:
							await db.execute("INSERT INTO main (UserID) VALUES (%s)", msg.author.id)
						cooldown = await db.field("SELECT LPCooldown FROM main WHERE UserID = %s", message.author.id)
						if int(time.time()) > cooldown:
							await db.execute("UPDATE main SET LigtasPoints = LigtasPoints + 1 WHERE UserID = %s", msg.author.id)
							await db.execute("UPDATE main SET LPCooldown = %s WHERE UserID = %s", int(time.time())+43200, message.author.id)
							_lp = await db.field("SELECT LigtasPoints FROM main WHERE UserID = %s", msg.author.id)
							_lb = await db.records("SELECT UserID, LigtasPoints FROM main ORDER BY LigtasPoints DESC")
							embed=Embed(color=0x2f3136, timestamp=datetime.datetime.now(), description=f"　Dahil ikaw ay nakatulong, gagantimpalaan kita ng **__+1 Ligtas Points__**!\n　　**Rank:** #{_lb.index(msg.author.id)+1:,}\n　　**LP:** {_lp:,}").set_author(name=f"{msg.author}", icon_url=msg.author.display_avatar)
							embed.set_thumbnail(url=message.guild.icon.url)
							await message.channel.send(content=f"Maraming salamat sa pagtulong, {msg.author.mention}!", embed=embed)
			if message.channel.id in [961504020508340294, 1045888798791323762] and message.attachments:
				files = []
				components = [Button(label="0", emoji="<:wahahaha:962970864003989505>"), Button(label="0", emoji="❌"), Button(label="0", emoji="♻️"), Button(label="0", emoji="❓"), Button(label="0", emoji="❤️")]
				for attachment in message.attachments:
					new_file = await attachment.to_file()
					files.append(new_file)
				await message.delete()
				content = message.content if message.content is not None else ""
				msg_p = await message.channel.send(content=f"{content}\n\nPosted by: {message.author.mention}\nDate Posted: <t:{int(time.time())}:R>", files=files)
				c = 0
				for button in components:
					button.custom_id = f"{msg_p.id}:{c}"
					c += 1
				await msg_p.edit(components=components)
				await db.execute("UPDATE main SET MessageIDS = JSON_SET(IFNULL(MessageIDS, '{}'), %s, JSON_OBJECT('owner_id', %s, 'laugh_reacts', JSON_ARRAY(), 'x_reacts', JSON_ARRAY(), 'recycle_reacts', JSON_ARRAY(), 'question_reacts', JSON_ARRAY(), 'heart_reacts', JSON_ARRAY())) WHERE UserID = %s", f"$.{msg_p.id}", message.author.id, message.author.id)
				# await message.add_reaction('<:wahahaha:962970864003989505>')
				# await message.add_reaction('❌')
				# await message.add_reaction('♻️')
				# await message.add_reaction('❓')
				# await message.add_reaction('♥')
			if message.channel.id in [961504364269301764, 961503519913938984, 961504384636846090, 961504419151745084, 961504460008489022, 969770039857270854, 966977955534356480, 961504650270502932]:
				await self.gen_process_xp(message)
			# 	if "happy halloween" in message.content:
			# 		await message.add_reaction('🎃')

	@commands.Cog.listener()
	async def on_button_click(self, interaction: MessageInteraction):
		print(interaction.component.custom_id)
		msg = interaction.component.custom_id.split(":")
		components = [Button(label="0", emoji="<:wahahaha:962970864003989505>"), Button(label="0", emoji="❌"), Button(label="0", emoji="♻️"), Button(label="0", emoji="❓"), Button(label="0", emoji="❤️")]
		try:
			pass
		except TypeError:
			return await interaction.response.edit_message(components=components)
		user_id = await db.field("SELECT UserID FROM main WHERE JSON_CONTAINS_PATH(MessageIDS, 'one', %s)", f"$.{msg[0]}")
		c = 0
		_rl = await db.field("SELECT JSON_EXTRACT(MessageIDS, %s) FROM main WHERE UserID = %s", f"$.{msg[0]}", user_id)
		sp_bonus = await db.field("SELECT SPBonus FROM main WHERE UserID = %s", user_id)
		reactions = []
		match msg[1]:
			case "0":
				message_json = json.loads(_rl)
				if isinstance(message_json, str):
					message_json = json.loads(message_json)

				laugh_reacts = message_json.get('laugh_reacts', [])
				x_reacts = message_json.get('x_reacts', [])
				recycle_reacts = message_json.get('recycle_reacts', [])
				question_reacts = message_json.get('question_reacts', [])
				heart_reacts = message_json.get('heart_reacts', [])

				if interaction.author.id == user_id:
					await interaction.response.send_message("You cannot react to your own post.", ephemeral=True)
				else:
					if interaction.author.id not in laugh_reacts:
						laugh_reacts.append(interaction.author.id)
						await db.execute("UPDATE main SET MonthlySP = MonthlySP + %s, LaughPts = LaughPts + 1 WHERE UserID = %s", 1 + sp_bonus, user_id)
					else:
						laugh_reacts.remove(interaction.author.id)
						await db.execute("UPDATE main SET MonthlySP = MonthlySP - %s, LaughPts = LaughPts - 1 WHERE UserID = %s", 1 + sp_bonus, user_id)
					message_json['laugh_reacts'] = laugh_reacts
					updated_json = json.dumps(message_json)
					await db.execute("UPDATE main SET MessageIDS = JSON_SET(MessageIDS, %s, %s) WHERE UserID = %s", f"$.{msg[0]}", updated_json, user_id)
					reactions.extend([f"{len(laugh_reacts)}", f"{len(x_reacts)}", f"{len(recycle_reacts)}", f"{len(question_reacts)}", f"{len(heart_reacts)}"])
			case "1":
				message_json = json.loads(_rl)
				if isinstance(message_json, str):
					message_json = json.loads(message_json)
				
				laugh_reacts = message_json.get('laugh_reacts', [])
				x_reacts = message_json.get('x_reacts', [])
				recycle_reacts = message_json.get('recycle_reacts', [])
				question_reacts = message_json.get('question_reacts', [])
				heart_reacts = message_json.get('heart_reacts', [])

				if interaction.author.id == user_id:
					await interaction.response.send_message("You cannot react to your own post.", ephemeral=True)
				else:
					if interaction.author.id not in x_reacts:
						x_reacts.append(interaction.author.id)
						await db.execute("UPDATE main SET MonthlySP = MonthlySP - %s, XPts = XPts + 1 WHERE UserID = %s", 1 + sp_bonus, user_id)
					else:
						x_reacts.remove(interaction.author.id)
						await db.execute("UPDATE main SET MonthlySP = MonthlySP + %s, XPts = XPts + 1 WHERE UserID = %s", 1 + sp_bonus, user_id)
					message_json['x_reacts'] = x_reacts
					updated_json = json.dumps(message_json)
					await db.execute("UPDATE main SET MessageIDS = JSON_SET(MessageIDS, %s, %s) WHERE UserID = %s", f"$.{msg[0]}", updated_json, user_id)
					reactions.extend([f"{len(laugh_reacts)}", f"{len(x_reacts)}", f"{len(recycle_reacts)}", f"{len(question_reacts)}", f"{len(heart_reacts)}"])
			case "2":
				message_json = json.loads(_rl)
				if isinstance(message_json, str):
					message_json = json.loads(message_json)
				
				laugh_reacts = message_json.get('laugh_reacts', [])
				x_reacts = message_json.get('x_reacts', [])
				recycle_reacts = message_json.get('recycle_reacts', [])
				question_reacts = message_json.get('question_reacts', [])
				heart_reacts = message_json.get('heart_reacts', [])

				if interaction.author.id == user_id:
					await interaction.response.send_message("You cannot react to your own post.", ephemeral=True)
				else:
					if interaction.author.id not in recycle_reacts:
						recycle_reacts.append(interaction.author.id)
						await db.execute("UPDATE main SET MonthlySP = MonthlySP - %s, RecPts = RecPts + 1 WHERE UserID = %s", 0.5 + sp_bonus, user_id)
					else:
						recycle_reacts.remove(interaction.author.id)
						await db.execute("UPDATE main SET MonthlySP = MonthlySP + %s, RecPts = RecPts + 1 WHERE UserID = %s", 0.5 + sp_bonus, user_id)
					message_json['recycle_reacts'] = recycle_reacts
					updated_json = json.dumps(message_json)
					await db.execute("UPDATE main SET MessageIDS = JSON_SET(MessageIDS, %s, %s) WHERE UserID = %s", f"$.{msg[0]}", updated_json, user_id)
					reactions.extend([f"{len(laugh_reacts)}", f"{len(x_reacts)}", f"{len(recycle_reacts)}", f"{len(question_reacts)}", f"{len(heart_reacts)}"])
			case "3":
				message_json = json.loads(_rl)
				if isinstance(message_json, str):
					message_json = json.loads(message_json)
				
				laugh_reacts = message_json.get('laugh_reacts', [])
				x_reacts = message_json.get('x_reacts', [])
				recycle_reacts = message_json.get('recycle_reacts', [])
				question_reacts = message_json.get('question_reacts', [])
				heart_reacts = message_json.get('heart_reacts', [])

				if interaction.author.id == user_id:
					await interaction.response.send_message("You cannot react to your own post.", ephemeral=True)
				else:
					if interaction.author.id not in question_reacts:
						question_reacts.append(interaction.author.id)
					else:
						question_reacts.remove(interaction.author.id)
					message_json['question_reacts'] = question_reacts
					updated_json = json.dumps(message_json)
					await db.execute("UPDATE main SET MessageIDS = JSON_SET(MessageIDS, %s, %s) WHERE UserID = %s", f"$.{msg[0]}", updated_json, user_id)
					reactions.extend([f"{len(laugh_reacts)}", f"{len(x_reacts)}", f"{len(recycle_reacts)}", f"{len(question_reacts)}", f"{len(heart_reacts)}"])
			case "4":
				message_json = json.loads(_rl)
				if isinstance(message_json, str):
					message_json = json.loads(message_json)
				
				laugh_reacts = message_json.get('laugh_reacts', [])
				x_reacts = message_json.get('x_reacts', [])
				recycle_reacts = message_json.get('recycle_reacts', [])
				question_reacts = message_json.get('question_reacts', [])
				heart_reacts = message_json.get('heart_reacts', [])

				if interaction.author.id == user_id:
					await interaction.response.send_message("You cannot react to your own post.", ephemeral=True)
				else:
					if interaction.author.id not in heart_reacts:
						heart_reacts.append(interaction.author.id)
					else:
						heart_reacts.remove(interaction.author.id)
					message_json['heart_reacts'] = heart_reacts
					updated_json = json.dumps(message_json)
					await db.execute("UPDATE main SET MessageIDS = JSON_SET(MessageIDS, %s, %s) WHERE UserID = %s", f"$.{msg[0]}", updated_json, user_id)
					reactions.extend([f"{len(laugh_reacts)}", f"{len(x_reacts)}", f"{len(recycle_reacts)}", f"{len(question_reacts)}", f"{len(heart_reacts)}"])
			case _:
				message_json = json.loads(_rl)
				if isinstance(message_json, str):
					message_json = json.loads(message_json)
				
				laugh_reacts = message_json.get('laugh_reacts', [])
				x_reacts = message_json.get('x_reacts', [])
				recycle_reacts = message_json.get('recycle_reacts', [])
				question_reacts = message_json.get('question_reacts', [])
				heart_reacts = message_json.get('heart_reacts', [])

				if interaction.author.id == user_id:
					await interaction.response.send_message("You cannot react to your own post.", ephemeral=True)
				else:
					if interaction.author.id not in laugh_reacts:
						laugh_reacts.append(interaction.author.id)
						await db.execute("UPDATE main SET MonthlySP = MonthlySP + %s WHERE UserID = %s", 1 + sp_bonus, user_id)
					else:
						laugh_reacts.remove(interaction.author.id)
						await db.execute("UPDATE main SET MonthlySP = MonthlySP - %s WHERE UserID = %s", 1 + sp_bonus, user_id)
					message_json['laugh_reacts'] = laugh_reacts
					updated_json = json.dumps(message_json)
					await db.execute("UPDATE main SET MessageIDS = JSON_SET(MessageIDS, %s, %s) WHERE UserID = %s", f"$.{msg[0]}", updated_json, user_id)
					reactions.extend([f"{len(laugh_reacts)}", f"{len(x_reacts)}", f"{len(recycle_reacts)}", f"{len(question_reacts)}", f"{len(heart_reacts)}"])

		for compo in components:
			compo.custom_id = f"{msg[0]}:{c}"
			compo.label = reactions[c]
			
			c += 1
		await interaction.response.edit_message(components=components)

def setup(client):
	client.add_cog(background_process(client))