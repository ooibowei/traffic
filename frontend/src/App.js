import './App.css';
import { useState } from "react";
import Plot from 'react-plotly.js';
import { GoogleMap, LoadScript, Polyline, Marker } from '@react-google-maps/api';

function App() {
  const [output, setOutput] = useState({
    x: "",
    y: "",
    targ: "",
    pred: ""
  });

  const [dt, setDt] = useState(new Date());

  const [sub, setSub] = useState({isSubmitted: false})

  const onClick = e => {
    e.preventDefault();
    setSub({isSubmitted: true})
    fetch("/predict",
    {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({dt_input: dt})
      }
    )
    .then(resp => resp.json())
    .then(resp => setOutput(resp))
  }

/*   const center = {
    lat: 42.466437,
    lng: -71.394159
  };

  const containerStyle = {
    width: '400px',
    height: '400px'
  };

  const onLoad = polyline => {
    console.log('polyline: ', polyline)
  };
  
  const path = [
    {lat: 42.466437, lng: -71.394159},
    {lat: 49.486437, lng: -79.374159}
  ];
  
  const options = {
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2
  }; */

  const mapContainerStyle = {
    height: "400px",
    width: "800px"
  };
  
  const center = {
    lat: 0,
    lng: -180
  };
  
  const onLoad = polyline => {
    console.log('polyline: ', polyline)
  };
  
  const path = [
    {lat: 37.772, lng: -122.214},
    {lat: 21.291, lng: -157.821},
    {lat: -18.142, lng: 178.431},
    {lat: -27.467, lng: 153.027}
  ];
  
  const options = {
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
    clickable: false,
    draggable: false,
    editable: false,
    visible: true,
    radius: 30000,
    paths: [
      {lat: 37.772, lng: -122.214},
      {lat: 21.291, lng: -157.821},
      {lat: -18.142, lng: 178.431},
      {lat: -27.467, lng: 153.027}
    ],
    zIndex: 1
  };
  

  return (
    <div
        style={{
        padding: "1em 0.7em",
        width: "100%",
        }}
    >
        <LoadScript googleMapsApiKey="AIzaSyDFOYWlEgtpryBkhQnVmj9BA_2MDvZnUAU">
            <GoogleMap
                id="marker-example"
                mapContainerStyle={mapContainerStyle}
                zoom={2}
                center={center}
            >
                <Marker position={center} />
                <Polyline
                onLoad={onLoad}
                path={path}
                options={options}
                />
            </GoogleMap>
        </LoadScript>
        <div>
            <h1 className="title">Hourly Traffic Volume App</h1>
{/*             <LoadScript googleMapsApiKey="AIzaSyDFOYWlEgtpryBkhQnVmj9BA_2MDvZnUAU">
            <GoogleMap
                mapContainerStyle={containerStyle}
                center={center}
                zoom={17}
            >
                <Polyline>
                    onLoad={onLoad}
                    path={path}
                    options={options}
                </Polyline>
            </GoogleMap>
            </LoadScript> */}
        </div>
        <div>
            <h2>Instructions</h2>
            <ul>
            <li>This app will forecast the hourly traffic volume at XXX, for both the east and west directions.</li>
            <li>Enter the target date and time in the box below.</li>
            <li>The target date must be from 2022 and beyond. The tick/cross to the right will indicate if it is an accepted input.</li>
            </ul>
            <h2>Input</h2>
            <form>
            <input type="datetime-local" onChange={(e) => setDt(e.target.value)} onClick={(e) => e.preventDefault()} step="3600" min="2022-01-01T00:00" required/><span className="validity" />
            <br />
            <input type="submit" value="Submit" onClick={onClick} />
            </form>
            <br />
        </div>
        {sub.isSubmitted &&
        <div>
            <h2>Results</h2>
            The predicted traffic volume on {output.targ} is {Math.round(output.pred)}.
            <br /><br />
            <Plot
                data={[
                    {
                    x: output.x,
                    y: output.y,
                    type: 'scatter',
                    name: "Traffic volume"
                    }
                    , {
                        x: [output.targ],
                        y: [output.pred],
                        marker: {color: 'red', symbol: 'star', size: 10},
                        name: "Target date"
                    }
                ]}
                layout={ {
                    width: 1200, 
                    height: 600, 
                    title: "Traffic Volume Predictions for Week of " + output.targ + " (East)"
                } }
            />
        </div>
        }
    </div>
  )

}

export default App;

//<input onChange={(e) => setInputval({inputval1: e.target.value})} />
//<input onChange={(e) => setInputval({year: e.target.value})} />
//<p>Your name is: {output} and {inputval.year} and </p>
//<p>Your name is: {output.output_x}  </p>