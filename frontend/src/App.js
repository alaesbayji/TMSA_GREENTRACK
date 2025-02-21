// App.js  
import React from 'react';  
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  
import Login from './pages/Login/Login'; // Adjust the import path as necessary  
import Home from './pages/Home/home';
import Add_entreprise1 from './pages/Entreprises/Add_entreprise1';

const App = () => {  
  return (  
    <Router>  
      <Routes>  
        <Route path="/" element={<Login />} />  
        <Route path="/map" element={<Add_entreprise1 />} />  
        <Route path="/home" element={<Home />} />  
      </Routes>  
    </Router>  
  );  
};  

export default App;