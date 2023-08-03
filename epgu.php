<?php
date_default_timezone_set('Europe/London' );

//$date = date('d_m_y_H_i', $_REQUEST["t"]);


//$xml = array2xml($jSON, false);

echo '<?xml version="1.0" encoding="utf-8"?>
<tv generator-info-name="techiesneh" generator-info-url="https://instagram.com/techiesneh">
    <channel id="indtvprogram">
        <display-name lang="en">Indtv</display-name>
    </channel>
  
';

//print_r($jSON);
for ($x = 0; $x <= 5; $x++) {
$raw_data = file_get_contents("https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?offset=$x&channel_id=946&langId=6");
$raw_data = gzdecode ($raw_data) ;
//print_r($raw_data);
$jSON = json_decode($raw_data);
$jSON=$jSON->epg;
foreach($jSON as $page){
	$start=$page->startEpoch;
	
	$end=$page->endEpoch;
	
	$start=substr($start, 0, -3);
	$end=substr($end, 0, -3);
	$start=$start-3600;
	$end=$end-3600;
	$start = date('YmdHis', $start);
	$end = date('YmdHis', $end);
	echo'<programme   channel="indtvprogram" start="'.$start.' +0000" stop="'.$end.' +0000">
  <title lang="en">'.$page->showname.' 
  </title>
  <desc lang="en">'.$page->description.'
  </desc>
   </programme>
';

}} 
echo'</tv> ';