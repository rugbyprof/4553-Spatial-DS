mongo world_data --eval "db.dropDatabase()"
mongoimport --db world_data --collection airports --type json --file geojson/airports_combined.geojson --jsonArray
mongoimport --db world_data --collection countries --type json --file geojson/countries.geo.json --jsonArray
mongoimport --db world_data --collection meteorites --type json --file geojson/meteorite-landings.geojson --jsonArray
mongoimport --db world_data --collection volcanos --type json --file geojson/world_volcanos2.geojson --jsonArray
mongoimport --db world_data --collection earthquakes --type json --file geojson/earthquakes.geojson --jsonArray
mongoimport --db world_data --collection cities --type json --file geojson/world_cities.geojson --jsonArray
mongoimport --db world_data --collection states --type json --file geojson/state_borders.json --jsonArray