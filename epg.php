<?php
error_reporting(0);
ini_set('display_errors', 0);
//date_default_timezone_set('Asia/Kolkata');
date_default_timezone_set('Europe/London' );
//$date = date('d_m_y_H_i', $_REQUEST["t"]);


//$xml = array2xml($jSON, false);

echo '<?xml version="1.0" encoding="utf-8"?>
<tv generator-info-name="techiesneh" generator-info-url="https://instagram.com/techiesneh">
    <channel id="indtvprogram">
        <display-name lang="en">Indtv</display-name>
    </channel>
';
$ch = file_get_contents('ch.json');
$result = json_decode($ch);
//print_r($result);
foreach($result as $page){
	echo' <channel id="'.$page->channel_id.'">
        <display-name lang="en">'.$page->channel_id.'</display-name>
    </channel>
';
	
} 
$ch = file_get_contents('ch.json');
$result = json_decode($ch);
//print_r($result);
foreach($result as $page){
	$raw_data = file_get_contents("https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?offset=0&channel_id=$page->channel_id&langId=6" );
$raw_data = gzdecode ($raw_data) ;
$raw_data=str_replace("&" ,"",$raw_data);
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
	echo'<programme   channel="'.$page->channel_id.'" start="'.$start.' +0000" stop="'.$end.' +0000">
  <title lang="en">'.$page->showname.' 
  </title>
  <desc lang="en">'.$page->description.'
  </desc>
   </programme>
';

}
	
} 

//print_r($jSON);
for ($x = 0; $x <= 1; $x++) {
$raw_data = file_get_contents("https://jiotvapi.cdn.jio.com/apis/v1.3/getepg/get?offset=$x&channel_id=1162&langId=6");
$raw_data = gzdecode ($raw_data) ;
//print_r($raw_data);
$jSON = json_decode($raw_data);
$jSON=$jSON->epg;
foreach($jSON as $page){
	$start=$page->startEpoch;
	$end=$page->endEpoch;
	$start=substr($start, 0, -3);
	$end=substr($end, 0, -3);
	$start = date('YmdHis', $start);
	$end = date('YmdHis', $end);
	echo'<programme   channel="indtvprogram" start="'.$start.' +0000" stop="'.$end.' +0000">
  <title lang="en">Program
  </title>
  <desc lang="en">Program
  </desc>
   </programme>
';

}}
echo'</tv> ';