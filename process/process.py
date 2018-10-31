import json
import csv

from cz import CommutingZone, County

class Grid(object):
    def __init__(self, I, J):
        self.I = I
        self.J = J
        self.key = "{}-{}".format(I, J)

    def add_zips(self, zips):
        self.zips = zips

    def __eq__(self, other):
        if isinstance(other, Grid):
            return self.I == other.I and self.J == other.J
        return NotImplemented



def load_norm():
    with open("../work/norm.json") as file:
        norm = json.loads(file.read())

    regions = norm['Regions']
    data = {}
    for r in regions:
        grid = Grid(r['I'], r['J'])
        data[grid.key] = r['Total']
    return data


def load_info():
    info = []
    grids = []
    for line in open("../work/info.json", 'r'):
        i = json.loads(line)
        info.append(i)

    for grid_info in info:
        grid = Grid(grid_info['I'], grid_info['J'])
        if grid_info['Zips']:
            zips = [z['Code'] for z in grid_info['Zips']]
        else:
            zips = []
        grid.add_zips(zips)
        grids.append(grid)
    return grids


def build_cz():
    cz_map = {}
    with open("cz.csv") as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            cz_id, county_id, county_name, zip = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()
            if cz_id in cz_map:
                cz = cz_map[cz_id]
            else:
                cz = CommutingZone(cz_id)
                cz_map[cz_id] = cz

            if county_id in cz.counties:
                cz.counties[county_id].zips.append(zip)
            else:
                new_county = County(county_id, county_name)
                new_county.zips.append(zip)
                cz.counties[county_id] = new_county

    for id, cz in cz_map.iteritems():
        cz.consolidate_zips()
        #cz.print_zips()
    return cz_map


# ask for 60% match
def is_sublist(sublist, lst):
    if not sublist:
        return True
    inter = set(sublist).intersection(set(lst))
    return len(inter) / float(len(sublist)) >= 0.6

def match_grid_to_cz(grid, cz_map):
    if not grid:
        return
    for id, cz in cz_map.iteritems():
        if is_sublist(grid.zips,cz.zips):
            cz.add_grid(grid)
            #print("grid {} matched to cz {}".format(grid.key, cz.cz_id))
            return
    print('No match found for grid {}'.format(grid.key))


def calc_pd(cz_map, norm):
    csv = open("out.csv", "w")
    columnTitleRow = "cz_id, days, match_rate\n"
    csv.write(columnTitleRow)

    for id, cz in cz_map.iteritems():
        total = 0
        size = 0
        for grid in cz.grids:
            total += norm[grid.key]
            size += 1
        if size:
            cz.total = round(total / float(size),1)
        row = "{},{},{}\n".format(str(id), str(cz.total), str(round(cz.match_rate, 2)))
        csv.write(row)


def main():
    norm = load_norm()
    grids = load_info()
    cz_map = build_cz()
    for grid in grids:
        match_grid_to_cz(grid, cz_map)

    unmatched = []
    goodmatch = []
    for id, cz in cz_map.iteritems():
        match = cz.calc_match()
        if match == 0:
            unmatched.append(id)
        if match >= 0.8 and match <= 1.2:
            goodmatch.append(id)


    print(unmatched)
    print(len(unmatched) / float(len(cz_map)))
    print(len(goodmatch) / float(len(cz_map)))

    calc_pd(cz_map, norm)


main()