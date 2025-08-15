const express = require('express');
const router = express.Router();

// GET home page. //
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

// GET test page. //
router.get('/testroute', function(req, res, next) {
  res.render('testpage', { title: 'Test Page' });
});


// Export //

module.exports = router;
