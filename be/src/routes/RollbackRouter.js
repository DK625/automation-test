const express = require("express");
const router = express.Router();
const rollbackController = require("../controllers/RollbackController");

router.post("/password", rollbackController.rollbackPassword);
router.post("/purchase", rollbackController.rollbackPurchase);

module.exports = router;
