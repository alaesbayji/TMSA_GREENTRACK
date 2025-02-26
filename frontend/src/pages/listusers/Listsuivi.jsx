import './List.scss'
import Sidebar from '../../components/Sidebar/Sidebar'
import Navbar from '../../components/Navbar/Navbar'
import Datatable_suivi from '../../components/Datatable_users/Datatable_suivi'

const Listsuivi = () => {
  return (
    <div className='list'>
      <Sidebar></Sidebar>
      <div className="listContainer">
        <Navbar></Navbar>
        <Datatable_suivi></Datatable_suivi>
      </div>
    </div>
  )
}

export default Listsuivi
