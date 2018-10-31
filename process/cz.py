
class County(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.zips = []
        self.grids = []


class CommutingZone(object):
    def __init__(self, id):
        self.cz_id = id
        self.counties = {}
        self.grids = []
        self.total = -1
        self.pop = 0

    def consolidate_zips(self):
        zips = []
        for county_id, county in self.counties.iteritems():
            zips.extend(county.zips)
        self.zips = zips

    def print_cz(self):
        res = []
        for id, county in self.counties.iteritems():
            res.append("{}-{}: {}".format(id, county.name, ",".join(county.zips)))
        print(self.cz_id, res)

    def print_zips(self):
        print(self.cz_id, self.zips)

    def add_grid(self, grid):
        self.grids.append(grid)
        self.pop += grid.pop

    def calc_match(self):
        matched_zips = [z for grid in self.grids for z in grid.zips]
        self.match_rate = len(matched_zips) / float(len(self.zips))
        return self.match_rate








