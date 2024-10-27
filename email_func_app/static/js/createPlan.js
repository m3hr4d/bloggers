document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createPlanForm');
    const steps = document.querySelectorAll('.form-step');
    const progressBar = document.querySelector('.progress-bar');
    const progressPercentage = document.querySelector('.progress-percentage');
    const stepItems = document.querySelectorAll('.step-item');
    const totalSteps = steps.length;
    let currentStep = 0;

    // Initialize the form
    updateFormState();

    // Next button click handler
    document.querySelectorAll('.btn-next').forEach(button => {
        button.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                currentStep++;
                updateFormState();
            }
        });
    });

    // Previous button click handler
    document.querySelectorAll('.btn-prev').forEach(button => {
        button.addEventListener('click', () => {
            currentStep--;
            updateFormState();
        });
    });

    // Service selection handler
    document.querySelectorAll('.service-option').forEach(option => {
        option.addEventListener('click', function() {
            this.classList.toggle('selected');
            const checkbox = this.querySelector('input[type="checkbox"]');
            checkbox.checked = !checkbox.checked;
        });
    });

    // Update form state (progress, visibility, etc.)
    function updateFormState() {
        // Update progress bar
        const progress = ((currentStep + 1) / totalSteps) * 100;
        progressBar.style.width = `${progress}%`;
        progressPercentage.textContent = `${Math.round(progress)}%`;

        // Update steps visibility
        steps.forEach((step, index) => {
            step.classList.remove('active');
            if (index === currentStep) {
                step.classList.add('active');
            }
        });

        // Update step indicators
        stepItems.forEach((item, index) => {
            item.classList.remove('active', 'completed');
            if (index === currentStep) {
                item.classList.add('active');
            } else if (index < currentStep) {
                item.classList.add('completed');
            }
        });

        // Add entrance animation to current step
        steps[currentStep].classList.add('step-enter');
        setTimeout(() => {
            steps[currentStep].classList.remove('step-enter');
        }, 500);
    }

    // Validate current step
    function validateStep(stepIndex) {
        const currentStepElement = steps[stepIndex];
        const requiredFields = currentStepElement.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('invalid');
                showError(field);
            } else {
                field.classList.remove('invalid');
                hideError(field);
            }
        });

        return isValid;
    }

    // Show error message
    function showError(field) {
        const existingError = field.parentElement.querySelector('.error-message');
        if (!existingError) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = 'این فیلد الزامی است';
            field.parentElement.appendChild(errorDiv);
        }
    }

    // Hide error message
    function hideError(field) {
        const error = field.parentElement.querySelector('.error-message');
        if (error) {
            error.remove();
        }
    }

    // Form submission handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateStep(currentStep)) {
            // Show success message with animation
            const successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            successMessage.innerHTML = `
                <div class="success-icon">
                    <i class="bi bi-check-circle"></i>
                </div>
                <h3>برنامه شما با موفقیت ثبت شد</h3>
                <p>به زودی کسب و کارها با شما تماس خواهند گرفت</p>
            `;
            form.innerHTML = '';
            form.appendChild(successMessage);
        }
    });
});
