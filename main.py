import googlemaps,pprint,time,csv,requests,json,re

userLat = input("Enter Latitude: ")
userLng = input("Enter Longitude: ")
rad = input("Enter Range - default: 1000: ")
search = input("What are you Looking For: ")
    
# userLat = '43.333592'
# userLng = '-79.879476'
storageDict = dict()
counter = 1
locationChosen = []
valid=False
directionsList = []
directionCounter = 1


api_key = "Enter Your API key"
gmaps = googlemaps.Client(key=api_key)

result = gmaps.places_nearby(location = userLat+","+userLng, radius = rad, open_now=True, type=search)

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


with open("Locations.csv",'w') as csvfile:
    field_names = ['Selection','Name','Address','Rating', 'Distance', 'Duration']
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    
    for location in result['results']:
        locLat = location['geometry']['location']['lat']
        locLng = location['geometry']['location']['lng']
        
        origin = (userLat,userLng)
        destination = (locLat,locLng)
        
        distance_matrix = gmaps.distance_matrix(origin,destination)
        distance = distance_matrix['rows'][0]['elements'][0]['distance']['text']
        travelTime = distance_matrix['rows'][0]['elements'][0]['duration']['text']
        
        storageDict.update({counter:[location['name'], location['vicinity'], location['rating'], distance, travelTime]})
        writer.writerow({'Selection':counter,'Name':location['name'],'Address':location['vicinity'],'Rating':location['rating'],'Distance':distance,'Duration':travelTime})
        counter += 1
        

while valid == False:
    selection = input("Make a Selection According to the CSV File: ")
    for loc in storageDict:
        if loc == int(selection):
            valid = True
            locationChosen = storageDict[loc]
    if valid == False:
        print("Invalid Selection. Try Again")

getDirectionsURL = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}".format(distance_matrix['origin_addresses'][0], location['vicinity'], api_key)
payload={}
headers = {}

response = requests.request("GET", getDirectionsURL, headers=headers, data=payload)

dictVersion = json.loads(response.text)
for x in dictVersion['routes'][0]['legs'][0]['steps']:
    directionsList.append(x['html_instructions'])
        
with open("Directions.txt",'w') as fh:
    fh.writelines("Directions to " + location['vicinity'] + " From " + distance_matrix['origin_addresses'][0] + "\n\n")
    for eachDirection in directionsList:
        eachDirection = remove_html_tags(eachDirection)
        fh.writelines(str(directionCounter) + " --> " + eachDirection + "\n")
        directionCounter += 1
print("Your Directions to " + location['vicinity'] + " are posted in a text file located in this directory")




    
    
   