import './List.scss'
import Sidebar from '../../components/Sidebar/Sidebar'
import Navbar from '../../components/Navbar/Navbar'
import Datatable_users from '../../components/Datatable_users/Datatable_users'

const List = () => {
  return (
    <div className='list'>
      <Sidebar></Sidebar>
      <div className="listContainer">
        <Navbar></Navbar>
        <Datatable_users></Datatable_users>
      </div>
    </div>
  )
}

export default List
