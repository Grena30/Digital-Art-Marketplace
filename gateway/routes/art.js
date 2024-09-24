const express = require('express');
const router = express.Router();
const axios = require('axios');

router.get('/', async (req, res) => {
    try {
        const response = await axios.get('http://art-management-service:5001/api/artworks/');
        res.json(response.data);
    } catch (error) {
        res.status(error.response.status).send(error.response.data);
    }
});

router.get('/:id', async (req, res) => {
    try {
        const response = await axios.get(`http://art-management-service:5001/api/artworks/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        res.status(error.response.status).send(error.response.data);
    }
});

router.post('/', async (req, res) => {
    try {
        const response = await axios.post('http://art-management-service:5001/api/artworks/', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response.status).send(error.response.data);
    }
})

router.get('/status', async (req, res) => {
    try {
        const response = await axios.get('http://art-management-service:5001/api/artworks/status', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response.status).send(error.response.data);
    }
});

module.exports = router;
