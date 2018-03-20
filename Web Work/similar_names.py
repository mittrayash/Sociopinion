import requests, json

def get_names(query):
    similar = []
    URL="http://suggestqueries.google.com/complete/search?client=firefox&q=" + query + " vs"
    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    count = 0
    for x in (result[1]):
        res = x[len(query) + 4:]
        if len(res) > 0:
            count += 1
            similar.append(res.title())
        if count == 5:
            break
    return similar


