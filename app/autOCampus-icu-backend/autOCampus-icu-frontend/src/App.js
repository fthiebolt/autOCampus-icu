import React from 'react';
import './App.css';
import {Marker, Popup } from 'react-leaflet'
import { Icon } from 'leaflet';

const batiments = [
  ["U6", 43.563, 1.4683],
  ["U4", 43.5628, 1.4692],
  ["U3", 43.5621, 1.4699],
  ["U2", 43.5613, 1.4707],
  ["U1", 43.5604, 1.4702]
];
const ICON = new Icon({
  iconUrl:"/static/css/marker.png",
  iconSize:[30, 37]
});

function App() {  
    var map = batiments.map((batiment) =>(
        <Marker icon={ICON} id="Test" key={batiment[0]} position={[batiment[1], batiment[2]]}>
              <Popup>
                <i class="fa fa-building"> :  &nbsp;{batiment[0]} </i> <br/>
                <i class='fa fa-thermometer'> : &nbsp;13°</i><br/>
                <i class="fa fa-tint">  :  &nbsp;51%</i>
              </Popup>
        </Marker>
      ));
    return map;
}

export default App;
