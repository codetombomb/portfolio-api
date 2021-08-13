const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.send("We are sending Projects")
})

router.get('/specificProject', (req, res) => {
    res.send("We are sending a specific Projects")
})

module.exports = router;