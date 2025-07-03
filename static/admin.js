// Admin Panel JavaScript - Enhanced UI and Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all admin panel features
    initializeAdminPanel();
});

function initializeAdminPanel() {
    // Add loading animations
    addLoadingAnimations();
    
    // Add interactive effects
    addInteractiveEffects();
    
    // Add real-time updates
    addRealTimeUpdates();
    
    // Add confirmation dialogs
    addConfirmationDialogs();
    
    // Add search and filter functionality
    addSearchAndFilter();
    
    // Add responsive navigation
    addResponsiveNavigation();

    // Add clear all student handler
    addClearAllStudentHandler();
}

function addLoadingAnimations() {
    // Add page load animation
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        document.body.style.opacity = '1';
    }, 100);

    // Add card entrance animations
    const cards = document.querySelectorAll('.card, .stat-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 + (index * 100));
    });
}

function addInteractiveEffects() {
    // Add hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0,0,0,0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
        });
    });

    // Add button click effects
    const buttons = document.querySelectorAll('.btn, button');
    buttons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add form input effects
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
}

function addRealTimeUpdates() {
    // Update system status in real-time
    updateSystemStatus();
    setInterval(updateSystemStatus, 30000); // Update every 30 seconds

    // Add live student count updates
    updateStudentCount();
    setInterval(updateStudentCount, 10000); // Update every 10 seconds
}

function updateSystemStatus() {
    const statusElement = document.querySelector('.system-status');
    if (statusElement) {
        statusElement.innerHTML = '🟢 System Online';
        statusElement.style.animation = 'pulse 1s ease-in-out';
        
        setTimeout(() => {
            statusElement.style.animation = '';
        }, 1000);
    }
}

function updateStudentCount() {
    // This would typically fetch from the server
    // For now, we'll simulate updates
    const countElements = document.querySelectorAll('.student-count');
    countElements.forEach(element => {
        const currentCount = parseInt(element.textContent) || 0;
        const newCount = currentCount + Math.floor(Math.random() * 3) - 1;
        if (newCount >= 0) {
            element.textContent = newCount;
            element.style.animation = 'countUpdate 0.5s ease-out';
            setTimeout(() => {
                element.style.animation = '';
            }, 500);
        }
    });
}

function addConfirmationDialogs() {
    // Enhanced confirmation for destructive actions (EXCLUDE clearAllForm and clearTestContentForm buttons)
    const destructiveButtons = document.querySelectorAll(
        '.btn-danger:not(#clearAllForm .btn-danger):not(#clearTestContentForm .btn-warning), .btn-warning:not(#clearTestContentForm .btn-warning):not(#clearAllForm .btn-danger)'
    );
    destructiveButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const action = this.textContent.trim();
            const message = `Are you sure you want to ${action.toLowerCase()}? This action cannot be undone.`;
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
            // Show loading state
            this.innerHTML = '<span class="loading-spinner"></span> Processing...';
            this.disabled = true;
        });
    });
}

function addSearchAndFilter() {
    // Add search functionality to tables
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search...';
        searchInput.className = 'table-search';
        searchInput.style.cssText = `
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        `;
        
        table.parentNode.insertBefore(searchInput, table);
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });
}

function addResponsiveNavigation() {
    // Add mobile menu toggle
    const navToggle = document.createElement('button');
    navToggle.className = 'nav-toggle';
    navToggle.innerHTML = '☰';
    navToggle.style.cssText = `
        display: none;
        background: none;
        border: none;
        font-size: 24px;
        color: white;
        cursor: pointer;
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    `;
    
    document.body.appendChild(navToggle);
    
    // Mobile menu functionality
    navToggle.addEventListener('click', function() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('mobile-open');
        }
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.sidebar') && !e.target.closest('.nav-toggle')) {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                sidebar.classList.remove('mobile-open');
            }
        }
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
    `;
    
    // Set background color based on type
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function addRippleEffect(element) {
    element.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes countUpdate {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    @media (max-width: 768px) {
        .nav-toggle {
            display: block !important;
        }
        
        .sidebar {
            transform: translateX(-100%);
            transition: transform 0.3s ease-in-out;
        }
        
        .sidebar.mobile-open {
            transform: translateX(0);
        }
    }
`;
document.head.appendChild(style); 


function addClearAllStudentHandler() {
    const clearAllForm = document.getElementById('clearAllForm');
    if (clearAllForm) {
        clearAllForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!confirm('Are you sure you want to clear all student data? This action cannot be undone.')) {
                return;
            }

            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
            }

            fetch('/cleardata', {
                method: 'POST'
            })
            .then(res => res.json())
            .then(data => {
                // Only show one alert and reload
                alert(data.message);
                window.location.href = '/admindashboard';
            })
            .catch(err => {
                alert('Error clearing data. Please try again.');
                console.error('Fetch error:', err);
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="fas fa-trash"></i> Clear All students Data';
                    submitBtn.disabled = false;
                }
            });
        });
    }

    // Add handler for clearTestContentForm
    const clearTestContentForm = document.getElementById('clearTestContentForm');
    if (clearTestContentForm) {
        clearTestContentForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!confirm('Are you sure you want to clear all test content? This action cannot be undone.')) {
                return;
            }

            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
            }

            fetch('/cleartestcontent', {
                method: 'POST'
            })
            .then(res => res.json())
            .then(data => {
                // Only show one alert and reload
                alert(data.message);
                window.location.href = '/admindashboard';
            })
            .catch(err => {
                alert('Error clearing test content. Please try again.');
                console.error('Fetch error:', err);
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="fas fa-eraser"></i> Clear Test Content';
                    submitBtn.disabled = false;
                }
            });
        });
    }
}
