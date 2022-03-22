# In here will be the helper methods
import csv
from tempfile import NamedTemporaryFile
import shutil
import os

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
      writer.writerow(row)
  shutil.move(tempfile.name, filename)

def deleteLine(filename, dataChange):
  tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
  with open(filename, 'r', newline='') as csvFile, tempfile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    writer = csv.writer(tempfile, delimiter=',', quotechar='"')
    for row in reader:
      if row[0] != dataChange:
        writer.writerow(row)
  shutil.move(tempfile.name, filename)

def clearFile(filename, header):
  os.remove(filename)
  createCSV(filename, header)
  
def readCol(filename, colName):
  id = []
  file = csv.DictReader(open(filename, 'r'))
  for col in file:
    id.append(col[colName])

  return id

def convertDate_to_days(date):
  if(len(date.split('/')) > 1):
      return (int(date.split('/')[0])-1)*30+int(date.split('/')[1])
