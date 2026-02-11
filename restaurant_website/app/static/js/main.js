// Main JavaScript for Restaurant Website

// ===== UTILITY FUNCTIONS =====
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// ===== NAVBAR SCROLL EFFECT =====
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('shadow');
    } else {
        navbar.classList.remove('shadow');
    }
});

// ===== FORM VALIDATION =====
const forms = document.querySelectorAll('.needs-validation');
forms.forEach(form => {
    form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);
});

// ===== MENU SEARCH & FILTER =====
const menuSearch = document.getElementById('menuSearch');
if (menuSearch) {
    menuSearch.addEventListener('input', debounce((e) => {
        const searchTerm = e.target.value.toLowerCase();
        const menuItems = document.querySelectorAll('.menu-item-card');
        
        menuItems.forEach(item => {
            const itemName = item.querySelector('.menu-item-title').textContent.toLowerCase();
            const itemDesc = item.querySelector('.menu-item-description').textContent.toLowerCase();
            
            if (itemName.includes(searchTerm) || itemDesc.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }, 300));
}

// ===== CATEGORY FILTER =====
const categoryBadges = document.querySelectorAll('.category-badge');
categoryBadges.forEach(badge => {
    badge.addEventListener('click', () => {
        const category = badge.dataset.category;
        const menuItems = document.querySelectorAll('.menu-item-card');
        
        // Update active badge
        categoryBadges.forEach(b => b.classList.remove('active'));
        badge.classList.add('active');
        
        // Filter items
        menuItems.forEach(item => {
            if (category === 'all' || item.dataset.category === category) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
});

// ===== RESERVATION FORM - AVAILABILITY CHECK =====
const reservationForm = document.getElementById('reservationForm');
if (reservationForm) {
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
    const partySizeInput = document.getElementById('party_size');
    const availabilityMessage = document.getElementById('availabilityMessage');
    
    const checkAvailability = debounce(async () => {
        const date = dateInput?.value;
        const time = timeInput?.value;
        const partySize = partySizeInput?.value;
        
        if (!date || !time || !partySize) return;
        
        try {
            const response = await fetch('/check-availability?' + new URLSearchParams({
                date: date,
                time: time,
                party_size: partySize
            }));
            
            const data = await response.json();
            
            if (availabilityMessage) {
                if (data.available) {
                    availabilityMessage.innerHTML = `
                        <div class="alert alert-success">
                            <i class="fas fa-check-circle me-2"></i>${data.message}
                        </div>
                    `;
                } else {
                    availabilityMessage.innerHTML = `
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle me-2"></i>${data.message}
                        </div>
                    `;
                }
            }
        } catch (error) {
            console.error('Error checking availability:', error);
        }
    }, 500);
    
    dateInput?.addEventListener('change', checkAvailability);
    timeInput?.addEventListener('change', checkAvailability);
    partySizeInput?.addEventListener('change', checkAvailability);
}

// ===== IMAGE LAZY LOADING =====
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    const lazyImages = document.querySelectorAll('img.lazy');
    lazyImages.forEach(img => imageObserver.observe(img));
}

// ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#!') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ===== GALLERY LIGHTBOX CONFIGURATION =====
if (typeof lightbox !== 'undefined') {
    lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true,
        'albumLabel': 'Image %1 of %2'
    });
}

// ===== TOOLTIP INITIALIZATION =====
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// ===== POPOVER INITIALIZATION =====
const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
});

// ===== DATE PICKER MIN DATE =====
const today = new Date().toISOString().split('T')[0];
const datePickers = document.querySelectorAll('input[type="date"]');
datePickers.forEach(picker => {
    picker.setAttribute('min', today);
});

// ===== LOADING STATE HANDLER =====
const showLoading = (element) => {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border spinner-border-sm me-2';
    spinner.setAttribute('role', 'status');
    element.prepend(spinner);
    element.disabled = true;
};

const hideLoading = (element) => {
    const spinner = element.querySelector('.spinner-border');
    if (spinner) spinner.remove();
    element.disabled = false;
};

// ===== AJAX FORM SUBMISSION =====
const ajaxForms = document.querySelectorAll('.ajax-form');
ajaxForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = form.querySelector('[type="submit"]');
        showLoading(submitBtn);
        
        const formData = new FormData(form);
        const url = form.getAttribute('action') || window.location.href;
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Show success message
                showAlert('success', data.message || 'Success!');
                form.reset();
            } else {
                // Show error message
                showAlert('danger', data.message || 'An error occurred');
            }
        } catch (error) {
            console.error('Form submission error:', error);
            showAlert('danger', 'An error occurred. Please try again.');
        } finally {
            hideLoading(submitBtn);
        }
    });
});

// ===== ALERT HELPER =====
const showAlert = (type, message) => {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = alertHtml;
        container.insertBefore(tempDiv.firstElementChild, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = container.querySelector('.alert');
            if (alert) {
                bootstrap.Alert.getInstance(alert)?.close();
            }
        }, 5000);
    }
};

// ===== PHONE NUMBER FORMATTING =====
const phoneInputs = document.querySelectorAll('input[type="tel"]');
phoneInputs.forEach(input => {
    input.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 0) {
            if (value.length <= 3) {
                value = `(${value}`;
            } else if (value.length <= 6) {
                value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
            } else {
                value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 10)}`;
            }
        }
        e.target.value = value;
    });
});

// ===== STAR RATING SYSTEM =====
const starRatings = document.querySelectorAll('.star-rating');
starRatings.forEach(rating => {
    const stars = rating.querySelectorAll('.star');
    const input = rating.querySelector('input[type="hidden"]');
    
    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            const value = index + 1;
            input.value = value;
            
            stars.forEach((s, i) => {
                if (i < value) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
        });
        
        star.addEventListener('mouseenter', () => {
            stars.forEach((s, i) => {
                if (i <= index) {
                    s.classList.add('hover');
                } else {
                    s.classList.remove('hover');
                }
            });
        });
    });
    
    rating.addEventListener('mouseleave', () => {
        stars.forEach(s => s.classList.remove('hover'));
    });
});

// ===== COPY TO CLIPBOARD =====
const copyButtons = document.querySelectorAll('[data-copy]');
copyButtons.forEach(button => {
    button.addEventListener('click', async () => {
        const text = button.dataset.copy;
        try {
            await navigator.clipboard.writeText(text);
            showAlert('success', 'Copied to clipboard!');
        } catch (error) {
            console.error('Copy failed:', error);
        }
    });
});

// ===== PRINT PAGE =====
const printButtons = document.querySelectorAll('[data-print]');
printButtons.forEach(button => {
    button.addEventListener('click', () => {
        window.print();
    });
});

// ===== AUTO-HIDE ALERTS =====
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// ===== EXPORT =====
window.restaurantApp = {
    showAlert,
    showLoading,
    hideLoading,
    debounce
};
