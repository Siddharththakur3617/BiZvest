document.addEventListener('DOMContentLoaded', function() {
    const searchInputs = document.querySelectorAll('input[name="q"]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.style.borderColor = '#333';
            } else {
                this.style.borderColor = '#ddd';
            }
        });
    });
});