const {CONFIG_MESSAGE_ERRORS, CONFIG_USER_TYPE} = require("../configs");
const Product = require("../models/ProductModel");
const User = require("../models/UserModel");
const Order = require("../models/OrderProduct");
const Review = require("../models/ReviewModel");
const Comment = require("../models/CommentModel");
const {getAllOrder} = require("./OrderService");
const mongoose = require("mongoose");

const getReportCountProductType = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const pipeline = [
                {
                    $group: {
                        _id: {
                            type: "$type", // Group by type ObjectId
                            status: "$status",
                        },
                        count: {$sum: 1},
                    },
                },
                {
                    $group: {
                        _id: "$_id.type", // Group by type ObjectId
                        countsByStatus: {
                            $push: {
                                status: {$toString: "$_id.status"},
                                count: "$count",
                            },
                        },
                        total: {$sum: "$count"},
                    },
                },
                {
                    $lookup: {
                        from: "producttypes", // Assuming the name of the collection is producttypes
                        localField: "_id",
                        foreignField: "_id",
                        as: "type",
                    },
                },
                {
                    $unwind: "$type",
                },
                {
                    $project: {
                        _id: 0,
                        typeName: "$type.name",
                        countsByStatus: {
                            $arrayToObject: {
                                $map: {
                                    input: "$countsByStatus",
                                    as: "statusCount",
                                    in: {
                                        k: "$$statusCount.status",
                                        v: {
                                            count: "$$statusCount.count",
                                        },
                                    },
                                },
                            },
                        },
                        total: 1,
                    },
                },
            ];

            const productCountByTypeAndStatus = await Product.aggregate(pipeline);

            resolve({
                status: CONFIG_MESSAGE_ERRORS.GET_SUCCESS.status,
                message: "Success",
                typeError: "",
                statusMessage: "Success",
                data: productCountByTypeAndStatus,
            });
        } catch (e) {
            reject(e);
        }
    });
};

const getReportCountRecords = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const userCount = await User.countDocuments();
            const productCount = await Product.countDocuments();
            const orderCount = await Order.countDocuments();
            const reviewCount = await Review.countDocuments();
            const commentCount = await Comment.countDocuments();
            const monthlyIncomeOrder = await Order.find({
                status: 2,
            }).lean()

            const monthlyIncome = monthlyIncomeOrder.reduce(((acc, order) => acc + order.totalPrice), 0)


            const totalRevenue = await Order.aggregate([
                {
                    $group: {
                        _id: null,
                        total: {$sum: "$totalPrice"}
                    }
                }
            ])

            resolve({
                status: CONFIG_MESSAGE_ERRORS.GET_SUCCESS.status,
                message: "Success",
                typeError: "",
                statusMessage: "Success",
                data: {
                    user: userCount,
                    product: productCount,
                    order: orderCount,
                    review: reviewCount,
                    revenue: totalRevenue?.[0]?.total,
                    comment: commentCount,
                    monthlyIncome
                },
            });
        } catch (e) {
            reject(e);
        }
    });
};

const getReportCountUser = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const userStatistics = await User.aggregate([
                {
                    $group: {
                        _id: "$userType",
                        count: {$sum: 1},
                    },
                },
                {
                    $project: {
                        _id: 0,
                        userType: "$_id",
                        count: 1,
                    },
                },
            ]);

            const totalUser = await User.countDocuments();


            // Organize statistics by userType
            const result = {};
            userStatistics.forEach((stat) => {
                result[stat.userType] = stat.count;
            });


            resolve({
                status: CONFIG_MESSAGE_ERRORS.GET_SUCCESS.status,
                message: "Success",
                typeError: "",
                statusMessage: "Success",
                data: {data: result, total: totalUser},
            });
        } catch (e) {
            reject(e);
        }
    });
};

const getReportTotalRevenue = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const currentDate = new Date();
            const lastYearDate = new Date();
            lastYearDate.setFullYear(lastYearDate.getFullYear() - 1);

            const revenueByMonth = await Order.aggregate([
                {
                    $match: {
                        createdAt: {$gte: lastYearDate, $lte: currentDate}
                    }
                },
                {
                    $group: {
                        _id: {month: {$month: "$createdAt"}, year: {$year: "$createdAt"}},
                        total: {$sum: "$totalPrice"}
                    }
                },
                {
                    $project: {
                        _id: 0,
                        month: "$_id.month",
                        year: "$_id.year",
                        total: 1
                    }
                },
                {
                    $sort: {"year": 1, "month": 1}
                }
            ]);


            resolve({
                status: CONFIG_MESSAGE_ERRORS.GET_SUCCESS.status,
                message: "Success",
                typeError: "",
                statusMessage: "Success",
                data: revenueByMonth,
            });
        } catch (e) {
            reject(e);
        }
    });
};

const getReportCountOrderStatus = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const orderStatistics = await Order.aggregate([
                {
                    $group: {
                        _id: "$status",
                        total: {$sum: 1}
                    }
                }
            ]);

            const orderCount = await Order.countDocuments();

            const statisticsByStatus = {};
            orderStatistics.forEach(stat => {
                statisticsByStatus[stat._id] = stat.total;
            });

            resolve({
                status: CONFIG_MESSAGE_ERRORS.GET_SUCCESS.status,
                message: "Success",
                typeError: "",
                statusMessage: "Success",
                data: {
                    data: statisticsByStatus,
                    total: orderCount
                },
            });
        } catch (e) {
            reject(e);
        }
    });
};

const getReportCountProductStatus = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const productStatistics = await Product.aggregate([
                {
                    $group: {
                        _id: "$status",
                        count: {$sum: 1},
                    },
                },
            ]);
            const totalCount = await Product.countDocuments();

            // Tổ chức thống kê theo status
            const result = {};
            productStatistics.forEach((stat) => {
                result[stat._id] = stat.count;
            });

            resolve({
                status: CONFIG_MESSAGE_ERRORS.GET_SUCCESS.status,
                message: "Success",
                typeError: "",
                statusMessage: "Success",
                data: {
                    data: result,
                    total: totalCount

                },
            });
        } catch (e) {
            reject(e);
        }
    });
};

async function getMonthlyProductAnalytics(year, month) {
    const startDate = new Date(year, month - 1, 1);
    const endDate = new Date(year, month, 0);

    const analytics = await Order.aggregate([

        {
            $match: {
                createdAt: {
                    $gte: startDate,
                    $lte: endDate
                },
                status: {$ne: 3}
            }
        },
        {
            $unwind: "$orderItems"
        },
        {
            $lookup: {
                from: "products",
                localField: "orderItems.product",
                foreignField: "_id",
                as: "productInfo"
            }
        },
        {
            $unwind: "$productInfo"
        },
        {
            $lookup: {
                from: "producttypes",
                localField: "productInfo.type",
                foreignField: "_id",
                as: "typeInfo"
            }
        },
        {
            $unwind: "$typeInfo"
        },
        {
            $group: {
                _id: {
                    typeId: "$typeInfo._id",
                    typeName: "$typeInfo.name"
                },
                totalQuantity: {$sum: "$orderItems.amount"},
                totalRevenue: {
                    $sum: {
                        $multiply: [
                            "$orderItems.price",
                            "$orderItems.amount",
                            {
                                $subtract: [
                                    1,
                                    {$ifNull: [{$divide: ["$orderItems.discount", 100]}, 0]}
                                ]
                            }
                        ]
                    }
                },
                productsSold: {
                    $addToSet: {
                        productId: "$productInfo._id",
                        productName: "$productInfo.name",
                        quantity: "$orderItems.amount",
                        revenue: {
                            $multiply: [
                                "$orderItems.price",
                                "$orderItems.amount",
                                {
                                    $subtract: [
                                        1,
                                        {$ifNull: [{$divide: ["$orderItems.discount", 100]}, 0]}
                                    ]
                                }
                            ]
                        }
                    }
                },
                numberOfOrders: {$addToSet: "$_id"},
                averageOrderValue: {
                    $avg: {
                        $multiply: [
                            "$orderItems.price",
                            "$orderItems.amount",
                            {
                                $subtract: [
                                    1,
                                    {$ifNull: [{$divide: ["$orderItems.discount", 100]}, 0]}
                                ]
                            }
                        ]
                    }
                }
            }
        },
        {
            $addFields: {
                numberOfUniqueProducts: {$size: "$productsSold"},
                numberOfOrders: {$size: "$numberOfOrders"},
                averageQuantityPerOrder: {
                    $divide: ["$totalQuantity", {$size: "$numberOfOrders"}]
                }
            }
        },
        {
            $sort: {totalRevenue: -1}
        },
        {
            $project: {
                type: "$_id.typeName",
                totalQuantity: 1,
                totalRevenue: 1,
                numberOfUniqueProducts: 1,
                numberOfOrders: 1,
                averageOrderValue: 1,
                averageQuantityPerOrder: 1,
                productsSold: 1,
                _id: 0
            }
        }
    ]);
    return {
        status: CONFIG_MESSAGE_ERRORS.ACTION_SUCCESS.status,
        message: "Order cancelled successfully",
        typeError: "",
        data: analytics,
        statusMessage: "Success",
    }
}

const getCustomerOrderCounts = async () => {
    const customerOrderStats = await Order.aggregate([
        {
            $group: {
                _id: "$user",
                orderCount: {$sum: 1}
            }
        },
        {
            $lookup: {
                from: "users",
                localField: "_id",
                foreignField: "_id",
                as: "userDetails"
            }
        },
        {
            $unwind: "$userDetails"
        },
        {
            $project: {
                _id: 1,
                firstName: "$userDetails.firstName",
                lastName: "$userDetails.lastName",
                middleName: "$userDetails.middleName",
                email: "$userDetails.email",
                orderCount: 1,
                phoneNumber: "$userDetails.phoneNumber",
                avatar: "$userDetails.avatar",
            }
        },
        {
            $sort: {
                orderCount: -1
            }
        }
    ]);

    return {
        status: CONFIG_MESSAGE_ERRORS.ACTION_SUCCESS.status,
        message: "Order cancelled successfully",
        typeError: "",
        data: customerOrderStats,
        statusMessage: "Success",
    }
};


module.exports = {
    getCustomerOrderCounts,
    getMonthlyProductAnalytics,
    getReportCountProductType,
    getReportCountRecords,
    getReportCountUser,
    getReportTotalRevenue,
    getReportCountOrderStatus,
    getReportCountProductStatus
};
