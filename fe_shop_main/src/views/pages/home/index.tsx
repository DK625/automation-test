// ** Next
import { NextPage } from 'next'

// ** React
import { useEffect, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'

// ** Mui
import { Box, Grid, Typography, useTheme, Tab, Tabs, TabsProps } from '@mui/material'

// ** Redux

// ** Components
import Spinner from 'src/components/spinner'
import CustomPagination from 'src/components/custom-pagination'
import CardProduct from 'src/views/pages/product/components/CardProduct'
import FilterProduct from 'src/views/pages/product/components/FilterProduct'
import InputSearch from 'src/components/input-search'
import NoData from 'src/components/no-data'
import CustomBreadcrumb from 'src/components/breadcrumb'

// ** Config
import { PAGE_SIZE_OPTION } from 'src/configs/gridConfig'

// ** Services
import { getAllProductTypes } from 'src/services/product-type'
import { getAllCities } from 'src/services/city'
import { getAllProductsPublic } from 'src/services/product'

// ** Utils
import { formatFilter } from 'src/utils'
import { TProduct } from 'src/types/product'
import { styled } from '@mui/material'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from 'src/stores'
import toast from 'react-hot-toast'
import { resetInitialState } from 'src/stores/product'
import { OBJECT_TYPE_ERROR_PRODUCT } from 'src/configs/error'
import CustomSelect from 'src/components/custom-select'
import CardSkeleton from 'src/views/pages/product/components/CardSkeleton'
import ChatBotAI from 'src/components/chat-bot-ai'
import { useRouter } from 'next/router'

interface TOptions {
  label: string
  value: string
}

type TProps = {
  products: TProduct[]
  totalCount: number
  productTypesServer: TOptions[]
  paramsServer: {
    limit: number
    page: number
    order: string
    productType: string
  }
}

interface TProductPublicState {
  data: TProduct[]
  total: number
}

const StyledTabs = styled(Tabs)<TabsProps>(({ theme }) => ({
  '&.MuiTabs-root': {
    borderBottom: 'none',
    '& .MuiTab-root': {
      margin: '0 4px',
      borderRadius: '8px',
      transition: 'all 0.3s ease',
      fontWeight: 500,
      '&:hover': {
        backgroundColor: theme.palette.mode === 'light'
          ? 'rgba(0, 0, 0, 0.04)'
          : 'rgba(255, 255, 255, 0.08)',
        transform: 'translateY(-2px)',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)'
      },
      '&.Mui-selected': {
        backgroundColor: theme.palette.mode === 'light'
          ? `${theme.palette.primary.main}15`
          : `${theme.palette.primary.main}25`,
        color: theme.palette.primary.main,
        fontWeight: 700,
        boxShadow: `0 2px 8px ${theme.palette.primary.main}30`
      }
    },
    '& .MuiTabs-indicator': {
      backgroundColor: theme.palette.primary.main,
      height: '3px',
      borderRadius: '3px 3px 0 0'
    }
  }
}))

const HomePage: NextPage<TProps> = props => {
  // ** Translate
  const { t } = useTranslation()

  // ** Props
  const { products, totalCount, paramsServer, productTypesServer } = props

  // State
  const [sortBy, setSortBy] = useState('createdAt desc')
  const [searchBy, setSearchBy] = useState('')
  const [productTypeSelected, setProductTypeSelected] = useState('')
  const [reviewSelected, setReviewSelected] = useState('')
  const [locationSelected, setLocationSelected] = useState('')

  const [optionCities, setOptionCities] = useState<{ label: string; value: string }[]>([])

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    if (!firstRender.current) {
      firstRender.current = true
    }
    setProductTypeSelected(newValue)
    setPage(1) // Reset to page 1 when changing tabs
    setPageSize(PAGE_SIZE_OPTION[0]) // Reset to default page size (8)
  }

  const [pageSize, setPageSize] = useState(PAGE_SIZE_OPTION[0])
  const [page, setPage] = useState(1)
  const [optionTypes, setOptionTypes] = useState<{ label: string; value: string }[]>([])
  const [filterBy, setFilterBy] = useState<Record<string, string | string[]>>({})
  const [loading, setLoading] = useState(false)
  const [productsPublic, setProductsPublic] = useState<TProductPublicState>({
    data: [],
    total: 0
  })

  // ** Ref
  const firstRender = useRef<boolean>(false)
  const isServerRendered = useRef<boolean>(false)

  // ** Redux
  const {
    isSuccessLike,
    isErrorLike,
    isErrorUnLike,
    typeError,
    isSuccessUnLike,
    messageErrorLike,
    messageErrorUnLike,
    isLoading
  } = useSelector((state: RootState) => state.product)
  const dispatch: AppDispatch = useDispatch()

  // ** theme
  const theme = useTheme()
  const router = useRouter()

  // fetch api
  const handleGetListProducts = async () => {
    setLoading(true)
    const query = {
      params: { limit: pageSize, page: page, search: searchBy, order: sortBy, ...formatFilter(filterBy) }
    }
    await getAllProductsPublic(query).then(res => {
      if (res?.data) {
        setLoading(false)
        setProductsPublic({
          data: res?.data?.products,
          total: res?.data?.totalCount
        })
      }
    })
  }

  const handleOnchangePagination = (page: number, pageSize: number) => {
    setPage(page)
    setPageSize(pageSize)
    if (!firstRender.current) {
      firstRender.current = true
    }
  }

  const handleFilterProduct = (value: string, type: string) => {
    switch (type) {
      case 'review': {
        setReviewSelected(value)
        if (!firstRender.current) {
          firstRender.current = true
        }
        break
      }
      case 'location': {
        setLocationSelected(value)
        if (!firstRender.current) {
          firstRender.current = true
        }
        break
      }
    }
  }

  const handleResetFilter = () => {
    setLocationSelected('')
    setReviewSelected('')
  }

  // ** fetch api

  const fetchAllCities = async () => {
    setLoading(true)
    await getAllCities({ params: { limit: -1, page: -1 } })
      .then(res => {
        const data = res?.data.cities
        if (data) {
          setOptionCities(data?.map((item: { name: string; _id: string }) => ({ label: item.name, value: item._id })))
        }
        setLoading(false)
      })
      .catch(e => {
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchAllCities()
  }, [])

  useEffect(() => {
    if (!isServerRendered.current && paramsServer && !!productTypesServer?.length) {
      setPage(paramsServer.page)
      setPageSize(paramsServer.limit)
      setSortBy(paramsServer.order)
      if (paramsServer?.productType) {
        setProductTypeSelected(paramsServer?.productType)
      }
      setProductsPublic({
        data: products,
        total: totalCount
      })
      setOptionTypes(productTypesServer)
      isServerRendered.current = true
    }
  }, [paramsServer, products, totalCount, productTypesServer])

  useEffect(() => {
    if (isServerRendered.current && firstRender.current) {
      handleGetListProducts()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sortBy, searchBy, page, pageSize, filterBy])

  useEffect(() => {
    if (isServerRendered.current && firstRender.current) {
      setFilterBy({ productType: productTypeSelected, minStar: reviewSelected, productLocation: locationSelected })
    }
  }, [productTypeSelected, reviewSelected, locationSelected])

  useEffect(() => {
    if (isSuccessLike) {
      toast.success(t('Like_product_success'))
      handleGetListProducts()
      dispatch(resetInitialState())
    } else if (isErrorLike && messageErrorLike && typeError) {
      const errorConfig = OBJECT_TYPE_ERROR_PRODUCT[typeError]
      if (errorConfig) {
        toast.error(t(errorConfig))
      } else {
        toast.error(t('Like_product_error'))
      }
      dispatch(resetInitialState())
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSuccessLike, isErrorLike, messageErrorLike, typeError])

  useEffect(() => {
    if (isSuccessUnLike) {
      toast.success(t('Unlike_product_success'))
      dispatch(resetInitialState())
      handleGetListProducts()
    } else if (isErrorUnLike && messageErrorUnLike && typeError) {
      const errorConfig = OBJECT_TYPE_ERROR_PRODUCT[typeError]
      if (errorConfig) {
        toast.error(t(errorConfig))
      } else {
        toast.error(t('Unlike_product_error'))
      }
      dispatch(resetInitialState())
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSuccessUnLike, isErrorUnLike, messageErrorUnLike, typeError])

  // Get current selected product type name
  const selectedProductTypeName = optionTypes.find(opt => opt.value === productTypeSelected)?.label || ''

  return (
    <>
      {loading && <Spinner />}
      <ChatBotAI />
      <Box
        sx={{
          height: '100%',
          width: '100%'
        }}
      >
        <CustomBreadcrumb
          items={[
            { label: 'Trang chủ', href: '/' },
            ...(selectedProductTypeName ? [{ label: selectedProductTypeName }] : [])
          ]}
        />
        <StyledTabs value={productTypeSelected} onChange={handleChange} aria-label='wrapped label tabs example'>
          {optionTypes.map(opt => {
            return (
              <Tab
                key={opt.value}
                value={opt.value}
                label={opt.label}
                data-testid={`tab-${opt.label}`} // Add test ID
              />
            )
          })}
        </StyledTabs>
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 4 }}>
          <Box sx={{ display: 'flex', gap: '20px' }}>
            <Box sx={{ width: '300px' }}>
              <CustomSelect
                fullWidth
                onChange={e => {
                  if (!firstRender.current) {
                    firstRender.current = true
                  }
                  setSortBy(e.target.value as string)
                }}
                value={sortBy}
                options={[
                  {
                    label: t('Sort_best_sold'),
                    value: 'sold desc'
                  },
                  {
                    label: t('Sort_new_create'),
                    value: 'createdAt desc'
                  },
                  {
                    label: t('Sort_high_view'),
                    value: 'views desc'
                  },
                  {
                    label: t('Sort_high_like'),
                    value: 'totalLikes desc'
                  }
                ]}
                placeholder={t('Sort_by')}
              />
            </Box>
            <Box sx={{ width: '300px' }}>
              <InputSearch
                placeholder={t('Search_name_product')}
                value={searchBy}
                onChange={(value: string) => {
                  if (!firstRender.current) {
                    firstRender.current = true
                  }
                  setSearchBy(value)
                }}
              />
            </Box>
          </Box>
        </Box>

        <Box
          sx={{
            height: '100%',
            width: '100%',
            mt: 4,
            mb: 8
          }}
        >
          <Grid
            container
            spacing={{
              md: 6,
              xs: 4
            }}
          >
            {/*<Grid item md={3} display={{ md: 'flex', xs: 'none' }}>*/}
            {/*  /!*<Box sx={{ width: '100%' }}>*!/*/}
            {/*  /!*  <FilterProduct*!/*/}
            {/*  /!*    locationSelected={locationSelected}*!/*/}
            {/*  /!*    reviewSelected={reviewSelected}*!/*/}
            {/*  /!*    handleReset={handleResetFilter}*!/*/}
            {/*  /!*    optionCities={optionCities}*!/*/}
            {/*  /!*    handleFilterProduct={handleFilterProduct}*!/*/}
            {/*  /!*  />*!/*/}
            {/*  /!*</Box>*!/*/}
            {/*</Grid>*/}
            <Grid item md={12} xs={12}>
              {loading ? (
                <Grid
                  container
                  spacing={{
                    md: 6,
                    xs: 4
                  }}
                >
                  {Array.from({ length: 6 }).map((_, index) => {
                    return (
                      <Grid item key={index} md={4} sm={6} xs={12}>
                        <CardSkeleton />
                      </Grid>
                    )
                  })}
                </Grid>
              ) : (
                <Grid
                  container
                  spacing={{
                    md: 6,
                    xs: 4
                  }}
                >
                  {productsPublic?.data?.length > 0 ? (

                    <>
                      {productsPublic?.data?.map((item: TProduct) => {
                        return (
                          <Grid item key={item._id} md={3} sm={6} xs={12}>

                            <CardProduct item={item} />
                          </Grid>
                        )
                      })}
                    </>
                  ) : (
                    <Box sx={{ width: '100%', mt: 10 }}>
                      <NoData widthImage='60px' heightImage='60px' textNodata={t('No_product')} />
                    </Box>
                  )}
                </Grid>
              )}
              {totalCount && (
                <Box mt={6}>
                  <CustomPagination
                    onChangePagination={handleOnchangePagination}
                    pageSizeOptions={PAGE_SIZE_OPTION}
                    pageSize={pageSize}
                    page={page}
                    rowLength={productsPublic.total}
                    isHideShowed
                  />
                </Box>
              )}
            </Grid>
          </Grid>
        </Box>
      </Box>
    </>
  )
}

export default HomePage
