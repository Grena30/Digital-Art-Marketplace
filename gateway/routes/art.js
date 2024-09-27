const express = require('express');
const router = express.Router();
const axios = require('axios');

// Get all
router.get('/', async (req, res) => {
    try {
        const response = await axios.get('http://art-management-service:5001/api/artworks/');
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Get by ID
router.get('/:id', async (req, res) => {
    try {
        const response = await axios.get(`http://art-management-service:5001/api/artworks/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Post
router.post('/', async (req, res) => {
    try {
        const response = await axios.post('http://art-management-service:5001/api/artworks/', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Update
router.put('/:id', async (req, res) => {
    try {
        const response = await axios.put(`http://art-management-service:5001/api/artworks/${req.params.id}`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.response ? error.response.data : 'Server error');
    }
});

// Delete
router.delete('/:id', async (req, res) => {
    try {
        const response = await axios.delete(`http://art-management-service:5001/api/artworks/${req.params.id}`);
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
