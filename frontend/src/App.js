import './App.css';
import { useState } from "react";
import Plot from 'react-plotly.js';

function App() {
  /*const [inputval, setInputval] = useState({
    inputval1: "",
    year: ""
  });*/
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
        //body: JSON.stringify({name_input: inputval.inputval1})
        body: JSON.stringify({dt_input: dt})
      }
    )
    .then(resp => resp.json())
    .then(resp => setOutput(resp))
    //.then(resp => setOutput(resp.output))
  }

  return (
    <div
        style={{
        padding: "1em 0.7em",
        width: "100%",
        }}
    >
        <div>
            <h1 className="title">Hourly Traffic Volume App</h1>
        </div>
        <div>
            <h2>Instructions</h2>
            <ul>
            <li>This app will predict the hourly traffic volume at XXX, for both the east and west directions.</li>
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