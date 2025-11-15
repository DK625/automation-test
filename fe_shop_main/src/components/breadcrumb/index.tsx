// ** React
import { FC } from 'react'
import { useRouter } from 'next/router'

// ** Mui
import { Breadcrumbs, Typography, Link, Box, useTheme } from '@mui/material'

// ** Icon
import Icon from 'src/components/Icon'

export interface BreadcrumbItem {
  label: string
  href?: string
}

interface BreadcrumbProps {
  items: BreadcrumbItem[]
}

const CustomBreadcrumb: FC<BreadcrumbProps> = ({ items }) => {
  const router = useRouter()
  const theme = useTheme()

  const handleClick = (event: React.MouseEvent<HTMLAnchorElement>, href?: string) => {
    event.preventDefault()
    if (href) {
      router.push(href)
    }
  }

  return (
    <Box sx={{ marginBottom: '16px' }}>
      <Breadcrumbs
        separator={<Icon icon='ic:round-navigate-next' fontSize={20} />}
        aria-label='breadcrumb'
        sx={{
          '& .MuiBreadcrumbs-separator': {
            color: theme.palette.text.secondary
          }
        }}
      >
        {items.map((item, index) => {
          const isLast = index === items.length - 1

          if (isLast || !item.href) {
            return (
              <Typography
                key={index}
                sx={{
                  color: theme.palette.primary.main,
                  fontWeight: 600,
                  fontSize: '14px'
                }}
              >
                {item.label}
              </Typography>
            )
          }

          return (
            <Link
              key={index}
              href={item.href}
              onClick={(e) => handleClick(e, item.href)}
              underline='hover'
              sx={{
                color: theme.palette.text.secondary,
                fontSize: '14px',
                cursor: 'pointer',
                '&:hover': {
                  color: theme.palette.primary.main
                }
              }}
            >
              {item.label}
            </Link>
          )
        })}
      </Breadcrumbs>
    </Box>
  )
}

export default CustomBreadcrumb
