const mongoose = require('mongoose');

const AboutSchema = mongoose.Schema({
    info: []
})

module.exports = mongoose.model('About', AboutSchema)