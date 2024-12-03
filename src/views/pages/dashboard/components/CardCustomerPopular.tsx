import {Box, MenuItem, Typography, useTheme} from "@mui/material"
import Image from "next/image"
import {useRouter} from "next/router"
import {useTranslation} from "react-i18next"
import {ROUTE_CONFIG} from "src/configs/route"
import {formatNumberToLocal} from "src/utils"
import {TCustomerPopular, TProductPopular} from "src/views/pages/dashboard"

interface TProps {
    data: TCustomerPopular[]
}

const CardCustomerPopular = (props: TProps) => {

    const {data} = props

    const theme = useTheme()

    const router = useRouter()

    const {t} = useTranslation()

    const handleNavigateDetail = (slug: string) => {
        router.push(`${ROUTE_CONFIG.PRODUCT}/${slug}`)
    }

    return (
        <Box
            sx={{
                backgroundColor: theme.palette.background.paper,
                padding: '20px 0',
                height: '400px',
                width: '100%',
                borderRadius: '15px',
                "canvas": {
                    width: '100% !important',
                }
            }}
        >
           <Box sx={{ padding: "0 20px" }}>
    <Typography sx={{ fontWeight: "600", fontSize: "20px", mb: 2 }}>
        {t("Danh sách khách hàng mua nhiều nhất")}
    </Typography>
</Box>
{data
    ?.sort((a: TCustomerPopular, b: TCustomerPopular) => b.orderCount - a.orderCount) // Sắp xếp giảm dần theo orderCount
    .slice(0, 5) // Lấy 5 phần tử đầu tiên
    .map((product: TCustomerPopular) => (
        <MenuItem
            key={product._id}
            sx={{ gap: 2 }}
            onClick={() => {
                // Xử lý khi click
            }}
        >
            <Image height={40} width={40} src={product.avatar} alt="image" />
            <Box sx={{ width: "60%" }}>
                <Typography
                    sx={{
                        fontWeight: "600",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        width: "100%",
                    }}
                >
                    {product.email}
                </Typography>
            </Box>
            <Typography>{product.orderCount} order(s)</Typography>
        </MenuItem>
    ))}
</Box>

    )
}

export default CardCustomerPopular