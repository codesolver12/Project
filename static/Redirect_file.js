// This page is to reset the local storage values
function setDefault(){
    console.log("======================")
    console.log("======================")
    console.log("======================")
localStorage.setItem('route_name', '/random_number');
localStorage.setItem('deploy_update',false);
localStorage.removeItem('time_key','alt_key','status_key');
localStorage.setItem('datapoints',[0,0,0,0,0,0,0,0,0]);
localStorage.setItem('zoneLatitude',['--','--','--','--']);
localStorage.setItem('zoneLongitude',['--','--','--','--']);
localStorage.setItem('zonecolour',['lightgray','lightgray','lightgray','lightgray']);
localStorage.setItem('zonestatus',['false','false','false','false'])
}
function changepage(){
    window.location.href = '/home';
}
setDefault();
changepage();