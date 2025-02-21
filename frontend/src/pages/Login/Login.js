// LoginPage.js  
import React, { useState } from 'react';  
import axios from 'axios';  
import { useNavigate } from 'react-router-dom';  
import './Login.css'; // Import the CSS file  
import image from '../../images/2.png';  
import shape from '../../images/shape.png';  
const Login = () => {  
  const [email, setEmail] = useState('');  
  const [password, setPassword] = useState('');  
  const [error, setError] = useState('');  
  const navigate = useNavigate(); // Hook for navigation  

  const handleSubmit = async (e) => {  
    e.preventDefault();  
    setError('');  

    try {  
      const response = await axios.post('http://localhost:8000/api/login/', {  
        email,  
        password,  
      });  

      // Handle successful login (e.g., save token, redirect)  
      console.log(response.data);  
      // Redirect to MapComponent  
      navigate('/map'); // Adjust the path according to your routes  
    } catch (err) {  
      setError('Invalid email or password.');  
    }  
  };  

  return (  
    <div className="login-container">  
      <div className="logo-section">  
        <img src={image} className='logo'></img>  
        <button className="read-more-button">Read More</button>  
        <img src={shape} className='logo1'></img>  
      </div>  

      <div className="login-form">  
        <h2>Hello Again!</h2>  
        <p>Welcome Back</p>  
        {error && <p className="error">{error}</p>}  
        <form onSubmit={handleSubmit}>  
    <input  
        type="email"  
        placeholder="Email Address"  
        value={email}  
        onChange={(e) => setEmail(e.target.value)}  
        required  
        className="input"  
    />  
    <input  
        type="password"  
        placeholder="Password"  
        value={password}  
        onChange={(e) => setPassword(e.target.value)}  
        required  
        className="input"  
    />  
    <button type="submit" className="login-button">Login</button>  
</form>  
<p className="forgot-password">Forgot Password?</p> 
      </div>  
    </div>  
  );  
};  

export default Login;