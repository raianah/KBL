import os, time, time
from disnake.ext.commands import Bot as BotBase, errors
from dotenv import load_dotenv
from disnake import Intents, Activity, ActivityType, AllowedMentions, Embed, Status
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..db import db
from glob import glob

load_dotenv()

token, token_ = os.getenv("MAIN_TOKEN"), os.getenv("BETA_TOKEN")
COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f"{cog} is ready.")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
	def __init__(self):
		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)
		super().__init__(command_prefix=".", case_insensitive=True, intents=Intents.all(), strip_after_prefix=True, allowed_mentions=AllowedMentions(roles=True, everyone=False, users=True, replied_user=True))

	def setup(self):
		for cog in os.listdir('./cogs'):
			if cog.endswith(".py"):
				try:
					cog = f"cogs.{cog.replace('.py', '')}"
					self.load_extension(cog)
				except Exception as e:
					print(f"{cog} can not be loaded.\nReason: {e}")

	def run(self):
		print("Running setup...")
		self.setup()

		print("Getting the token...")

		super().run(token_, reconnect=True)

	async def on_connect(self):
		print("Connected!")
		await bot.change_presence(activity=Activity(type=ActivityType.playing, name=f'discord.gg/kbl'))

	async def on_disconnect(self):
		print("Disconnected!")

	async def on_ready(self):
		self.scheduler.start()
		print("Ready!")
		guild = bot.get_guild(961502956195303494)
		print(guild.name, len(guild.members))
		index, t_index = 0, 0
		for member in guild.members:
			roles = [role.id for role in member.roles]
			reg = db.record("SELECT * FROM main WHERE UserID = ?", member.id)
			if reg is None and not member.bot and 961967298955079740 in roles:
				db.execute("INSERT INTO main (UserID) VALUES (?)", member.id)
				db.execute("INSERT INTO items (UserID) VALUES (?)", member.id)
				db.execute("INSERT INTO colors (UserID) VALUES (?)", member.id)
				index += 1
		for member in guild.members:
			roles = [role.id for role in member.roles]
			if 961967298955079740 in roles:
				db.execute("INSERT INTO trophies (UserID) VALUES (?)", member.id)
				t_index += 1
		print(f"{index} members registered.\n{t_index} members added.")

	async def on_command_error(self, ctx, error):
		if isinstance(error, errors.BadUnionArgument):
			return await ctx.send(f"Please check your `channel` input. It should be a text/voice/forum channel.")
		if isinstance(error, errors.CommandNotFound):
			return
		else:
			await ctx.send("Oops, an error occurred. The said error is being sent to the developer.")
			user = await ctx.guild.fetch_member(603256030742183959)
			await user.send(f"{error} | {ctx.author} | <t:{int(time.time())}:D> (<t:{int(time.time())}:R>)")
			raise error

bot = Bot()