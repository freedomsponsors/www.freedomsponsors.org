import requests

def usd2brl():
	url = 'http://www.google.com/ig/calculator?hl=en&q=1USD%3D%3FBRL'
	response = requests.get(url)
	#sample response.content: '{lhs: "1 U.S. dollar",rhs: "2.02739826 Brazil reais",error: "",icc: true}'
	return float(response.content.split('rhs:')[1].split(',')[0].split('"')[1].split(' ')[0])