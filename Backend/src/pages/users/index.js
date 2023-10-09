// ** MUI Imports
import Grid from '@mui/material/Grid'
import Link from '@mui/material/Link'
import Card from '@mui/material/Card'
import Typography from '@mui/material/Typography'
import CardHeader from '@mui/material/CardHeader'
import { useEffect } from 'react'
import { useRouter } from 'next/router'

// ** Demo Components Imports
import TableBasic from 'src/views/tables/TableBasic'
import TableDense from 'src/views/tables/TableDense'
import TableSpanning from 'src/views/tables/TableSpanning'
import TableCustomized from 'src/views/tables/TableCustomized'
import TableCollapsible from 'src/views/tables/TableCollapsible'
import TableStickyHeader from 'src/views/tables/TableStickyHeader'


// ** MUI Imports
import Paper from '@mui/material/Paper'
import Table from '@mui/material/Table'
import TableRow from '@mui/material/TableRow'
import TableHead from '@mui/material/TableHead'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import { useState } from 'react'
import { getRequest } from 'src/@core/utils/api'

const createData = (name, calories, fat, carbs, protein) => {
  return { name, calories, fat, carbs, protein }
}


const Users = () => {

  const router = useRouter()
  const [formData, setFormData] = useState([])

  console.log('Request Data', formData)
  

  useEffect(()=> {
    const token = localStorage.getItem("adminInfo")
    console.log('TOKEN...', token)
    

     if(token == "" || token == null) {
        router.push('/')
      }

      getRequest(`http://127.0.0.1:8000/api/request/list`)
      .then(response => {
        setFormData(response.data)
      })
      .catch(error => {
        console.error(error);
    });
    
  }, [])

  return (
    <Grid container spacing={6}>
      <Grid item xs={12}>
        <Typography variant='h5'>
          <Link href='#' target='_blank'>
          First Section
          </Link>
        </Typography>
        {/* <Typography variant='body2'>Tables display sets of data. They can be fully customized</Typography> */}
      </Grid>
      <Grid item xs={12}>
        <Card>
          <CardHeader title='' titleTypographyProps={{ variant: 'h6' }} />
          {/* <TableBasic /> */}
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label='simple table'>
              <TableHead>
                <TableRow>
                  <TableCell>S. No</TableCell>
                  <TableCell align='center'>How much do you want to invest?</TableCell>
                  <TableCell align='center'>For what purpose?</TableCell>
                  <TableCell align='center'>For how long do you plan to invest?</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {formData.map((item, index) => {
                  return(
                    <TableRow
                  key={index}
                  sx={{
                    '&:last-of-type td, &:last-of-type th': {
                      border: 0
                    }
                  }}
                >
                  <TableCell component='th' scope='row'>
                    {index+1}
                  </TableCell>
                  <TableCell align='center'>{item?.amount}</TableCell>
                  <TableCell align='center'>{item?.purpose}</TableCell>
                  <TableCell align='center'>{item?.duration}</TableCell>
                </TableRow>
                  )
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </Card>
      </Grid>
    </Grid>
  )
}

export default Users
