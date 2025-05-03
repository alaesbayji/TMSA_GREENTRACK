import './ListEntreprises.scss'
import Sidebar from '../../components/Sidebar/Sidebar'
import Navbar from '../../components/Navbar/Navbar'
import Datatable_entreprise from '../../components/Datatable_entreprises/Datatable_entreprises'
import Widget from '../../components/Stat_entreprise/Widget'

const ListEntreprises = () => {
  return (
    <div className='list'>
      <Sidebar></Sidebar>
      <div className="homeContainer">
        <Navbar></Navbar>
        <div className="widgets"> 
        <Widget type="entreprises" />
        <Widget type="emplois" />
        <Widget type="investissements" />
        <Widget type="superficie" />
        </div>
        <div className="listContainer">
        <Datatable_entreprise></Datatable_entreprise>

        </div>
       
      </div>
    </div>
  )
}

export default ListEntreprises
