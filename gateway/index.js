const express = require('express');
const axios = require('axios');
const loginRoutes = require('./routes/login');
const artRoutes = require('./routes/art');


const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use((req, res, next) => {
    const timeout = setTimeout(() => {
        if (!res.headersSent) {
            return res.status(408).json({ message: 'Request timed out' });
        }
    }, 5000);

    res.on('finish', () => {
        clearTimeout(timeout);
    });

    next();
});
app.use('/api/auth', loginRoutes);
app.use('/api/art', artRoutes);

app.listen(PORT, () => {
    console.log(`Gateway is running on port ${PORT}`);
});
