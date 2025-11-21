/**
 * Client-side Form Validation for Warehouse Inventory Management System
 * Provides real-time validation feedback for forms
 */

// Initialize validation on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add Bootstrap validation classes
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Real-time validation for specific fields
    initializeFieldValidation();

    // Number input validation
    validateNumberInputs();

    // Date validation
    validateDateInputs();

    // Email validation
    validateEmailInputs();

    // Password validation
    validatePasswordInputs();
});

/**
 * Initialize field-level validation with real-time feedback
 */
function initializeFieldValidation() {
    // Validate on blur
    const inputs = document.querySelectorAll('input[required], textarea[required], select[required]');

    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') || this.classList.contains('is-valid')) {
                validateField(this);
            }
        });
    });
}

/**
 * Validate a single field and show feedback
 */
function validateField(field) {
    const isValid = field.checkValidity();

    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }

    return isValid;
}

/**
 * Validate number inputs (min, max, step)
 */
function validateNumberInputs() {
    const numberInputs = document.querySelectorAll('input[type="number"]');

    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);

            let errorMsg = '';

            if (this.value && isNaN(value)) {
                errorMsg = 'Please enter a valid number';
            } else if (!isNaN(min) && value < min) {
                errorMsg = `Value must be at least ${min}`;
            } else if (!isNaN(max) && value > max) {
                errorMsg = `Value must not exceed ${max}`;
            }

            showFieldError(this, errorMsg);
        });
    });
}

/**
 * Validate date inputs
 */
function validateDateInputs() {
    const dateInputs = document.querySelectorAll('input[type="date"]');

    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            let errorMsg = '';

            // Check if date is in the past (for expiry dates)
            if (this.classList.contains('expiry-date') && selectedDate <= today) {
                errorMsg = 'Expiry date must be in the future';
            }

            // Check if end date is before start date
            if (this.name === 'end_date') {
                const startDateInput = document.querySelector('input[name="start_date"]');
                if (startDateInput && startDateInput.value) {
                    const startDate = new Date(startDateInput.value);
                    if (selectedDate < startDate) {
                        errorMsg = 'End date must be after start date';
                    }
                }
            }

            showFieldError(this, errorMsg);
        });
    });
}

/**
 * Validate email inputs
 */
function validateEmailInputs() {
    const emailInputs = document.querySelectorAll('input[type="email"]');

    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            let errorMsg = '';

            if (this.value && !emailRegex.test(this.value)) {
                errorMsg = 'Please enter a valid email address';
            }

            showFieldError(this, errorMsg);
        });
    });
}

/**
 * Validate password inputs with strength indicator
 */
function validatePasswordInputs() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');

    passwordInputs.forEach(input => {
        // Add password strength indicator
        if (input.name === 'password' && !input.nextElementSibling?.classList.contains('password-strength')) {
            const strengthDiv = document.createElement('div');
            strengthDiv.className = 'password-strength mt-1';
            input.parentNode.insertBefore(strengthDiv, input.nextSibling);
        }

        input.addEventListener('input', function() {
            let errorMsg = '';

            // Password length validation
            if (this.value && this.value.length < 8) {
                errorMsg = 'Password must be at least 8 characters long';
            }

            // Show strength for password field
            if (this.name === 'password') {
                showPasswordStrength(this);
            }

            // Confirm password validation
            if (this.name === 'confirm_password') {
                const passwordInput = document.querySelector('input[name="password"]');
                if (passwordInput && this.value !== passwordInput.value) {
                    errorMsg = 'Passwords do not match';
                }
            }

            showFieldError(this, errorMsg);
        });
    });
}

/**
 * Show password strength indicator
 */
function showPasswordStrength(input) {
    const strengthDiv = input.nextElementSibling;
    if (!strengthDiv || !strengthDiv.classList.contains('password-strength')) return;

    const password = input.value;
    let strength = 0;
    let strengthText = '';
    let strengthClass = '';

    if (password.length === 0) {
        strengthDiv.innerHTML = '';
        return;
    }

    // Length check
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;

    // Character variety checks
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;

    // Determine strength level
    if (strength <= 2) {
        strengthText = 'Weak';
        strengthClass = 'text-danger';
    } else if (strength <= 4) {
        strengthText = 'Medium';
        strengthClass = 'text-warning';
    } else {
        strengthText = 'Strong';
        strengthClass = 'text-success';
    }

    strengthDiv.innerHTML = `<small class="${strengthClass}">Password Strength: ${strengthText}</small>`;
}

/**
 * Show error message for a field
 */
function showFieldError(field, errorMsg) {
    // Remove existing feedback
    const existingFeedback = field.parentElement.querySelector('.invalid-feedback:not(.d-none)');
    if (existingFeedback && existingFeedback.classList.contains('custom-error')) {
        existingFeedback.remove();
    }

    if (errorMsg) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');

        // Add custom error message
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback custom-error d-block';
        feedback.textContent = errorMsg;
        field.parentElement.appendChild(feedback);
    } else {
        field.classList.remove('is-invalid');
        if (field.value) {
            field.classList.add('is-valid');
        }
    }
}

/**
 * Validate barcode format (13 digits for EAN-13)
 */
function validateBarcode(input) {
    const barcode = input.value;
    let errorMsg = '';

    if (barcode && !/^\d{13}$/.test(barcode)) {
        errorMsg = 'Barcode must be exactly 13 digits';
    }

    showFieldError(input, errorMsg);
}

/**
 * Validate stock quantity
 */
function validateStock(input) {
    const stock = parseInt(input.value);
    let errorMsg = '';

    if (stock < 0) {
        errorMsg = 'Stock cannot be negative';
    }

    showFieldError(input, errorMsg);
}

/**
 * Validate price
 */
function validatePrice(input) {
    const price = parseFloat(input.value);
    let errorMsg = '';

    if (price <= 0) {
        errorMsg = 'Price must be greater than zero';
    }

    showFieldError(input, errorMsg);
}

// Export functions for use in other scripts
window.validateField = validateField;
window.validateBarcode = validateBarcode;
window.validateStock = validateStock;
window.validatePrice = validatePrice;
