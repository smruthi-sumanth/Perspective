import React from 'react';
import './App.css'; // Assuming you have some basic CSS styling
import FormComponent from './FormComponent';
import Background from './Components/Background';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>PERSPECTIVE</h1>
        <FormComponent/>
        <Background/>
      </header>
    </div>
  );
}

export default App;
