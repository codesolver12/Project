function CheckReleaseData(){

    const time_key = 'time_key';
    const alt_key = 'alt_key';
    const status_key = 'status_key';


    let stored_release_time = localStorage.getItem('time_key');
    let stored_release_alt = localStorage.getItem('alt_key');
    let stored_release_status = localStorage.getItem('status_key');


    if (stored_release_time === null || stored_release_alt === null || stored_release_status === null){
    stored_release_time = '--:--:--';
    stored_release_alt = '-- ft.';
    stored_release_status ='ARMED';
    localStorage.setItem(time_key, stored_release_time);
    localStorage.setItem(alt_key, stored_release_alt);
    localStorage.setItem(status_key, stored_release_status);
    updateReleaseData();
    }
}


function updateReleaseData() {

let stored_release_time = localStorage.getItem('time_key');
let stored_release_alt = localStorage.getItem('alt_key');
let stored_release_status = localStorage.getItem('status_key');

document.getElementById('RELEASE_TIME').textContent = stored_release_time;
document.getElementById('RELEASE_ALTITUDE').textContent = stored_release_alt;
document.getElementById('PADA_STATUS').textContent = stored_release_status;
}
