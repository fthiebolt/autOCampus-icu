import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import ICON from './App';
import { MapContainer, Marker, Popup,TileLayer } from 'react-leaflet';
// import batiments from './App'
import reportWebVitals from './reportWebVitals';
// import { Marker, Popup } from 'react-leaflet';
// import {Marker, Popup } from 'react-leaflet'
var i = 0;
const iterations = [];
function Iterate(){
  if(i < iterations.length){
    ReactDOM.render(
      <React.StrictMode>
        <MapContainer id='map' icon={ICON} style={{ height: 800, width: "100%" }} center={[43.5613, 1.4631]} zoom={16}>
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
              <App />
              <Marker key={iterations[i][0]} position={[iterations[i][2], iterations[i][1]]}>
                    <Popup>
                      Car with id 1
                    </Popup>
              </Marker>
        </MapContainer>
      </React.StrictMode>,
      document.getElementById('root')
    );
    console.log(i);
    i++;
  }
  
}


ReactDOM.render(
  <React.StrictMode>
    <MapContainer id='map' icon={ICON} style={{ height: 800, width: "100%" }} center={[43.5613, 1.4631]} zoom={16}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <App />
      <Marker key={iterations[i][0]} position={[iterations[i][2], iterations[i][1]]}>
              <Popup>
                Car with id 1
              </Popup>
        </Marker>
    </MapContainer>
  </React.StrictMode>,document.getElementById('root')
);
var cord = '{"id":"R1", "Lat":43.5613, "Lag":1.4631}';
const obj = JSON.parse(cord);
console.log(obj.id);

// Test la cnnexion websocket
const socket = new WebSocket('ws://localhost:8000');
 
socket.addEventListener('open', function (event) {
 
    socket.send('Connection Established');
 
});
 
 
 
socket.addEventListener('message', function (event) {
 
    console.log(event.data);
 
});

// client.send(JSON.stringify(obj));
// client.send(JSON.stringify(obj));



//setInterval(Iterate, 2000);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
