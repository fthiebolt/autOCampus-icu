import React from 'react';
import './App.css';
import {Marker, Popup } from 'react-leaflet'
import { icon } from "leaflet"

const batiments = [
  ["U6", 43.563, 1.4683],
  ["U4", 43.5628, 1.4692],
  ["U3", 43.5621, 1.4699],
  ["U2", 43.5613, 1.4707],
  ["U1", 43.5604, 1.4702]
];
const ICON = icon({
    iconUrl: "/marker.png",
    iconSize: [32, 32],
  });
function App() {
  

      
    var map = batiments.map((batiment) =>(
        <Marker id={batiment[0]} position={[batiment[1], batiment[2]]}>
              <Popup>
                {batiment[0]}
              </Popup>
        </Marker>
      ));
    return map;
}

export default App;
