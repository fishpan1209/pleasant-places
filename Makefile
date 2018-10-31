DATA=data/isd-history.csv \
	data/gsod_2009.tar \
	data/gsod_2010.tar \
	data/gsod_2011.tar \
	data/gsod_2012.tar \
	data/gsod_2013.tar \
	data/gsod_2014.tar \
	data/gsod_2015.tar \
	data/gsod_2016.tar \
	data/gsod_2017.tar

ALL : work/norm.json

src/github.com/kellegous/pork:
	@GOPATH=`pwd` go get github.com/kellegous/pork

bin/% : src/cmds/%.go
	@GOPATH=`pwd` go build -o $@ $<

bin/build-grid: work/zips.json
	@GOPATH=`pwd` go build -o $@ src/cmds/build-grid.go

bin/serve: src/cmds/serve.go src/github.com/kellegous/pork
	@GOPATH=`pwd` go build -o $@ src/cmds/serve.go

data/isd-history.csv: bin/download
	@echo 'DOWNLOADING GSOD DATA'
	@./bin/download 2009-2017

data/gsod_%.tar : bin/download
	@echo 'DOWNLOADING GSOD DATA'
	@./bin/download 2009-2017

work/zips.json: bin/build-zips
	@echo 'BUILDING ZIP DATA'
	@./bin/build-zips

work/norm.json: bin/build-grid $(DATA)
	@echo 'BUILDING GRID DATA'
	@./bin/build-grid

check: bin/check-deps
	@./bin/check-deps

serve: bin/serve work/norm.json
	@./bin/serve

clean:
	rm -rf work bin

nuke: clean
	rm -rf $(DATA) src/github.com
