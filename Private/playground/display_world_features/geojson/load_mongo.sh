mongo world_data --eval "db.dropDatabase()"
mongoimport --db world_data --collection airports       --type json --file airports_combined.geojson    --jsonArray
mongoimport --db world_data --collection countries      --type json --file countries.geojson            --jsonArray
mongoimport --db world_data --collection meteorites     --type json --file meteorite-landings.geojson   --jsonArray
mongoimport --db world_data --collection volcanos       --type json --file world_volcanos.geojson       --jsonArray
mongoimport --db world_data --collection earthquakes    --type json --file earthquakes.geojson          --jsonArray
mongoimport --db world_data --collection cities         --type json --file world_cities.geojson         --jsonArray
mongoimport --db world_data --collection states         --type json --file state_borders.geojson        --jsonArray