const RollbackService = require("../services/RollbackService");
const { CONFIG_MESSAGE_ERRORS } = require("../configs");

const rollbackPassword = async (req, res) => {
  try {
    const email = "lovecatdat@gmail.com";
    const password = "123456@Dat";

    const response = await RollbackService.rollbackPassword(email, password);
    const { data, status, typeError, message, statusMessage } = response;

    return res.status(status).json({
      typeError,
      data,
      message,
      status: statusMessage,
    });
  } catch (e) {
    console.log("Rollback password error:", e);
    return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
      typeError: "Internal Server Error",
      data: null,
      status: "Error",
    });
  }
};

const rollbackPurchase = async (req, res) => {
  try {
    const email = "lovecatdat@gmail.com";
    const productName = "Microsoft Surface Laptop 5";

    const response = await RollbackService.rollbackPurchase(email, productName);
    const { data, status, typeError, message, statusMessage } = response;

    return res.status(status).json({
      typeError,
      data,
      message,
      status: statusMessage,
    });
  } catch (e) {
    console.log("Rollback purchase error:", e);
    return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
      typeError: "Internal Server Error",
      data: null,
      status: "Error",
    });
  }
};

module.exports = {
  rollbackPassword,
  rollbackPurchase,
};
