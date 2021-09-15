const express = require('express');
const mongoose = require('mongoose')
const app = express();
const cors = require('cors');
// require('dotenv/config') // ACCESS .ENV FILE
require('dotenv').config({ path: './.env' });
app.use(express.json())
app.use(cors());

// ROUTES 
const homeRoute = require('./routes/home');
app.use('/home', homeRoute)

const projectsRoutes = require('./routes/projects')
app.use('/projects', projectsRoutes)

const aboutRoute = require('./routes/about')
app.use('/about', aboutRoute)

const port = process.env.PORT || 4000;

// CONNTECT TO MONGODB
const fireItUp = async () => {
    try {
        await mongoose.connect(`${process.env.DB_CONNECTION}`, {
            useNewUrlParser: true,
            useCreateIndex: true,
            useFindAndModify: false,
            useUnifiedTopology: true,
            family: 4 // Use IPv4, skip trying IPv6
        })
        app.listen(port, () => {
            console.log('listening on %d', port)
        })
        console.log('Connected to %d', port)
    } catch (err) {
            console.log('Failed to connect to MongoDB', err);
    }
}

fireItUp();