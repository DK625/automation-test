const User = require("../models/UserModel");
const Product = require("../models/ProductModel");
const bcrypt = require("bcrypt");
const { CONFIG_MESSAGE_ERRORS } = require("../configs");

const rollbackPassword = (email, newPassword) => {
  return new Promise(async (resolve, reject) => {
    try {
      const user = await User.findOne({ email });

      if (!user) {
        resolve({
          status: CONFIG_MESSAGE_ERRORS.INVALID.status,
          message: "User not found",
          typeError: CONFIG_MESSAGE_ERRORS.INVALID.type,
          data: null,
          statusMessage: "Error",
        });
        return;
      }

      const hash = bcrypt.hashSync(newPassword, 10);
      user.password = hash;
      await user.save();

      resolve({
        status: CONFIG_MESSAGE_ERRORS.ACTION_SUCCESS.status,
        message: "Password rollback successfully",
        typeError: "",
        data: { email: user.email },
        statusMessage: "Success",
      });
    } catch (e) {
      reject(e);
    }
  });
};

const rollbackPurchase = (email, productName) => {
  return new Promise(async (resolve, reject) => {
    try {
      // Rollback user addresses
      const user = await User.findOne({ email });

      if (!user) {
        resolve({
          status: CONFIG_MESSAGE_ERRORS.INVALID.status,
          message: "User not found",
          typeError: CONFIG_MESSAGE_ERRORS.INVALID.type,
          data: null,
          statusMessage: "Error",
        });
        return;
      }

      // Keep only the first address (Ha Noi)
      if (user.addresses && user.addresses.length > 0) {
        const firstAddress = user.addresses[0];
        user.addresses = [firstAddress];
        await user.save();
      }

      // Rollback product stock and sold
      const product = await Product.findOne({ name: productName });

      if (!product) {
        resolve({
          status: CONFIG_MESSAGE_ERRORS.INVALID.status,
          message: "Product not found",
          typeError: CONFIG_MESSAGE_ERRORS.INVALID.type,
          data: null,
          statusMessage: "Error",
        });
        return;
      }

      product.countInStock = 5;
      product.sold = 34;
      await product.save();

      resolve({
        status: CONFIG_MESSAGE_ERRORS.ACTION_SUCCESS.status,
        message: "Purchase data rollback successfully",
        typeError: "",
        data: {
          user: {
            email: user.email,
            addressesCount: user.addresses.length,
          },
          product: {
            name: product.name,
            countInStock: product.countInStock,
            sold: product.sold,
          },
        },
        statusMessage: "Success",
      });
    } catch (e) {
      reject(e);
    }
  });
};

module.exports = {
  rollbackPassword,
  rollbackPurchase,
};
