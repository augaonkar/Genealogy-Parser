from datetime import datetime, timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
#from collections import counter
import re
import sys
import pymongo
from pymongo import MongoClient
from pprint import pprint

connection = MongoClient('localhost', 27017)
db = connection['GEDCOMDB']


def birth_date_less_marriage_date():
	return_flag=False
	family=db.family.find({})
	results = [res for res in family] #count = cursor.count()
	family.close()

	for res in results: # while index != count //This will iterate the list without you needed to keep a counter:
    # doc = cursor[index] // No need for this since 'res' holds the current record in the loop cycle
	#Check age for dead person 
		wife_age = 0
		husband_age = 0
		if "marriage" in res:
			marriage_date = datetime.strptime(res["marriage"],"%Y-%m-%d %H:%M:%S")
			if "HUSBAND" in res and "WIFE" in res: 
				husband = db.people.find({"ID" : res["HUSBAND"]})
				result_for_husband = [doc for doc in husband]
				wife =  db.people.find({"ID" : res["WIFE"]})
				result_for_wife = [doc1 for doc1 in wife]
				for doc in result_for_husband:
					hbd = datetime.strptime(doc["birthday"],"%Y-%m-%d %H:%M:%S")
					print(hbd)
					husband_age = marriage_date.year - hbd.year
				for doc1 in result_for_wife:
					wbd = datetime.strptime(doc1["birthday"],"%Y-%m-%d %H:%M:%S")
					print(wbd)
					wife_age = marriage_date.year - wbd.year
			else:
				print("Husband wife no present for particular marriage")
		else:
			print("Marraiage date not present")
		
		if wife_age > 18 and husband_age > 21: 
			print("Valid Data")
				
		else:
			print("Invalid Data")

if __name__ == '__main__':
    check_birth_before_marriage = birth_date_less_marriage_date()
   