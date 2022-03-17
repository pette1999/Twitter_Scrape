# In here will be the helper methods
import csv

def createCSV(filename, header):
  with open(filename, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

def writeToFile(filename, data):
  with open(filename, 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the data
    writer.writerow(data)

def readCol(filename, colName):
  id = []
  file = csv.DictReader(open(filename, 'r'))
  for col in file:
    id.append(col[colName])

  return id
