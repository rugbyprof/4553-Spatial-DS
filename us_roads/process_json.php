<?php
error_reporting(1);
//       "geometry": {
//         "type": "LineString", 
//         "coordinates": [
//           [
//             -88.019893, 
//             44.519309
//           ], 
//           [
//             -88.01937699999999, 
//             44.520126
//           ], 
//           [
//             -88.01880799999999, 
//             44.520931999999995
//           ], 
//           [
//             -88.01849, 
//             44.521383
//           ], 
//           [
//             -88.018104, 
//             44.521981
//           ], 
//           [
//             -88.018, 
//             44.522124999999996
//           ], 
//           [
//             -88.01732799999999, 
//             44.523055
//           ], 
//           [
//             -88.016598, 
//             44.524097999999995
//           ]
//         ]
//       }, 
//       "type": "Feature", 
//       "properties": {
//         "RTTYP": "M", 
//         "MTFCC": "S1200", 
//         "FULLNAME": "N Broadway", 
//         "LINEARID": "110488653292"
//       }


$p = new processJson('.');

//$p->dumpDir();
$p->processDir();

class processJson{
    var $Dir;
    var $fp;
    var $i;
    var $fips;
    
    function __construct($dir){
       $temp = scandir($dir);
       array_shift($temp);
       array_shift($temp);
       
		$this->fips = file('state-fips.csv');

		for($i=0;$i<sizeof($this->fips);$i++){
			$this->fips[$i] = explode(',',trim($this->fips[$i]));
			array_pop($this->fips[$i]);
		}
       
       
        foreach($temp as $file){
           $path_parts = pathinfo($file);
           if($path_parts['extension'] == 'json'){
           	  $this->Dir[$file] = filesize($file);
           }
        }
    }
    
    function processDir(){
    	foreach($this->Dir as $file => $size){
    	    $this->processFile($file);
//     	    $this->processFile('tl_2013_54_prisecroads.json');
//     	    break;
    	}
    }
    
    function processFile($filename){
        $totals = array();
    	$this->fp = fopen($filename,'r');
    	$name = $this->getStateName($filename);
    	echo $name."\n";
    	$fo = fopen("{$name}.json","w");
    	while($obj = $this->getObject()){
    	    if(is_array($obj))
    		    fwrite($fo,print_r($obj,true));
    		    $totals[$obj['properties']['FULLNAME']]['nameCount'] += 1;
				$totals[$obj['properties']['FULLNAME']]['pointsCount'] += sizeof($obj['linestring']);

    	}
		fwrite($fo,print_r($totals,true));
		fwrite($fo,print_r(sizeof($totals),true));
    	fclose($fo);
    	fclose($this->fp);
    }
    
    function getStateName($filename){
    	 $index = substr($filename,8,2) * 1;
         return str_replace(' ','_',$this->fips[$index][2]);
    }
    
    function getObject(){
    	 $objectEnd = false;
    	 $objectArray = array();
    	 $readPoints = false;
    	 $readFeature = false;
    	 $properties = null;
    	
		 while($objectEnd == false){
		 	 $line = fgets($this->fp);
		 	 if(feof($this->fp)){
		 	 	return false;
		 	 }
			 if(strpos($line,"geometry")){
				 //kill next two lines
				 $null = fgets($this->fp);
				 $null = fgets($this->fp);
				 $readPoints = true;
			 }
			 while($readPoints){
				 $null = fgets($this->fp);
				 $x = trim(fgets($this->fp)," ,\n");
				 $y = trim(fgets($this->fp));
				 $objectArray['linestring'][] = array($x,$y);
				 $last = fgets($this->fp);
				 if(!strpos($last,","))
					$readPoints = false;
					$readFeature = true;
			 }
			 if($readFeature){
			     $null = fgets($this->fp);
			     $null = fgets($this->fp);
			     $null = fgets($this->fp);
			     $null = fgets($this->fp);

				 list($null,$properties['RTTYP']) = explode(":",trim(fgets($this->fp)," ,\n"));
				 list($null,$properties['MFTFCC']) = explode(":",trim(fgets($this->fp)," ,\n"));
				 list($null,$properties['FULLNAME']) = explode(":",trim(fgets($this->fp)," ,\n"));
				 list($null,$properties['LINEARID']) = explode(":",trim(fgets($this->fp)," ,\n"));
	  		     $objectEnd = true;
	         }
             if($properties){
				 foreach($properties as $key => $val){
					$properties[$key] = str_replace('"', '', $val);
				 }
				 $objectArray['properties'] = $properties;
				 return($objectArray);
			 }
			 return 1;
		}
        
    }
    
    
    function dumpDir(){
    	print_r($this->Dir);
    }
}