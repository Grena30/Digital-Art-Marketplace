const express = require('express');
const router = express.Router();
const axios = require('axios');


const getAuthHeader = (req) => {
    const token = req.headers.authorization;
    return token ? { Authorization: token } : {};
};

// Search art
router.get('/search', async (req, res) => {
    try {
        const response = await axios.get('http://art-management-service:5001/api/artworks/search', { params: req.query });
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Get popular art
router.get('/popular', async (req, res) => {
    try {
        const response = await axios.get('http://art-management-service:5001/api/artworks/popular', { params: req.query });
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Update profile
router.put('/profile', async (req, res) => {
    try {
        const response = await axios.put('http://art-management-service:5001/api/artworks/profile', req.body, {
            headers: getAuthHeader(req)
        });
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Delete profile
router.delete('/profile', async (req, res) => {
    try {
        const response = await axios.delete('http://art-management-service:5001/api/artworks/profile', {
            headers: getAuthHeader(req),
            data: req.body  // For DELETE, pass the body in 'data'
        });
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Post artwork
router.post('/', async (req, res) => {
    try {
        const response = await axios.post('http://art-management-service:5001/api/artworks', req.body, {
            headers: getAuthHeader(req)
        });
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Update artwork
router.put('/:id', async (req, res) => {
    try {
        const response = await axios.put(`http://art-management-service:5001/api/artworks/${req.params.id}`, req.body, {
            headers: getAuthHeader(req)
        });
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Delete artwork
router.delete('/:id', async (req, res) => {
    try {
        const response = await axios.delete(`http://art-management-service:5001/api/artworks/${req.params.id}`, {
            headers: getAuthHeader(req)
        });
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Check status
router.get('/status', async (req, res) => {
    try {
        const response = await axios.get('http://art-management-service:5001/api/artworks/status', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

module.exports = router;
