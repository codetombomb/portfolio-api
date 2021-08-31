const mongoose = require('mongoose');

//create a schema
const ProjectSchema = mongoose.Schema({
    title: {
        type: String,
        required: true
    },
    imgName: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    },
    youTube: {
        type: String,
        required: true
    },
    gitHub: {
        type: String,
        required: true
    },
    technologies: []

})


module.exports = mongoose.model('Projects', ProjectSchema)