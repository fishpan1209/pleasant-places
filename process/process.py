import json


class Region(object):
    def __init__(self, I, J, city, total):
        self.I = I
        self.J = J
        self.city = city
        self.total = total

def load_norm():
    with open("../work/norm.json") as file:
        norm = json.loads(file.read())

    regions = norm['Regions']
    data = []
    for r in regions:
        region = Region(r['I'], r['J'], r['City'],r['Total'])
        data.append(region)
    for d in data:
        print(d.city, d.total)



def main():
    load_norm()


main()