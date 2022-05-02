import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import ICON from './App';
import { MapContainer, Marker, Popup,TileLayer, LayersControl, LayerGroup } from 'react-leaflet';
// import batiments from './App'
import reportWebVitals from './reportWebVitals';
// import { Marker, Popup } from 'react-leaflet';
// import {Marker, Popup } from 'react-leaflet';
var devices = {}; 
const interval = 5 * 60 * 1000;
function Iterate(jsonObject){
    var devicesTab = [];
    for (var i in devices)
        devicesTab.push({"id": i, "Lat": devices[i].Lat, "Lag": devices[i].Lag});
    var Rb_Va = devicesTab.map((device) =>(
      <Marker id={device['id']} position={[device['Lat'], device['Lag']]}>
            <Popup>
              {device['id']}
            </Popup>
      </Marker>
    ));
    ReactDOM.render(
      <React.StrictMode>
        <MapContainer id='map' style={{ height: 800, width: "100%" }} center={[43.5613, 1.4631]} zoom={17}>
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <LayersControl position="topright">
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

                  </LayersControl.Overlay>  
              </LayersControl>
        </MapContainer>
      </React.StrictMode>,
      document.getElementById('root')
    );
}


ReactDOM.render(
  <React.StrictMode>
    <MapContainer id='map' icon={ICON} style={{ height: 800, width: "100%" }} center={[43.5613, 1.4631]} zoom={16}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <App />
    </MapContainer>
  </React.StrictMode>,document.getElementById('root')
);
var cord = '{"id":"R1", "Lat":43.5613, "Lag":1.4631}';
const obj = JSON.parse(cord);
console.log(obj);

// Test la connexion websocket
const socket = new WebSocket('ws://localhost:8000');
 
socket.addEventListener('open', function (event) {
  socket.send('Connection Established');
});

socket.addEventListener('message', function (event) {
    var jsonObj = JSON.parse(event.data);
    var date = Date.now()
    devices[jsonObj.id] = {"Lat" :jsonObj.Lat, "Lag" : jsonObj.Lag, "TimeStamp": date};
    var temp = devices;
    for(var i in devices)
      if(devices[i].TimeStamp.valueOf() <= date - interval)
          delete temp[i];
    devices = temp;
    Iterate(JSON.parse(event.data));
});


reportWebVitals();