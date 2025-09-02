const { CONFIG_MESSAGE_ERRORS } = require("../configs");
const ReportService = require("../services/ReportService");
const { getMonthlyProductAnalytics, getCustomerOrderCounts } = require("../services/ReportService");

const getReportCountProductType = async (req, res) => {
    try {
        const response = await ReportService.getReportCountProductType();
        const { data, status, typeError, message, statusMessage } = response;
        return res.status(status).json({
            typeError,
            data,
            message,
            status: statusMessage,
        });
    } catch (e) {
        return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
            message: "Internal Server Error",
            data: null,
            status: "Error",
            typeError: CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.type,
        });
    }
};


const getReportCountRecords = async (req, res) => {
    try {
        const response = await ReportService.getReportCountRecords();
        const { data, status, typeError, message, statusMessage } = response;
        return res.status(status).json({
            typeError,
            data,
            message,
            status: statusMessage,
        });
    } catch (e) {
        return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
            message: "Internal Server Error",
            data: null,
            status: "Error",
            typeError: CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.type,
        });
    }
};

const getReportCountUser = async (req, res) => {
    try {
        const response = await ReportService.getReportCountUser();
        const { data, status, typeError, message, statusMessage } = response;
        return res.status(status).json({
            typeError,
            data,
            message,
            status: statusMessage,
        });
    } catch (e) {
        return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
            message: "Internal Server Error",
            data: null,
            status: "Error",
            typeError: CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.type,
        });
    }
};

const getReportTotalRevenue = async (req, res) => {
    try {
        const response = await ReportService.getReportTotalRevenue();
        const { data, status, typeError, message, statusMessage } = response;
        return res.status(status).json({
            typeError,
            data,
            message,
            status: statusMessage,
        });
    } catch (e) {
        return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
            message: "Internal Server Error",
            data: null,
            status: "Error",
            typeError: CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.type,
        });
    }
};
const getReportCountOrderStatus = async (req, res) => {
    try {
        const response = await ReportService.getReportCountOrderStatus();
        const { data, status, typeError, message, statusMessage } = response;
        return res.status(status).json({
            typeError,
            data,
            message,
            status: statusMessage,
        });
    } catch (e) {
        return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
            message: "Internal Server Error",
            data: null,
            status: "Error",
            typeError: CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.type,
        });
    }
};

const getReportCountProductStatus = async (req, res) => {
    try {
        const response = await ReportService.getReportCountProductStatus();
        const { data, status, typeError, message, statusMessage } = response;
        return res.status(status).json({
            typeError,
            data,
            message,
            status: statusMessage,
        });
    } catch (e) {
        return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
            message: "Internal Server Error",
            data: null,
            status: "Error",
            typeError: CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.type,
        });
    }
};
const getMonthlyIncome = async (req, res) => {
    try {
        const currentDate = new Date();
        const response = await getMonthlyProductAnalytics(
            currentDate.getFullYear(),
            currentDate.getMonth() + 1
        );


        const { data, status, typeError, message, statusMessage } = response;
        return res.status(status).json({
            typeError,
            data,
            message,
            status: statusMessage,
        });
    } catch (e) {
        console.log(e);
        return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
            message: "Internal Server Error",
            data: null,
            status: "Error",
            typeError: CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.type,
        });
    }
}

const getCustomerOrderCount = async (req, res) => {
    try {

        const response = await getCustomerOrderCounts();


        const { data, status, typeError, message, statusMessage } = response;
        return res.status(status).json({
            typeError,
            data,
            message,
            status: statusMessage,
        });
    } catch (e) {
        console.log(e);
        return res.status(CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.status).json({
            message: "Internal Server Error",
            data: null,
            status: "Error",
            typeError: CONFIG_MESSAGE_ERRORS.INTERNAL_ERROR.type,
        });
    }
}
module.exports = {
    getCustomerOrderCount,
    getMonthlyIncome,
    getReportCountProductType,
    getReportCountRecords,
    getReportCountUser,
    getReportTotalRevenue,
    getReportCountOrderStatus,
    getReportCountProductStatus
};
