import scrape

def main():
  while True:
    scrape.getRecentTweeter('nft','./data/people.csv')
    scrape.followAndHello('./data/following.csv', 'chen_haifan')
    scrape.time.sleep(3600)

main()
