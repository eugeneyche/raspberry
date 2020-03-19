import React from 'react';
import logo from './logo.svg';
import './App.css';
import {DEBUG_bindApi} from './stateApi';

DEBUG_bindApi();

interface State {
  version: number;
  data: {counter: number} | null;
}

class App extends React.Component<{}, State> {
  constructor(props: {}) {
    super(props);
    this.state = {
      version: 0,
      data: null,
    };
  }

  private handleClick = () => {
    const {version, data} = this.state;
    const counter = data ? data.counter : 0;
  };

  public componentDidMount() {
  }

  public render() {
    const {data} = this.state;
    const counter = data ? data.counter : 0;
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.tsx</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          <button onClick={this.handleClick}>{counter}</button>
        </header>
      </div>
    )
  }
}

export default App;
