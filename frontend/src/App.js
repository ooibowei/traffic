import './App.css';
import { useState } from "react";
import Plot from 'react-plotly.js';
import { GoogleMap, LoadScript, Polyline, InfoWindow } from '@react-google-maps/api';

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
    fetch("https://traffic-0rnt.onrender.com/predict",
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
    height: "600px",
    width: "900px"
  };
  
  const center = {
    lat: 42.4661436440556, 
    lng: -71.39302047738968
  };
  
  const onLoad = polyline => {
    console.log('polyline: ', polyline)
  };
  
  const [infoE, setInfoE] = useState(false);

  const [infoW, setInfoW] = useState(false);

  const path_e = [
    {lat: 42.46668835230436, lng: -71.39541045877085},
    {lat: 42.46558016279177, lng: -71.39068690943682}
  ];

  const path_w = [
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
              The forecasted traffic volume on {output.targ} can be displayed in the map below by selecting the appropriate traffic lane. 
              The traffic lanes are coloured green/orange/red depending on the forecasted traffic volume. The forecasts for the week is shown in the plot further below.
              <br /><br />
              <LoadScript googleMapsApiKey="Redacted">
              <GoogleMap
                  mapContainerStyle={mapContainerStyle}
                  zoom={17.5}
                  center={center}
              >                

                  {/* Change polyline colour depending on traffic volume */}

                  {output.pred_e < 700 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_e}
                  options={options_green}
                  onClick={() => {setInfoE(true)}}
                  />}
                  
                  {output.pred_e >= 700 && output.pred_e < 1400 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_e}
                  options={options_orange}
                  onClick={() => {setInfoE(true)}}
                  />}

                  {output.pred_e >= 1400 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_e}
                  options={options_red}
                  onClick={() => {setInfoE(true)}}
                  />}

                  {output.pred_w < 700 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_w}
                  options={options_green}
                  onClick={() => {setInfoW(true)}}
                  />}

                  {output.pred_w >= 700 && output.pred_w < 1400 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_w}
                  options={options_orange}
                  onClick={() => {setInfoW(true)}}
                  />}

                  {output.pred_w >= 1400 && 
                  <Polyline
                  onLoad={onLoad}
                  path={path_w}
                  options={options_red}
                  onClick={() => {setInfoW(true)}}
                  />}

                  {infoE && (
                    <InfoWindow
                        onCloseClick={() => {
                          setInfoE(false);
                        }}
                        position={{lat: 42.465950833062536, lng: -71.39222675607662}}
                    >
                      <div style={{ color: 'black' }}>
                        <u>East</u><br />
                        Forecasted hourly traffic volume: {Math.round(output.pred_e)}
                      </div>
                    </InfoWindow>
                  )}

                  {infoW && (
                    <InfoWindow
                        onCloseClick={() => {
                          setInfoW(false);
                        }}
                        position={{lat: 42.4663852375204, lng: -71.39392857210585}}
                    >
                      <div style={{ color: 'black' }}>
                        <u>West</u><br />
                        Forecasted hourly traffic volume: {Math.round(output.pred_w)}
                      </div>
                    </InfoWindow>
                  )}

              </GoogleMap>
              </LoadScript>
              
          </div>
          <br />
          <div>
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
                      width: 900, 
                      height: 600, 
                      title: "Traffic Volume Forecasts for Week of " + output.targ
                  } }
              />
          </div>
        </div>
        }
    </div>
  )

}

export default App;
