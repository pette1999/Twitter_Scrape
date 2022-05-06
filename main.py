import scrape
from tqdm import tqdm
import random
import time
import browser

def main():
  message = "Please checkout our new generative art Spectrum by @LibertasART, if you like it you can have one on opensea: https://opensea.io/collection/libertasart"
  
  while True:
    sleepTime = random.randrange(1800, 3600, 30)
    scrape.getTargetTweets('drop%20your%20nft')
    browser.reply(message)
    for i in tqdm(range(sleepTime), desc="Waiting time: "):
      time.sleep(1)

main()
