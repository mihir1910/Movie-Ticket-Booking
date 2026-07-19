const mongoose = require("mongoose");

const theatreSchema = new mongoose.Schema(
  {
    name : {
        type : String,
        required: true
    },
    address:{
        type:String,
        required : true
    },
    
    email:{

        type:String,
        required: true
    },
    phone : {
        type:Number,
        required: true
    },
    isActive:{
        type:Boolean,
        default:false
    },

    // owner:{
    //     type
    // },


  },
  { timestamps: true }
);

const Theatre = mongoose.model("theatre", theatreSchema);

module.exports = Theatre;