const express = require('express');
const router = express.Router();
const About = require('../models/About')

router.get('/', async  (req, res) => {
    try {
        const about = await About.find();
        res.send(about)
    } catch (err) {
        res.json({ message: err.message })
    }
})

router.post('/', (req, res) => {
    console.log(req.body.info)
    const about = new About({
        info: req.body.info,
    })

    about.save()
        .then(data => {
            res.json(data);
        })
        .catch(err => {
            res.json({ message: err.message });
        })
})

module.exports = router;