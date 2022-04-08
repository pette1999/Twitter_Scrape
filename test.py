import scrape

print("V1 API passed: ", scrape.getAPIV1())
print("V2 API passed: ", scrape.getClientV2())

try:
  scrape.followUser(1494209139064860678)
except:
  pass