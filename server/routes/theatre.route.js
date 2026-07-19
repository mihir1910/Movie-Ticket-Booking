const express = require('express')
const Theatre = require('../models/theatre.model.js');
const theatreRouter = express.Router(); // Route

theatreRouter.post('/add-theatre',  async (req, res) => {
    try{
        const newTheatre = new Theatre(req.body);
        await newTheatre.save();
        res.send({
            success: true,
            message: "New theatre has been added!"
        })
    }catch(err){
        res.send({
            success: false,
            message: err.message
        })
    }
});

// Get all theatres for Admin route
theatreRouter.get('/get-all-theatres', async (req, res) => {
    try{
        const allTheatres = await Theatre.find();
        res.send({
            success: true,
            message: "All theatres fetched!",
            data: allTheatres
        });
    }catch(err){
        res.send({
            success: false,
            message: err.message
        });
    }
});

// Get the theatres of a specific owner
// theatreRouter.post('/get-all-theatres-by-owner',  async (req, res) => {
//     try{
//         const allTheatres = await Theatre.find({owner: req.body.owner});
//         res.send({
//             success: true,
//             message: "All theatres fetched successfully!",
//             data: allTheatres
//         })
//     }catch(err){
//         res.send({
//             success: false,
//             message: err.message
//         })
//     }
// });


// Update theatre
theatreRouter.put('/update-theatre',  async (req, res) => {
    try{
        await Theatre.findByIdAndUpdate(req.body.theatreId, req.body);
        // console.log(req.body.theatreId)
        res.send({
            success: true,
            message: "Theatre has been updated!"
        })
    }catch(err){
        res.send({
            success: false,
            message: err.message
        })
    }
})

// Delete theatre
theatreRouter.put('/delete-theatre', async (req, res) => {
    try{
        await Theatre.findByIdAndDelete(req.body.theatreId);
        res.send({
            success: true,
            message: "The theatre has been deleted!"
        })
    }catch(err){
        res.send({
            success: false,
            message: err.message
        })
    }
});

module.exports = theatreRouter;