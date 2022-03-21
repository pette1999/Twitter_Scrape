# In here will be the helper methods
import csv
from tempfile import NamedTemporaryFile
import shutil

def createCSV(filename, header):
  with open(filename, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

def writeToFile(filename, data):
  with open(filename, 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the data
    writer.writerow(data)

def editFile(filename, dataChange, newData):
  tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
  with open(filename, 'r', newline='') as csvFile, tempfile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    writer = csv.writer(tempfile, delimiter=',', quotechar='"')
    for row in reader:
      if row[0] == dataChange:
        row = newData
      if newData != []:
        writer.writerow(row)
  shutil.move(tempfile.name, filename)
  
def readCol(filename, colName):
  id = []
  file = csv.DictReader(open(filename, 'r'))
  for col in file:
    id.append(col[colName])

  return id
