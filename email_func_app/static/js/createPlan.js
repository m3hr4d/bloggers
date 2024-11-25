document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createPlanForm');
    const steps = form.querySelectorAll('.form-step');
    const stepItems = document.querySelectorAll('.step-item');
    const progressBar = document.querySelector('.progress-bar');
    const progressPercentage = document.querySelector('.progress-percentage');
    const nextButtons = form.querySelectorAll('.btn-next');
    const prevButtons = form.querySelectorAll('.btn-prev');
    let currentStep = 0;

    // Initialize progress
    updateProgress(0);

    // Next button click handler
    nextButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                steps[currentStep].classList.remove('active');
                currentStep++;
                steps[currentStep].classList.add('active');
                updateProgress(currentStep);
            }
        });
    });

    // Previous button click handler
    prevButtons.forEach(button => {
        button.addEventListener('click', () => {
            steps[currentStep].classList.remove('active');
            currentStep--;
            steps[currentStep].classList.add('active');
            updateProgress(currentStep);
        });
    });

    // Update progress bar and step numbers
    function updateProgress(step) {
        const percent = (step / (steps.length - 1)) * 100;
        progressBar.style.width = `${percent}%`;
        progressPercentage.textContent = `${Math.round(percent)}%`;

        // Update step items
        stepItems.forEach((item, index) => {
            if (index <= step) {
                item.classList.add('completed');
            } else {
                item.classList.remove('completed');
            }
            if (index === step) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    // Validate current step
    function validateStep(step) {
        const currentStepElement = steps[step];
        const inputs = currentStepElement.querySelectorAll('input[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        // For step 3 (services), at least one service should be selected
        if (step === 2) {
            const checkedServices = currentStepElement.querySelectorAll('input[type="checkbox"]:checked');
            if (checkedServices.length === 0) {
                isValid = false;
                // Show error message
                const servicesGrid = currentStepElement.querySelector('.services-grid');
                if (!servicesGrid.nextElementSibling?.classList.contains('error-message')) {
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'error-message';
                    errorMessage.textContent = 'لطفاً حداقل یک خدمت را انتخاب کنید';
                    servicesGrid.after(errorMessage);
                }
            } else {
                const errorMessage = currentStepElement.querySelector('.error-message');
                if (errorMessage) {
                    errorMessage.remove();
                }
            }
        }

        return isValid;
    }

    // Form submit handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateStep(currentStep)) {
            // Submit form
            this.submit();
        }
    });
});
