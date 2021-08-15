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


//LISTEN ON PORT 3000
app.listen(3000, () => {
    console.log('listening on port 3000')
})

// CONNTECT TO MONGODB
mongoose.connect(process.env.DB_CONNECTION, 
    { useNewUrlParser: true, useUnifiedTopology: true  }, 
() => {console.log('Connected to DB')
})
