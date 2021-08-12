const express = require('express');
const app = express();

//ROUTES 
app.get('/', (req, res) => {
    res.send("We are home")
})

//LISTEN ON PORT 3000
app.listen(3000, () => {
    console.log('listening on port 3000')
})