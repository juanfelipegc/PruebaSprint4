// Imports
let router = require('express').Router();
var productController = require('./controllers/productController');

// Set default API response
router.get('/', function (req, res) {
    res.json({
       status: 'success',
       message: 'Raíz de MS inventario en productos',
    });
});

// Import product controller
// Rutas de Productos
router.route('/productos')
    .get(productController.findAllProducts)
    .post(productController.createProduct);
router.route('/productos/:product_code')
    .get(productController.findProductById)
    .put(productController.updateProduct)
    .delete(productController.deleteProduct);

// Export API routes
module.exports.router = router;
module.exports.updateProductKafka = productController.updateProductKafka;