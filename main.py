import scrape
from tqdm import tqdm
import random
import time

def main():
  while True:
    sleepTime = random.randrange(1800, 3600, 30)
    scrape.replyRecentTweets('drop%20your%20nft')
    for i in tqdm(range(sleepTime), desc="Waiting time: "):
      time.sleep(1)

main()
