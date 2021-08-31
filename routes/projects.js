const express = require('express');
const router = express.Router();
const Project = require('../models/Project')

router.get('/', async (req, res) => {
    try {
        const projects = await Project.find();
        res.send(projects)
    } catch (err) {
        res.json({ message: err.message })
    }
})

router.get('/:projectId', (req, res) => {
    console.log(req.params.projectId)
    res.send("We are sending a specific Project")
})

router.post('/', (req, res) => {
    const project = new Project({
        title: req.body.title,
        description: req.body.description,
        imgName: req.body.imgName,
        youTube: req.body.youTube,
        gitHub: req.body.gitHub,
        technologies: req.body.technologies
    })

    project.save()
        .then(data => {
            res.json(data);
        })
        .catch(err => {
            res.json({ message: err.message });
        })
})

module.exports = router;