// Imports
Product = require('../models/productModel');

// ======================================================================

/**
 * Busca todos los productos existentes
 */
exports.findAllProducts = function (req, res) {
    Product.get(function (err, products) {
        if (err) {
            res.json({
                status: "error",
                message: err,
            });
        }
        res.json(products);
    });
};

/**
 * Crea un nuevo producto según la información suministrada en el JSON
 */
exports.createProduct = function (req, res) {
    var product = new Product();

    product.nombre = req.body.nombre;
    product.codigoBarras = req.body.codigoBarras;
    product.marca = req.body.marca;
    product.precio = req.body.precio;
    product.existencias = req.body.existencias;

    // save the product and check for errors
    product.save(function (err) {
        if (err)
            res.json(err);
        res.json(product);
    });
};

/**
 * Busca un producto por el codigo de barras del mismo
 */
exports.findProductById = function (req, res) {
    Product.findOne({codigoBarras: req.params.product_code}, 'nombre codigoBarras marca precio existencias', function (err, product) {
        if (err)
            res.send(err);
        res.json(product);
    });
};


/**
 * Actualiza un producto existente si existe en la base de datos
 */
exports.updateProduct = function (req, res) {
    Product.findOne({codigoBarras: req.params.product_code}, 'nombre codigoBarras marca precio existencias', function (err, product) {
        if (err)
            res.send(err);
        product.nombre = req.body.nombre ? req.body.nombre : product.nombre;
        product.codigoBarras = req.body.codigoBarras ? req.body.codigoBarras : product.codigoBarras;
        product.marca = req.body.marca ? req.body.marca : product.marca;
        product.precio = req.body.precio ? req.body.precio : product.precio;
        product.existencias = req.body.existencias ? req.body.existencias : product.existencias;
        // save the product and check for errors
        product.save(function (err) {
            if (err)
                res.json(err);
            res.json(product);
        });
    });
};

/**
 * Remueve un producto con el código de barras especificado
 */
exports.deleteProduct = function (req, res) {
    Product.findOneAndRemove({
        codigoBarras: req.params.product_code
    }, function (err, product) {
        if (err)
            res.send(err);
        res.json({
            status: "success",
            message: 'Producto borrado'
        });
    });
};

// ================================================================================
// Funciones de kafka

/**
 * Actualiza un producto según el codigo de barras dado y la cantidad de comprados del mismo
 */
exports.updateProductKafka = function (message) {
    Product.findOne({codigoBarras: message.codigoBarras}, 'nombre codigoBarras marca precio existencias', function (err, product) {
        if (err)
            console.error('Error actualizado producto según el topico de kafka!');
        if (!product)
            console.error('No se encontró producto con ese código de barras!');
        else {
            product.existencias = (product.existencias - message.comprados) <= 0 ? 0 : (product.existencias - message.comprados);
            // save the product and check for errors
            product.save(function (err) {
                if (err)
                    console.error(err);
                console.log('Producto actualizado, existencias reducidas de: ' + JSON.stringify(product) );
            });
        }
    });
}