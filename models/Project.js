const mongoose = require('mongoose');

//create a schema
const ProjectSchema = mongoose.Schema({
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    },
    youtubeLink: {
        type: String,
        required: true
    },
    technologies: [],

})


module.exports = mongoose.model('Projects', ProjectSchema)