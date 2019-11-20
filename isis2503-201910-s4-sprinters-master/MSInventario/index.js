// Imports necesarios para funcionamiento de microservicio de inventario
const express = require('express');
const kafka = require('kafka-node');
const bodyParser = require('body-parser');

let mongoose = require('mongoose');
let inventoryRoutes = require('./inventory-routes');

//Configuración del microservicio
const port = process.env.PORT || 8000;
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Conexión a la base de datos
mongoose.connect('mongodb+srv://user:user@cluster0-jwmit.mongodb.net/inventory_db?retryWrites=true', { useNewUrlParser: true });
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error: '));

// Conexión con kafka 
var client = new kafka.KafkaClient({ kafkaHost: 'ec2-52-90-84-251.compute-1.amazonaws.com:9092', clientId: 'msinventario' });
var topics = [{ topic: 'actualizaciones' }];
var consumer = new kafka.Consumer(client, topics, { autoCommit: true });

consumer.on('message', async function (message) {
    console.log(JSON.parse(message.value));
    inventoryRoutes.updateProductKafka(JSON.parse(message.value));
});
consumer.on('error', function (err) {
    console.error('Error del consumidor: ' + err);
});

// Rutas del microservicio desde la raíz
app.get('/', (req, res) => res.send('Hello World!'));
app.use('/inventario', inventoryRoutes.router);

// Inicializar el microservicio para escucha
app.listen(port, () => {
    console.log('App listening on port ' + port);
});