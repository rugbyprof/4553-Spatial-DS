<?php

$sizes = array();

for($i=12;$i<=64;$i+=2){
    $sizes[] = $i;
    exec("mkdir letters_lower_{$i}");
    exec("mkdir letters_upper_{$i}");
    exec("mkdir numbers_{$i}");
}

foreach($sizes as $s){
    for($l=97;$l<=122;$l++){
        $letter = chr($l);
        exec("convert -background white -fill black -font /Library/Fonts/Courier\ New\ Bold.ttf -pointsize {$s} label:{$letter} -gravity center ./letters_lower_{$s}/{$letter}.png");
    }
    for($l=65;$l<=90;$l++){
        $letter = chr($l);
        exec("convert -background white -fill black -font /Library/Fonts/Courier\ New\ Bold.ttf -pointsize {$s} label:{$letter} -gravity center ./letters_upper_{$s}/{$letter}.png");
    }

    for($l=48;$l<=57;$l++){
        $letter = chr($l);
        exec("convert -background white -fill black -font /Library/Fonts/Courier\ New\ Bold.ttf -pointsize {$s} label:{$letter} -gravity center ./numbers_{$s}/{$letter}.png");
    }
}
