const express = require('express');
const router = express.Router();
const Project = require('../models/Project')

router.get('/', async(req, res) => {
    try{
        const projects = await Project.find();
        console.log(projects.length)
        res.send(projects)
    } catch (err) {
        res.json({message: err})
    }
})

router.get('/specificProject', (req, res) => {
    res.send("We are sending a specific Project")
})

router.post('/', (req, res) => {
    const project = new Project({
        title: req.body.title,
        description: req.body.description,
        technologies: req.body.technologies
    })

    project.save()
    .then(data => {
        res.json(data);
    })
    .catch(err => {
        res.json({message: err.message});
    })
})

module.exports = router;