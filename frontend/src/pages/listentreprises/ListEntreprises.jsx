import './ListEntreprises.scss'
import Sidebar from '../../components/Sidebar/Sidebar'
import Navbar from '../../components/Navbar/Navbar'
import Datatable_users from '../../components/Datatable_users/Datatable_users'
import Datatable_entreprise from '../../components/Datatable_entreprises/Datatable_entreprises'

const ListEntreprises = () => {
  return (
    <div className='list'>
      <Sidebar></Sidebar>
      <div className="listContainer">
        <Navbar></Navbar>
        <Datatable_entreprise></Datatable_entreprise>
      </div>
    </div>
  )
}

export default ListEntreprises
