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

const GridCancel = (props: TGridInfo) => {
    const {t} = useTranslation()

    // Props
    const {onClick, disabled} = props

    return (
        <Tooltip title={t('Cancel')}>
            <IconButton onClick={onClick} disabled={disabled}>
                <Icon icon="material-symbols:cancel"/>
            </IconButton>
        </Tooltip>
    )
}

export default GridCancel
