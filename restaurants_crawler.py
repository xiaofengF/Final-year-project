from bs4 import BeautifulSoup
import requests
import re
import MySQLdb

urls = [];

def insertFromDict(table, dict):
    #Insert to table
    sql = 'INSERT INTO ' + table
    sql += ' ('
    sql += ', '.join(dict)
    sql += ') VALUES ('
    sql += ', '.join(map(dictValuePad, dict))
    sql += ');'
    return sql

def dictValuePad(key):
    return '%(' + str(key) + ')s'

#Restaurants pages
for i in range(0, 605):
	var = str(30 * i)
	urls.append('https://www.tripadvisor.com/RestaurantSearch-g186338-oa' + var + '-London_England.html%23EATERY_LIST_CONTENTS')
print("url done")

#Connect to the database
db = MySQLdb.connect(host='localhost', user='root',passwd='961127',db='django')
cursor = db.cursor()
db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

for url in urls:
	data = requests.get(url)
	soup = BeautifulSoup(data.text, 'lxml')
	# Get data from the website
	titles = soup.select('div.title > a.property_title')
	rates = soup.select('div.popIndexBlock > div.popIndex')
	features = soup.select('div.cuisines')
	links = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(titles))
	locations = []
	phones = []
	postLeft = []
	postRight = []

	for link in links:
		inner_url = 'https://www.tripadvisor.com' + link
		inner_data = requests.get(inner_url)
		inner_soup = BeautifulSoup(inner_data.text, 'lxml')
		location = inner_soup.select(' div.headerBL > div.blRow > div.address')
		phone = inner_soup.select('div.headerBL > div.blRow > div.phone')

		for loc,ph in zip(location,phone):
			l = loc.get_text()
			ll = l[l.rfind('o') + 3: -9]
			llleft = ll[:ll.find(' ')]
			llright = ll[ll.find(' ') + 1:]
			postLeft.append(llleft)
			postRight.append(llright)
			locations.append(l)
			phones.append(ph.get_text())

	for title,rate,feature,lo,p,x,y in zip(titles,rates,features,locations,phones,postLeft,postRight):
		#Data processing
		#Delete \n in the text
		t = title.get_text()[1:-1]
		r = rate.get_text()[1:-1]
		#Get the rank number from the text
		ra = r[1:r.find(' ')]
		#divide features
		f = feature.get_text()[1:-1]
		fe = f[f.find('\n') + 1:]
		feature_list = fe.split('\n')
		price = f[:f.find('\n')]

		#Store data
		for fea in feature_list:
			restaurant = {
				'title':t,
				'rate':ra,
				'feature':fea,
				'location':lo,
				'phone':p,
				'price':price,
				'postLeft':x,
				'postRight':y
			}
			# insert data into database
			sql = insertFromDict("Restaurants_data", restaurant)
			cursor.execute(sql, restaurant)
			db.commit()

cursor.close()
db.close()