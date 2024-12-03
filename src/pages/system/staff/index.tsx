// ** Import Next
import { NextPage } from 'next'

// ** Config
import { PERMISSIONS } from 'src/configs/permission'

// ** Page
import StaffListPage from 'src/views/pages/system/staff/StaffList'

// ** views

type TProps = {}

const Index: NextPage<TProps> = ({params}: any) => {
  return <StaffListPage/>
}

Index.permission = [PERMISSIONS.SYSTEM.STAFF.VIEW]
export default Index

