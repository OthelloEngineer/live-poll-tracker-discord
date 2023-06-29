import sched

import hikari
from lightbulb.ext import tasks
import plottingservice
import strawpollservice
import json
import lightbulb
from tracked_source import TrackedSource

polls: list[TrackedSource] = []

config = json.load(open('config.json'))
token = config["token"]
channel = config["channel_id"]

bot = lightbulb.BotApp(token=token)
tasks.load(bot)


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    """If a non-bot user mentions your bot, respond with 'Pong!'."""

    # Do not respond to bots nor webhooks pinging us, only user accounts
    if not event.is_human:
        return

    me = bot.get_me()

    if me.id in event.message.user_mentions_ids:
        await event.message.respond("Pong!")


@bot.command
@lightbulb.option("poll_name", "a short name of the poll (not the question itself)", str)
@lightbulb.option("poll_link", "Link to poll", str)
@lightbulb.command('track_strawpoll', 'start a live tracking of a strawpoll')
@lightbulb.implements(lightbulb.SlashCommand)
async def start_poll_visualization(ctx: lightbulb.SlashContext):
    strawpoll_service = strawpollservice.StrawpollService()
    plotting_service = plottingservice.PlottingService()
    poll_data = strawpoll_service.get_data(ctx.options.poll_link, ctx.options.poll_name)
    plotting_service.generate_plot(poll_data)
    msg = await ctx.respond(hikari.File(ctx.options.poll_name + ".png"))
    source = TrackedSource(link=ctx.options.poll_link, name=ctx.options.poll_name, message=msg)
    polls.append(source)


@tasks.task(s=5, auto_start=True)
async def update_polls():
    global polls
    print("updating polls...")
    for poll in polls:
        strawpoll_service = strawpollservice.StrawpollService()
        plotting_service = plottingservice.PlottingService()
        poll_data = strawpoll_service.get_data(poll.link, poll.name)
        plotting_service.generate_plot(poll_data)
        print("updating poll")
        print(poll_data.reference_name)
        await poll.message.edit(hikari.File(poll_data.reference_name + ".png"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
