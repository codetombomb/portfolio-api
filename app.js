const express = require('express');
const mongoose = require('mongoose')
const app = express();
const cors = require('cors');
require('dotenv/config') // ACCESS .ENV FILE

app.use(express.json())
app.use(cors());

// ROUTES 
const homeRoute = require('./routes/home');
app.use('/home', homeRoute)

const projectsRoutes = require('./routes/projects')
app.use('/projects', projectsRoutes)

const aboutRoute = require('./routes/about')
app.use('/about', aboutRoute)


//LISTEN ON PORT 3000
app.listen(4000, () => {
    console.log('listening on port 4000')
})

// CONNTECT TO MONGODB
mongoose.connect(process.env.DB_CONNECTION,
    { useNewUrlParser: true, useUnifiedTopology: true },
    () => {
        console.log('Connected to DB')
    })
