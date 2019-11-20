// Imports
var mongoose = require('mongoose');

// =====================================================================

// Setup schema
var productSchema = mongoose.Schema({
    nombre: {
        type: String,
        required: true
    },
    codigoBarras: {
        type: String,
        required: true
    },
    marca: String,
    precio: {
        type: Number,
        required: true
    },
    existencias: {
        type: Number,
        required: true
    }
});

// Export Product model
var Product = module.exports = mongoose.model('products', productSchema);
module.exports.get = function (callback, limit) {
    Product.find(callback).limit(limit);
}