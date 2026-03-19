const express = require('express');
const GodManager = require('./GodManager');
const { config } = require('./utils');

const app = express();
app.use(express.json());

const manager = new GodManager();
manager.initDb();
manager.setupRoutes(app);

app.listen(config.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
});