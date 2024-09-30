const express = require('express');
const router = express.Router();
const axios = require('axios');

const getAuthHeader = (req) => {
    const token = req.headers.authorization;
    return token ? { Authorization: token } : {};
};

router.post('/login', async (req, res) => {
    try {
        const response = await axios.post('http://login-service:5000/api/auth/login', req.body);
        if (!res.headersSent) {
            res.json(response.data);
        }
    } catch (error) {
        if (!res.headersSent) {
            res.status(error.response?.status || 500).send(error.response?.data || { message: 'Request failed' });
        }
    }
});

router.post('/register', async (req, res) => {
    try {
        const response = await axios.post('http://login-service:5000/api/auth/register', req.body);
        if (!res.headersSent) {
            res.json(response.data);
        }
    } catch (error) {
        if (!res.headersSent) {
            res.status(error.response?.status || 500).send(error.response?.data || { message: 'Request failed' });
        }
    }
});

router.post('/logout', async (req, res) => {
    try {
        const response = await axios.post('http://login-service:5000/api/auth/logout', req.body, {
            headers: getAuthHeader(req),
        });
        if (!res.headersSent) {
            res.json(response.data);
        }
    } catch (error) {
        if (!res.headersSent) {
            res.status(error.response?.status || 500).send(error.response?.data || { message: 'Request failed' });
        }
    }
});

router.get('/status', async (req, res) => {
    try {
        const response = await axios.get('http://login-service:5000/api/auth/status', req.body);
        if (!res.headersSent) {
            res.json(response.data);
        }
    } catch (error) {
        if (!res.headersSent) {
            res.status(error.response?.status || 500).send(error.response?.data || { message: 'Request failed' });
        }
    }
});

router.get('/timeout', async (req, res) => {
    try {
        const response = await axios.get('http://login-service:5000/api/auth/timeout', req.body);
        if (!res.headersSent) {
            res.json(response.data);
        }
    } catch (error) {
        if (!res.headersSent) {
            res.status(error.response?.status || 500).send(error.response?.data || { message: 'Request failed' });
        }
    }
});

module.exports = router;
