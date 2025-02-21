import './Navbar.css';  
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';  
import DarkModeIcon from '@mui/icons-material/DarkMode';  
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';  
import LanguageIcon from '@mui/icons-material/Language';  
import alae from '../../images/alae.jpg';  

const Navbar = () => {  
  return (  
    <div className='navbar'>  
      <div className='wrapper'>  
        <div className='search'>  
          <input type='text' placeholder='Search ...' />  
          <SearchOutlinedIcon />  
        </div>  
        <div className='items'>  
          <div className='item'>   
            <LanguageIcon className='icon' />  
            Français  
          </div>  
          <div className='item'>   
            <DarkModeIcon className='icon' />  
          </div>  
          <div className='item'>  
            <FormatListBulletedIcon className='icon' />  
          </div>  
          <div className='item'>  
            <img src={alae} alt='User Avatar' className='avatar' />  
          </div>  
        </div>  
      </div>  
    </div>  
  )  
}  

export default Navbar;