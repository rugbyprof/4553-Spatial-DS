<?php

getPriSecRoads();

    
function getPriSecRoads(){
	for($i=1;$i<=78;$i++){
		
		if($i < 10){
			$n = "0".$i;
		}else{
			$n = $i;
		}
		$url = "http://www2.census.gov/geo/tiger/TIGER2013/PRISECROADS/tl_2013_{$n}_prisecroads.zip";
		
		echo $url."\n";
		if (@file_get_contents($url,0,null,0,1)) {
			if(!file_exists("./tl_2013_{$n}_prisecroads.zip")){    
				exec("wget -N http://www2.census.gov/geo/tiger/TIGER2013/PRISECROADS/tl_2013_{$n}_prisecroads.zip");
		
				exec("unzip -u tl_2013_{$n}_prisecroads.zip");
			
				exec("python shp2gj.py tl_2013_{$n}_prisecroads.shp tl_2013_{$n}_prisecroads.json");
			}
		}
	}
}

