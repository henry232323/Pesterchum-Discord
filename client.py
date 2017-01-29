import discord


class DiscordClient(discord.Client):
    def __init__(self, app=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)        
        self.app = app

    async def on_ready(self):
        # Login info
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.app.on_ready()

    async def on_message(self, message):
        await self.app.on_message(message)
