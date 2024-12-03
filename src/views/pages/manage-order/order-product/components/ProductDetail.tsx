// @flow
import * as React from 'react';
import {hexToRGBA} from "src/utils/hex-to-rgba";
import CustomDataGrid from "src/components/custom-data-grid";
import {GridColDef} from "@mui/x-data-grid";
import {Typography, useTheme} from "@mui/material";
import GridInfo from "src/components/grid-info/GridInfo";
import GridCancel from "src/components/grid-cancel/GridCancel";
import GridDelete from "src/components/grid-delete";
import MoreButton from "src/views/pages/manage-order/order-product/components/MoreButton";
import OrderProduct from "src/stores/order-product";
import CustomPagination from "src/components/custom-pagination";
import {PAGE_SIZE_OPTION} from "src/configs/gridConfig";
import Image from "next/image";
import Spinner from "src/components/spinner";

type Props = {
    orderData: any;
};
export const ProductDetail = (props: Props) => {
    const theme = useTheme()
    const {orderData} = props;

    console.log(orderData.orderItems);
    const columns: GridColDef[] = [
        {
            field: 'product id',
            headerName: "Product id",
            minWidth: 150,
            maxWidth: 150,
            renderCell: params => {
                const {row} = params

                return <Typography>{row._id}</Typography>
            }
        },
        {
            field: 'product image',
            headerName: ('Product Image'),
            minWidth: 150,
            maxWidth: 150,
            renderCell: params => {
                const {row} = params

                return <Image width={100} height={100} src={row.image} alt=""/>
            }
        },
        {
            field: 'product_name',
            headerName: ('Product name'),
            minWidth: 250,
            maxWidth: 150,
            renderCell: params => {
                const {row} = params

                return <Typography>{row.name}</Typography>
            }
        },

        {
            field: 'quantity',
            headerName: "Quantity",
            minWidth: 200,
            maxWidth: 200,
            renderCell: params => {
                const {row} = params

                return <Typography>{row.amount}</Typography>
            }
        },
        {
            field: 'price',
            headerName: "Price",
            minWidth: 200,
            maxWidth: 200,
            renderCell: params => {
                const {row} = params

                return <Typography>{row.price}</Typography>
            }
        },
        {
            field: 'totalPrice',
            headerName: ('Total price'),
            minWidth: 150,
            maxWidth: 200,
            renderCell: params => {
                const {row} = params

                return <Typography>{row.price * row.amount - row.price * row.amount * row.discount / 100}</Typography>
            }
        },

    ]


    return (orderData.orderItems ? <CustomDataGrid
        rows={orderData.orderItems}
        columns={columns}
        autoHeight
        sx={{
            '.row-selected': {
                backgroundColor: `${hexToRGBA(theme.palette.primary.main, 0.08)} !important`,
                color: `${theme.palette.primary.main} !important`
            }
        }}
        sortingOrder={['desc', 'asc']}
        sortingMode='server'
        onSortModelChange={() => {
        }}
        getRowId={row => row._id}
        disableRowSelectionOnClick
        // slots={{
        //     pagination: <></>
        // }}
        disableColumnFilter
    /> : <Spinner/>)

};