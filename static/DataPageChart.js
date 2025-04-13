function deployPADA(){      // Function activated once PADA is released(Clicking button on GUI or physical switch for dropping mechanism)
    localStorage.setItem('route_name','/random_number_deployed');   // Change route name in local storage to PADA-deployed version
    localStorage.setItem('deploy_update',true);     // Set the deployment status update requirement to true
    localStorage.setItem('PADAimgSRC',"{{ url_for('serve_static', filename='PADA_BUTTON_DEPLOYED.png') }}")

    const displayedImage = document.getElementById('PADA_STATUS_IMAGE');
    //displayedImage.src = localStorage.getItem('PADAimgSRC');
    //displayedImage.src = "{{ url_for('serve_static', filename='PADA_BUTTON_DEPLOYED.png') }}"


    updateChartData();     // Call function
}




function CheckReleaseData(){ // function called whenever page is reloaded to check if pada has been deployed
    let stored_release_time = localStorage.getItem('time_key');
    let stored_release_alt = localStorage.getItem('alt_key');
    let stored_release_status = localStorage.getItem('status_key');


    if (stored_release_time === null || stored_release_alt === null || stored_release_status === null){
        stored_release_time = '--:--:--';
        stored_release_alt = '-- ft.';
        stored_release_status ='ARMED';
        localStorage.setItem('time_key', stored_release_time);
        localStorage.setItem('alt_key', stored_release_alt);
        localStorage.setItem('status_key', stored_release_status);   
    }
    updateReleaseData();
}

function updateReleaseData() { // function to update release data boxes, called on refresh and when pada button clicked

    // console.log("USING UPDATE RELEASE DATA")
    let stored_release_time = localStorage.getItem('time_key');
    let stored_release_alt = localStorage.getItem('alt_key');
    let stored_release_status = localStorage.getItem('status_key');
    let stored_release_img = localStorage.getItem('status_key');
    
    document.getElementById('RELEASE_TIME').textContent = stored_release_time;
    document.getElementById('RELEASE_ALTITUDE').textContent = stored_release_alt;
    document.getElementById('PADA_STATUS').textContent = stored_release_status;
    //document.getElementById('PADA_STATUS_IMAGE').src = stored_release_img;
    }



function updateChartData() {
    route_used = localStorage.getItem('route_name')
    console.log("THIS IS THE ROUTE BEING USED:",route_used)
    
    
    $.get(route_used, function (data) {         // Data comes in from the python program here
        const altitude_value = data.altitude;
        const airspeed_value = data.airspeed;
        const latitude_value = data.lat;
        const longitude_value = data.lon;

        $('#LIVE_ALTITUDE').text(altitude_value+" ft.");
        $('#AIRSPEED_DISPLAY').text(airspeed_value+" ft./s");
        $('#LATITUDE_DISPLAY').text(latitude_value+" °N");
        $('#LONGITUDE_DISPLAY').text(longitude_value+" °E");


        load_chart_data.shift();
        load_chart_data.push(altitude_value);
        localStorage.setItem('datapoints',load_chart_data)

        addRandomCoordinates(latitude_value,longitude_value)


        const options = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
        const formatter = new Intl.DateTimeFormat('en-US', options);
        const now = new Date();
        let formattedTime;

        if (now.getHours() === 0) {
            const adjustedHours = '00';
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const seconds = now.getSeconds().toString().padStart(2, '0');
            formattedTime = `${adjustedHours}:${minutes}:${seconds}`;
        }
        else {
            formattedTime = formatter.format(now);
        }

        $('#LIVE_TIME').text(formattedTime);
        // console.log(deploy_update_check)

        deploy_update_check = localStorage.getItem('deploy_update')
        //console.log("checking deploy_update_check:  " + deploy_update_check)

        if (deploy_update_check=='true'){

            stored_release_time = formattedTime;
            stored_release_alt = `${altitude_value} ft.`;
            stored_release_status = 'DEPLOYED';

            localStorage.setItem('time_key', stored_release_time);
            localStorage.setItem('alt_key', stored_release_alt);
            localStorage.setItem('status_key', stored_release_status);

            localStorage.setItem('deploy_update',false); 

            updateReleaseData();
        }
        

        myChart.data.datasets[0].data.push({
            x: Date.now(),
            y: altitude_value
        });
        myChart.update();
    });
}

function addflight_coordinates(GPS_Latitude,GPS_Longitude) {
    lineCoordinates =[];
    //var flight_coordinate = generateflight_coordinate();
    var flight_coordinate = [GPS_Latitude,GPS_Longitude];
    lineCoordinates.push(flight_coordinate);
    //console.log(typeof lineCoordinates)
    localStorage.setItem('FlightPath',lineCoordinates)

    

    // Update the polyline with the new coordinates
    polyline.setLatLngs(lineCoordinates);

    // Update the marker position
    marker.setLatLng(flight_coordinate);
    }

function CheckFlightPath(){
    // flight_path=localStorage.getItem('FlightPath');
    // console.log(flight_path)
    // flight_path_coordinates = flight_path.split(',');

    // // Convert the array of values into the desired format
    // const lineCoordinates = [];
    // for (let i = 0; i < flight_path_coordinates.length; i += 2) {
    //     const coord_pair = [parseInt(flight_path_coordinates[i]), parseInt(flight_path_coordinates[i + 1])];
    //     lineCoordinates.push(coord_pair);
    // }

    // return(lineCoordinates)
        // once restructured, update poly.
}


function getFlightData(csvDataUrl) {
    coordinates =[[11.650227,76.167492],[11.650227,76.167492],[11.650727,76.166992],[11.650227,76.166992],[11.650727,76.166492],[11.649727,76.167492],[11.650727,76.166992],[11.650227,76.167492],[11.650727,76.166492]];

    // const response = await fetch(csvDataUrl);
    // const data = await response.text();


    // const table = data.split('\n').slice(1);
    // table.forEach(row => {
    //     const columns = row.split(',');

    //     const latitude = parseFloat(columns[3]);
    //     const longitude = parseFloat(columns[4]);


    //     if (!isNaN(latitude) && !isNaN(longitude)) {
    //         coordinates.push([latitude, longitude]);
    //     }

    // });

    //console.log(coordinates);

    return {coordinates};
};



