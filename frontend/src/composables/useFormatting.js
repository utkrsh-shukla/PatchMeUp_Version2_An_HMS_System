export function useFormatting() {
    const formatDate = (dateStr) => {
        if (!dateStr) return 'N/A'
        return new Date(dateStr).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        })
    }

    const formatTime = (timeStr) => {
        if (!timeStr) return 'N/A'
        const [hours, minutes] = timeStr.split(':')
        const hour = parseInt(hours)
        const ampm = hour >= 12 ? 'PM' : 'AM'
        const hour12 = hour % 12 || 12
        return `${hour12}:${minutes} ${ampm}`
    }

    const formatDateTime = (dateStr, timeStr) => {
        return `${formatDate(dateStr)} at ${formatTime(timeStr)}`
    }

    return { formatDate, formatTime, formatDateTime }
}
