// Home.js  
import React from 'react';  
import Sidebar from '../../components/Sidebar/Sidebar';  
import Navbar from '../../components/Navbar/Navbar';  
import './Home.css'; // Ajoutez des styles si nécessaire  

const Home = () => {  
  return (  
    <div className="home-container">  
          <Sidebar />
      <Navbar /> {/* Ajout de la Navbar */}  
 {/* Ajout de la Sidebar */}  
      <div className="content-section">  
        <h1>Welcome to the Home Page</h1>  
        {/* Vous pouvez ajouter plus de contenu ici */}  
      </div>  
    </div>  
  );  
}  

export default Home;