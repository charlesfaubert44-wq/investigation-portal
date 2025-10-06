const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../client')));

app.get('/api/dashboard/summary', (req, res) => {
  res.json({ total: 24, deadlines: 5, highRisk: 7 });
});

app.post('/api/evidence', upload.array('photos'), (req, res) => {
  const { investigationId, description, location } = req.body;
  const photos = req.files.map(f => f.filename);
  console.log('Evidence submitted:', { investigationId, description, location, photos });
  res.json({ success: true });
});

app.get('/api/legislation', (req, res) => {
  res.json([
    {
      title: "Workers’ Compensation Act (NT)",
      category: "Compensation",
      jurisdiction: "NT",
      url: "https://wscc.nt.ca/about-wscc/policy-and-legislation/legislation"
    },
    {
      title: "Safety Regulations (NU)",
      category: "Safety",
      jurisdiction: "NU",
      url: "https://wscc.nt.ca/about-wscc/policy-and-legislation/legislation"
    },
    {
      title: "Mine Health & Safety Act",
      category: "Mining",
      jurisdiction: "NT/NU",
      url: "https://wscc.nt.ca/about-wscc/policy-and-legislation/legislation"
    }
  ]);
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));

