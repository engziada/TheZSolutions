// Main JavaScript file

// Notification system
const showNotification = (message, type = 'success') => {
    const notification = document.createElement('div');
    notification.className = `notification ${type} animate-slide-in`;
    notification.innerHTML = `
        <div class="flex items-center">
            <div class="flex-shrink-0">
                ${type === 'success' 
                    ? '<svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/></svg>'
                    : type === 'error'
                        ? '<svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"/></svg>'
                        : '<svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v5a1 1 0 102 0V7zm0 8a1 1 0 10-2 0 1 1 0 102 0z"/></svg>'
                }
            </div>
            <div class="ml-3">
                <p class="text-sm font-medium text-gray-900">${message}</p>
            </div>
            <div class="ml-auto pl-3">
                <button class="inline-flex text-gray-400 hover:text-gray-500 focus:outline-none">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"/>
                    </svg>
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(notification);

    // Add click event to close button
    const closeButton = notification.querySelector('button');
    closeButton.addEventListener('click', () => {
        notification.remove();
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
};

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuButton = document.querySelector('[data-mobile-menu-button]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
            mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
            mobileMenu.classList.toggle('hidden');
        });

        // Mobile menu item click handler
        document.querySelectorAll('.mobile-menu .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
            });
        });
        
        // Ensure the home link also hides the mobile menu
        document.querySelector('[data-home]').addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            mobileMenuButton.setAttribute('aria-expanded', 'false');
        });
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation
const validateForm = (form) => {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('border-red-500');
            
            // Add error message
            const errorMessage = document.createElement('p');
            errorMessage.className = 'text-red-500 text-xs mt-1';
            errorMessage.textContent = 'This field is required';
            
            // Remove existing error message if any
            const existingError = input.parentNode.querySelector('.text-red-500');
            if (existingError) {
                existingError.remove();
            }
            
            input.parentNode.appendChild(errorMessage);
        } else {
            input.classList.remove('border-red-500');
            const errorMessage = input.parentNode.querySelector('.text-red-500');
            if (errorMessage) {
                errorMessage.remove();
            }
        }
    });

    return isValid;
};

// Initialize form validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!validateForm(this)) {
            e.preventDefault();
        }
    });
});

// File upload preview
const handleFileUpload = (input, previewContainer) => {
    const preview = document.getElementById(previewContainer);
    if (!preview) return;

    preview.innerHTML = '';
    const files = input.files;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();

        reader.onload = function(e) {
            const div = document.createElement('div');
            div.className = 'relative';
            
            if (file.type.startsWith('image/')) {
                div.innerHTML = `
                    <img src="${e.target.result}" class="h-20 w-20 object-cover rounded-md">
                    <button type="button" class="absolute top-0 right-0 -mt-2 -mr-2 bg-red-500 text-white rounded-full p-1" onclick="this.parentElement.remove()">
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                `;
            } else {
                div.innerHTML = `
                    <div class="h-20 w-20 flex items-center justify-center bg-gray-100 rounded-md">
                        <svg class="h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                        </svg>
                    </div>
                    <button type="button" class="absolute top-0 right-0 -mt-2 -mr-2 bg-red-500 text-white rounded-full p-1" onclick="this.parentElement.remove()">
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                `;
            }
            
            preview.appendChild(div);
        };

        reader.readAsDataURL(file);
    }
};

// Initialize tooltips
const initTooltips = () => {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    
    tooltips.forEach(tooltip => {
        const content = tooltip.getAttribute('data-tooltip');
        
        tooltip.addEventListener('mouseenter', () => {
            const tooltipElement = document.createElement('div');
            tooltipElement.className = 'absolute z-50 px-2 py-1 text-sm text-white bg-gray-900 rounded shadow-lg';
            tooltipElement.textContent = content;
            tooltipElement.style.top = tooltip.offsetTop - 30 + 'px';
            tooltipElement.style.left = tooltip.offsetLeft + (tooltip.offsetWidth / 2) - (tooltipElement.offsetWidth / 2) + 'px';
            document.body.appendChild(tooltipElement);
            
            tooltip.addEventListener('mouseleave', () => {
                tooltipElement.remove();
            });
        });
    });
};
