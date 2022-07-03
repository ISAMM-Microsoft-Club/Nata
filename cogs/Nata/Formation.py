import multiprocessing
import time
from dataclasses import dataclass

from discord.utils import get

@dataclass
class Formation:
  bot : ...
  ctx : ...
  time : int
  chef : int

  def __post_init__(self):
    self.time = int(self.time)
    self.chef = int(self.chef)
    print(f" Sudo : {self.chef}")
    thread = multiprocessing.Process(target=self.presence, args=("_",))
    thread.start()

  async def confirmation(self):
    await self.ctx.send("Formation in {} seconds".format(self.time))

  def presence (self, _):
    time.sleep(self.time)
    channel = self.bot.get_channel(992785842101813251) #gets the channel you want to get the list from

    for member in channel.voice_states.keys() :
      user = get(self.bot.get_all_members(), id=member)
      print(user)
