import discord
from discord.ext import commands

bot=commands.Bot(command_prefix='!')

approved_roles=['Admin','Bot'] #add roles that can clear and call members from the queue
_queue=[]

def is_approved():
	def predicate(ctx):
		author=ctx.message.author
		if author is ctx.message.server.owner:
			return True
		if any(role.name in approved_roles for role in author.roles):
			return True
	return commands.check(predicate)

@bot.event
async def on_ready():
	print(bot.user.name)
	print(bot.user.id)

@bot.command(pass_context=True)
async def add(ctx):
	''': Add yourself to the queue'''
	author=ctx.message.author
	if author.id not in _queue:
		_queue.append(author.id)
		await bot.send_message(author,'You have been added to the queue')

@bot.command(pass_context=True)
async def remove(ctx):
	''': Remove yourself from the queue'''
	author=ctx.message.author
	if author.id in _queue:
		_queue.remove(author.id)
		await bot.send_message(author,'You have been removed from the queue')
@bot.command()
async def queue():
	''': See who's in the queue'''
	place=1
	message=''
	for member in _queue:
		message+='**#{}** : <@{}>'.format(place,member)
		place+=1
	if message != '':
		await bot.say(message)
	else:
		await bot.say('Queue is empty')

@bot.command(pass_context=True)
async def position(ctx):
	''': Check your postion in the queue'''
	author=ctx.message.author
	if author.id in _queue:
		await bot.send_message(author,'You are **#{}** in the queue.'.format(_queue.index(author.id)+1))

@is_approved()
@bot.command(pass_context=True)
async def call(ctx):
	''': Call the next member in the queue'''
	if len(_queue)>0:
		member=discord.utils.get(ctx.message.server.members,id=_queue[0])
		await bot.send_message(member,"You're up, lets play!")
		await bot.send_message(ctx.message.author,'{} has been sent a message to play'.format(member.name))
		await bot.say('**{}** has been called up. The queue has been updated.'.format(member.mention))
		_queue.remove(_queue[0])

@is_approved()
@bot.command()
async def clear():
	''': Clears the queue'''
	global _queue
	_queue=[]
	await bot.say('Queue has been cleared')

bot.run('TOKEN')
