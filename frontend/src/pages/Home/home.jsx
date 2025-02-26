// Home.js  
import React from 'react';  
import Sidebar from '../../components/Sidebar/Sidebar';  
import Navbar from '../../components/Navbar/Navbar';  
import './home.scss'; // Ajoutez des styles si nécessaire  

const Home = () => {  
  return (  
    <div className='home'>
    <Sidebar />
    <div className='homeContainer'>
      <Navbar></Navbar>
       
          </div>
   </div>
  );  
}  

export default Home;