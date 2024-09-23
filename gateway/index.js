const express = require('express');
const axios = require('axios');
const loginRoutes = require('./routes/login');
const artRoutes = require('./routes/art');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/api/auth', loginRoutes);
app.use('/api/art', artRoutes);

app.listen(PORT, () => {
    console.log(`Gateway is running on port ${PORT}`);
});
