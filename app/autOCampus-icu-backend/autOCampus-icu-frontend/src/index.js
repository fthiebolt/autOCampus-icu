import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
//import CARICON from './App';
import {useMemo} from 'react'
import { MapContainer, Marker, Popup,TileLayer, LayersControl,
   LayerGroup} from 'react-leaflet';
import { Icon } from 'leaflet';
// import batiments from './App'
import reportWebVitals from './reportWebVitals';

const ICON = new Icon({
  iconUrl:"/static/css/caricon.png",
  iconSize:[30, 37]
});

// Classes used by Leaflet to position controls
const POSITION_CLASSES = {
  bottomleft: 'leaflet-bottom leaflet-left',
  bottomright: 'leaflet-bottom leaflet-right',
  topleft: 'leaflet-top leaflet-left',
  topright: 'leaflet-top leaflet-right',
}

//Var of the connected objects
var devices = {};
var barrieres = {};
var buildings = {};

//Interval for an information to expire
const interval = 5 * 60 * 1000; // 5 min

//Create Connected Devices Table
function TableBounds() {

  // Keep track of bounds in state to trigger renders

  return (<table style={{maxHeight: window.innerHeight * 0.5}} id="DevicesTable" className="w3-table w3-hovorable w3-center-align">
              <tr>
                <th>Device ID</th>
                <th>Last Updated</th>
              </tr>    
            </table> );
}

//Create Connected Devices Table Control Layer
function TableControl({position}) {
  // Memoize the minimap so it's not affected by position changes
  const minimap = useMemo(
    () => (
        <TableBounds/>
    ),
    [],
  )

  const positionClass =
    (position && POSITION_CLASSES[position]) || POSITION_CLASSES.topright
  return (
    <div className={positionClass}>
      <div id="scroll" className="leaflet-control leaflet-bar">{minimap}</div>
    </div>
  )
}

//Update Map when new information arrived
function Iterate(){
    var devicesTab = [];
    var barrieresTab = [];
    for (var i in devices) //update cars and robots location
        devicesTab.push({"id": i, "lat": devices[i].lat, "lon": devices[i].lon});
    for (i in barrieres) //updat Barres states
        barrieresTab.push({"id": i, "lat": devices[i].lat, "lon": devices[i].lon
                                    , "State": devices[i].State});
    
    //Create Cars and robots Markers                                
    var Rb_Va = devicesTab.map((device) =>(
      <Marker icon={ICON} id={device['id']} position={[device['lat'], device['lon']]}>
            <Popup>
              {device['id']}
            </Popup>
      </Marker>
    ));

    //Create Barres Markers
    
    var Barres = barrieresTab.map((Barre) =>(
      <Marker id={Barre['id']} position={[Barre['lat'], Barre['lon']]}>
            <Popup>
              {Barres['id']}
            </Popup>
      </Marker>
    ));
    ReactDOM.render(
      <React.StrictMode>
        <MapContainer id='map' style={{ height: window.innerHeight, width: "100%" }} center={[43.5613, 1.4631]} zoom={17}>
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <LayersControl position="topleft">
                  <LayersControl.Overlay checked name="Batiments de campus">
                    <LayerGroup>
                      <App />
                    </LayerGroup>
                  </LayersControl.Overlay>
                  <LayersControl.Overlay name="Robots - Voitures Autonomes">
                    <LayerGroup>
                      {Rb_Va}
                    </LayerGroup>
                  </LayersControl.Overlay>
                  <LayersControl.Overlay name="Barres">
                    <LayerGroup>
                      {Barres}
                    </LayerGroup>
                  </LayersControl.Overlay>  
              </LayersControl>
              <TableControl />
        </MapContainer>
      </React.StrictMode>,
      document.getElementById('root')
    );
}

//Update Connected Devices Table
function updateTable(){
  var refTable = document.getElementById('DevicesTable');

  //Delete Table content
  while(refTable.rows.length > 1)
      refTable.deleteRow(1);
  
  //Update Table content
  for(var indice in devices){
    //Create Row Object
    var row = refTable.insertRow(1);

    //Create Cells Objects
    var idCell = row.insertCell(0); //id
    // var locationCell = row.insertCell(1); //Location ??
    var lastUpdatedCell = row.insertCell(1); //last Updated

    //Add Infrmation
    idCell.innerHTML = indice;
    lastUpdatedCell.innerHTML = new Date(devices[indice]['TimeStamp']);
  }
}

//Update Devices Object
function updateDevices(jsonObj, date){
  //Get DATA
  var data = {}
  for (var j=0; j < jsonObj['value'].length; j++)
    data[jsonObj['value_units'][j]] = jsonObj['value'][j];
  data['id'] = jsonObj['unitID']
  console.log(data)
  if(data.hasOwnProperty('lat') && data.hasOwnProperty('lon'))
     devices[data.id] = {"lat" :data.lat, "lon" : data.lon, "TimeStamp": date};
  var temp = devices;
  //Update Devices Location
  for(var i in devices)
    if(devices[i].TimeStamp.valueOf() <= date - interval)
        delete temp[i];
  devices = temp;
  console.log("Devices Infos");
}  
//Update Barres Object
function updateBarres(jsonObj, date){
  //Get DATA
  var data = {}
  for (var j=0; j < jsonObj['value'].length; j++)
    data[jsonObj['value_units'][j]] = jsonObj['value'][j];
  data['id'] = jsonObj['unitID']
  console.log(data)
  barrieres[data.id] = {"lat" :data.lat, "lon" : data.Log, "TimeStamp": date};
  var temp = barrieres;
  //Update Devices Location
  for(var i in devices)
    if(barrieres[i].TimeStamp.valueOf() <= date - interval)
        delete temp[i];
  barrieres = temp;
  console.log(" Barres Infos");
}  

//Update Building Object
function updateBuildings(jsonObj, date){
  //Get DATA
  var data = {}
  for (var j=0; j < jsonObj['value'].length; j++)
    data[jsonObj['value_units'][j]] = jsonObj['value'][j];
  data['id'] = jsonObj['unitID']
  console.log(data)
  buildings[data.id] = {"lat" :data.lat, "lon" : data.Log, "TimeStamp": date};
  var temp = buildings;
  //Update Buildings Location
  for(var i in devices)
    if(buildings[i].TimeStamp.valueOf() <= date - interval)
        delete temp[i];
  buildings = temp;
  console.log(" Buildings Infos");
}  

//initialize the map
Iterate();

//websocket Connection
const socket = new WebSocket('wss://defi-midoc.univ-tlse3.fr');
 
socket.addEventListener('open', function (event) {
  socket.send('Connection Established');
});

socket.addEventListener('message', function (event) {
    console.log(JSON.parse(event.data))
    var jsonObj = JSON.parse(event.data);
    var date = Date.now()
    //new Informations
    if(jsonObj.Type === "VARB") //Cars and Robots
        updateDevices(jsonObj, date);
    else if(jsonObj.Type === "Build") //Buildings
        updateBuildings(jsonObj, date);
    else if(jsonObj.Type === "BARRES") //Barres
        updateBarres(jsonObj, date);
    else //Default
        updateDevices(jsonObj);
    
    Iterate();

    
    //Update Table
    updateTable();
});


reportWebVitals();
