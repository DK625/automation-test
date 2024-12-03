import {Box, useTheme} from "@mui/material"
import {TCountProductType} from "src/views/pages/dashboard"

import {Bar} from "react-chartjs-2";
import 'chart.js/auto';
import {useMemo} from "react";
import {useTranslation} from "react-i18next";
import LineChart from "src/views/pages/dashboard/components/Chart";

interface TProps {
    data: TCountProductType[]
}

const CardMonthlyIncomeByRevenue = ({rawData}: any) => {

    // Props
    // const {data} = props
    //
    const theme = useTheme()
    // const {t} = useTranslation()
    //
    // const labelsMemo = useMemo(() => {
    //     return data?.map((item) => item?.typeName)
    // }, [data])
    //
    const data = {
        labels: rawData.map((record: any) => record.type)
        , // X-axis labels
        datasets: [
            {
                label: 'Doanh thu theo tháng (VND)',
                data: rawData.map((item: any) => item.totalRevenue),
                borderColor: 'rgba(75, 192, 192, 1)', // Line color
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill under the line
                tension: 0,
            },
        ],
    };
    console.log({rawData});

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Doanh số danh mục mặt hàng theo tháng',
            },
        },
        scales: {
            y: {
                beginAtZero: true, // Start Y-axis from 0
            },
        },
    };

    return (
        <Box
            sx={{
                backgroundColor: theme.palette.background.paper,
                padding: '20px',
                height: '400px',
                width: '100%',
                borderRadius: '15px',
                mt: 4,
                "canvas": {
                    width: '100% !important',
                    height: '100% !important',
                }
            }}
        >
            <LineChart data={data} options={options}/>
        </Box>
    )
}

export default CardMonthlyIncomeByRevenue