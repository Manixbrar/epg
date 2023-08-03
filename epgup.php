<?php
$p= file_get_contents("http://localhost:8080/epg.php");

//Our original number.
//$originalNumber = $p;

//Get 2.25% of 100.
//$numberToAdd = (1 / 100) * 100;

//Finish it up with some simple addition
//$newNumber = $originalNumber + $numberToAdd;

//Result is 102.25
//echo $newNumber;
//$p= gzencode($p) ;
//$p= gzcompress('$p', 8);
//echo $p;
$compressedContent = gzencode($p , 9);
//echo $compressedContent;
// Save the compressed content to a .xml.gz file
$myfile = fopen("yepg.xml.gz", "w") or die("Unable to open file!");
fwrite($myfile, $compressedContent);
fclose($myfile);
echo "Refresh done" ;