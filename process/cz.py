import csv

class County(object):
    def __init__(self, name):
        self.name = name
        self.zips = []


class CommutingZone(object):
    def __init__(self, id):
        self.cz_id = id
        self.counties = {}

    def print_cz(self):
        res = []
        for name, county in self.counties.iteritems():
            res.append("{}: {}".format(name, ",".join(county.zips)))
        print(self.cz_id, res)



def build_cz():
    cz_map = {}
    with open("cz.csv") as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            cz_id, county, zip = row[0].strip(), row[1].strip(), row[2].strip()
            if cz_id in cz_map:
                cz = cz_map[cz_id]
            else:
                cz = CommutingZone(cz_id)
                cz_map[cz_id] = cz

            if county in cz.counties:
                cz.counties[county].zips.append(zip)
            else:
                new_county = County(county)
                new_county.zips.append(zip)
                cz.counties[county] = new_county

    for id, cz in cz_map.iteritems():
        cz.print_cz()

build_cz()



