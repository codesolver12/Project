let popup = document.getElementById("ZONE_POPUP");

function setZone(){

    //Destructure Latitude values from local storage
    const Latitude_data = localStorage.getItem('zoneLatitude'); 
    Latitudes = Latitude_data.split(',')

    //Destructure Longitude values from local storage
    const Longitude_data = localStorage.getItem('zoneLongitude'); 
    Longitudes = Longitude_data.split(',')

    //Destructure Colour values from local storage
    const colour_data = localStorage.getItem('zonecolour'); 
    Colours = colour_data.split(',')

    //Destructure Status values from local storage 
    const status_data = localStorage.getItem('zonestatus'); 
    zone_status = status_data.split(',')
    // Check if Zone input and add marker
    if (zone_status[0] == 'true'){
        L.marker([Latitudes[0], Longitudes[0]]).addTo(map);
    }
    if (zone_status[1] == 'true'){
        L.marker([Latitudes[1], Longitudes[1]]).addTo(map);
    }
    if (zone_status[2] == 'true'){
        L.marker([Latitudes[2], Longitudes[2]]).addTo(map);
    }
    if (zone_status[3] == 'true'){
        L.marker([Latitudes[3], Longitudes[3]]).addTo(map);
    }

    // Get Element IDs to update values
    let zonecolour1 = document.getElementById("ZONE_COLOUR1");
    let zonecolour2 = document.getElementById("ZONE_COLOUR2");
    let zonecolour3 = document.getElementById("ZONE_COLOUR3");
    let zonecolour4 = document.getElementById("ZONE_COLOUR4");

    // Update Zone Colours
    zonecolour1.style.backgroundColor = "#" + Colours[0];
    zonecolour2.style.backgroundColor = "#" + Colours[1];
    zonecolour3.style.backgroundColor = "#" + Colours[2];
    zonecolour4.style.backgroundColor = "#" + Colours[3];

    //Update Zone Coordinates
    zonecoord1_text = Latitudes[0] + " N  ,  " + Longitudes[0] + " E"
    zonecoord2_text = Latitudes[1] + " N  ,  " + Longitudes[1] + " E"
    zonecoord3_text = Latitudes[2] + " N  ,  " + Longitudes[2] + " E"
    zonecoord4_text = Latitudes[3] + " N  ,  " + Longitudes[3] + " E"


    $('#ZONE_COORDINATE1').text(zonecoord1_text);
    $('#ZONE_COORDINATE2').text(zonecoord2_text);
    $('#ZONE_COORDINATE3').text(zonecoord3_text);
    $('#ZONE_COORDINATE4').text(zonecoord4_text);

}

function PopUp_Submit(){

    let popup = document.getElementById("ZONE_POPUP");

    // Receive Values from Zone Popup
    var lattitudeValue = document.getElementById("LATTITUDE").value;
    var longitudeValue = document.getElementById("LONGITUDE").value;
    var colourValue = document.getElementById("COLOUR_CODE").value;                         // Taking Values from Popup Input

    // Identify Zone number to update values
    zone_number = localStorage.getItem('ZONE_NUMBER');                                      // Checking which zone number for which data should be updated


    // Set Lattitude value to local storage
    const Latitude_data = localStorage.getItem('zoneLatitude'); 
    Latitudes = Latitude_data.split(',')                                 
    Latitudes[zone_number] = lattitudeValue;
    localStorage.setItem('zoneLatitude',Latitudes);

    // Set Longitude value to local storage
    const Longitude_data = localStorage.getItem('zoneLongitude'); 
    Longitudes = Longitude_data.split(',')                                 
    Longitudes[zone_number] = longitudeValue;
    localStorage.setItem('zoneLongitude',Longitudes);

    // Set Colour value to local storage
    const colour_data = localStorage.getItem('zonecolour'); 
    Colours = colour_data.split(',')                                 
    Colours[zone_number] = colourValue;
    localStorage.setItem('zonecolour',Colours);

    // Set Status value to local storage
    const status_data = localStorage.getItem('zonestatus');
    zonestatus = status_data.split(',')
    zonestatus[zone_number] = 'true';
    localStorage.setItem('zonestatus',zonestatus);

    // Hide and update Popup
    popup.style.visibility = "hidden";
    document.getElementById("COLOUR_INPUT").reset();
    document.getElementById("LONGITUDE_INPUT").reset();
    document.getElementById("LATTITUDE_INPUT").reset();

    setZone()

}

function PopUp_Close(){

    let popup = document.getElementById("ZONE_POPUP");

    popup.style.visibility = "hidden";
    document.getElementById("COLOUR_INPUT").reset();
    document.getElementById("LONGITUDE_INPUT").reset();
    document.getElementById("LATTITUDE_INPUT").reset();
}

function PopUp_Open(ZONE_NUMBER){

    let popup = document.getElementById("ZONE_POPUP");

    popup.style.visibility = "visible";
    localStorage.setItem('ZONE_NUMBER',ZONE_NUMBER) ;                                       //assigning zone number whose data has to be updated
}