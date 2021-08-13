const express = require('express');
const mongoose = require('mongoose')
const app = express();
require('dotenv/config') // ACCESS .ENV FILE

// ROUTES 
const homeRoute = require('./routes/home');
app.use('/home', homeRoute)

const projectsRoutes = require('./routes/projects')
app.use('/projects', projectsRoutes)


//LISTEN ON PORT 3000
app.listen(3000, () => {
    console.log('listening on port 3000')
})

//CONNTECT TO MONGODB
mongoose.connect(process.env.DB_CONNECTION, 
{ useNewUrlParser: true }, 
() => {console.log('Connected to DB')
})
