import json
import re
import requests
from django.http import HttpResponse

def root(request):
    root_file = open("../public/index.html")
    response = HttpResponse(root_file.read())
    root_file.close()
    return response

def public(request):
    path = ".."+request.path
    static_file = open(path)
    response = HttpResponse(static_file.read(),content_type='application/javascript')
    static_file.close()
    return response

def search(request):
    phrase = request.GET['phrase']
    url =('https://v2.sg.media-imdb.com/suggests/%s/%s.json'%(phrase[0].lower(),phrase.lower())).replace(' ','_')
    data_response = requests.get(url)
    data = re.sub(r"^imdb\$\w+\(","[",data_response.text)
    data = re.sub(r"}\)$","}]",data)
    data_json = json.loads(data)[0]["d"]
    result_array=[]
    for item in data_json:
        if(re.match(r"tt\d+",item["id"])):
            result_array.append({
                "name": item["l"],
                "id": item["id"]
            })
    response = HttpResponse(json.dumps(result_array),content_type='application/json')
    return response

def node(request):
    imdb_id= request.GET['imdb_id']

    json.dumps({"field":"value"})
    result = "Text"

    return HttpResponse(result,content_type='application/json')