import './App.css';
import { useState } from "react";
import Plot from 'react-plotly.js';
import { GoogleMap, LoadScript, Polyline, Marker } from '@react-google-maps/api';

function App() {
  const [output, setOutput] = useState({
    x: "",
    y_e: "",
    y_w: "",
    targ: "",
    pred_e: "",
    pred_w: ""
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

  const mapContainerStyle = {
    height: "400px",
    width: "800px"
  };
  
  const center = {
    lat: 42.4661436440556, 
    lng: -71.39302047738968
  };
  
  const onLoad = polyline => {
    console.log('polyline: ', polyline)
  };
  
  const path_e = [
    {lat: 42.46668835230436, lng: -71.39541045877085},
    //{lat: 42.465569824119775, lng: -71.39069250025713}
    {lat: 42.46558016279177, lng: -71.39068690943682}
  ];

  const path_w = [
    //{lat: 42.46561140545062, lng: -71.39068686350859},
    {lat: 42.46561963118116, lng: -71.39067016089516},
    {lat: 42.46673824901031, lng: -71.39539918526981}
  ];

  const options_red = {
    strokeColor: 'Red',
    strokeOpacity: 0.8,
    strokeWeight: 4
  };

  const options_orange = {
    strokeColor: '#FF5733',
    strokeOpacity: 0.8,
    strokeWeight: 4
  };

  const options_green = {
    strokeColor: 'Green',
    strokeOpacity: 0.8,
    strokeWeight: 4
  };
  
  /* const options = {
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
  }; */
  
  return (
    <div
        style={{
        padding: "1em 0.7em",
        width: "100%",
        }}
    >
        <div>
            <h1 className="title">Hourly Traffic Volume Forecasts</h1>
        </div>
        <div>
            <h2>Instructions</h2>
            <ul>
            <li>This app will forecast the east-going and west-going hourly traffic volume at Elm Street, Concord, Massachusetts.</li>
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
          <div>
              <h2>Results</h2>
              The predicted traffic volume on {output.targ} is 
              <ul>
                <li>East: {Math.round(output.pred_e)}</li>
                <li>West: {Math.round(output.pred_w)}</li>
              </ul>
              
              <br /><br />
              <Plot
                  data={[
                      {
                        x: output.x,
                        y: output.y_e,
                        type: 'scatter',
                        name: "East"
                      }, 
                      {
                        x: output.x,
                        y: output.y_w,
                        type: 'scatter',
                        marker: {color: 'orange'},
                        name: "West"
                      }, 
                      {
                        x: [output.targ],
                        y: [output.pred_e],
                        marker: {color: 'indigo', symbol: 'circle', size: 10},
                        name: "East - Target"
                      },
                      {
                        x: [output.targ],
                        y: [output.pred_w],
                        marker: {color: 'brown', symbol: 'circle', size: 10},
                        name: "West - Target"
                      }
                  ]}
                  layout={ {
                      width: 1200, 
                      height: 600, 
                      title: "Traffic Volume Predictions for Week of " + output.targ
                  } }
              />
          </div>
          <br />
          <div>
              <LoadScript googleMapsApiKey="AIzaSyDFOYWlEgtpryBkhQnVmj9BA_2MDvZnUAU">
              <GoogleMap
                  mapContainerStyle={mapContainerStyle}
                  zoom={17.5}
                  center={center}
              >
                  <Marker position={{lat: 42.466140759994005, lng: -71.3928541589189}}
                  label={"West: " + Math.round(output.pred_w)}
                  key="west"
                  />

                  {/* Change polyline colour depending on traffic volume */}

                  {output.pred_e < 700 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_e}
                  options={options_green}
                  />}

                  {output.pred_e >= 700 && output.pred_e < 1400 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_e}
                  options={options_orange}
                  />}

                  {output.pred_e >= 1400 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_e}
                  options={options_red}
                  />}

                  {output.pred_w < 700 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_w}
                  options={options_green}
                  />}

                  {output.pred_w >= 700 && output.pred_w < 1400 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_w}
                  options={options_orange}
                  />}

                  {output.pred_w >= 1400 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_w}
                  options={options_red}
                  />}

              </GoogleMap>
          </LoadScript>
          </div>
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