const express = require('express');
const router = express.Router();
const axios = require('axios');

router.post('/login', async (req, res) => {
    try {
        const response = await axios.post('http://login-service:5000/api/auth/login', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response.status).send(error.response.data);
    }
});

router.post('/register', async (req, res) => {
    try {
        const response = await axios.post('http://login-service:5000/api/auth/register', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response.status).send(error.response.data);
    }
});

router.get('/status', async (req, res) => {
    try {
        const response = await axios.get('http://login-service:5000/api/auth/status', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response.status).send(error.response.data);
    }
});

module.exports = router;
