// Main JavaScript for Hospital Management System V2

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    // Auto-hide alerts
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150);
        });
    }, 5000);
});

// Export for use in Vue components
export const autoHideAlerts = () => {
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150);
        });
    }, 5000);
};
