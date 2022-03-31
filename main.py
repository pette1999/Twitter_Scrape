import scrape

def main():
  count = 0
  while True:
    scrape.getRecentTweeter('nft','./data/people.csv')
    scrape.followAndHello('./data/following.csv', 'PeterCh39124642')
    scrape.time.sleep(1800)
    count += 1
    if count % 48 == 0:
      scrape.check()

main()
 