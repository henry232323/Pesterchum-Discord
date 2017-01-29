import discord


class DiscordClient(discord.Client):
    def __init__(self, app=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)        
        self.app = app

    async def dispatch(self, event, *args, **kwargs):
        super().dispatch(event, *args, **kwargs)
        coro = getattr(self.app, 'on_' + event)
        if coro is not None:
            await coro(*args, **kwargs)