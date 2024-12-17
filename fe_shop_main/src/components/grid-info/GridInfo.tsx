// ** React
import React from 'react'
import {useTranslation} from 'react-i18next'

// ** Mui
import Icon from 'src/components/Icon'
import {IconButton, Tooltip} from '@mui/material'

interface TGridInfo {
    onClick: () => void
    disabled?: boolean
}

const GridInfo = (props: TGridInfo) => {
    const {t} = useTranslation()

    // Props
    const {onClick, disabled} = props

    return (
        <Tooltip title={t('Detail')}>
            <IconButton onClick={onClick} disabled={disabled}>
                <Icon icon='tabler:eye'/>
            </IconButton>
        </Tooltip>
    )
}

export default GridInfo
