/**
 * PhishLab - Main JavaScript
 * Educational Cybersecurity Framework
 */

// Global utility functions
const PhishLab = {
    /**
     * Show loading state on button
     */
    showLoading: function(buttonId, spinId, textId, loadingText = 'Loading...') {
        const btn = document.getElementById(buttonId);
        const spinner = document.getElementById(spinId);
        const text = document.getElementById(textId);
        
        if (btn) btn.disabled = true;
        if (spinner) spinner.classList.remove('d-none');
        if (text) text.textContent = loadingText;
    },

    /**
     * Hide loading state on button
     */
    hideLoading: function(buttonId, spinId, textId, normalText) {
        const btn = document.getElementById(buttonId);
        const spinner = document.getElementById(spinId);
        const text = document.getElementById(textId);
        
        if (btn) btn.disabled = false;
        if (spinner) spinner.classList.add('d-none');
        if (text) text.textContent = normalText;
    },

    /**
     * Display error message
     */
    showError: function(message, elementId = null) {
        if (elementId) {
            const element = document.getElementById(elementId);
            if (element) {
                element.innerHTML = `
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <strong>Error:</strong> ${message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                `;
            }
        } else {
            alert('Error: ' + message);
        }
    },

    /**
     * Display success message
     */
    showSuccess: function(message, elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Success:</strong> ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    },

    /**
     * Scroll to element smoothly
     */
    scrollTo: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    },

    /**
     * Format risk score with color
     */
    formatRiskScore: function(score) {
        let color = '';
        let level = '';
        
        if (score >= 70) {
            color = 'danger';
            level = 'CRITICAL';
        } else if (score >= 50) {
            color = 'warning';
            level = 'HIGH';
        } else if (score >= 30) {
            color = 'info';
            level = 'MEDIUM';
        } else if (score > 0) {
            color = 'secondary';
            level = 'LOW';
        } else {
            color = 'success';
            level = 'SAFE';
        }
        
        return {
            color: color,
            level: level,
            score: score
        };
    },

    /**
     * Copy text to clipboard
     */
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showSuccess('Copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        } else {
            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            try {
                document.execCommand('copy');
                this.showSuccess('Copied to clipboard!');
            } catch (err) {
                console.error('Failed to copy:', err);
            }
            document.body.removeChild(textarea);
        }
    },

    /**
     * Format date/time
     */
    formatDateTime: function(date) {
        const options = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(date).toLocaleDateString('en-US', options);
    },

    /**
     * Validate URL format
     */
    isValidUrl: function(string) {
        try {
            new URL(string.startsWith('http') ? string : 'http://' + string);
            return true;
        } catch (_) {
            return false;
        }
    },

    /**
     * Sanitize HTML to prevent XSS
     */
    sanitizeHtml: function(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Generate random ID
     */
    generateId: function() {
        return 'id-' + Math.random().toString(36).substr(2, 9);
    }
};

// Initialize tooltips and popovers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });

    // Console warning
    console.log('%c⚠️ PHISHLAB WARNING', 'color: red; font-size: 20px; font-weight: bold;');
    console.log('%cThis is an educational cybersecurity tool.', 'font-size: 14px;');
    console.log('%cDo not use for malicious purposes.', 'font-size: 14px;');
    console.log('%cAll simulations are safe and offline.', 'font-size: 14px;');
});

// Handle Enter key on input fields
document.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        const target = event.target;
        
        // Check if we're in a specific input field
        if (target.id === 'urlInput') {
            const scanBtn = document.getElementById('scanBtn');
            const detectBtn = document.getElementById('detectBtn');
            
            if (scanBtn && window.location.pathname === '/url-scanner') {
                scanBtn.click();
            } else if (detectBtn && window.location.pathname === '/login-detector') {
                detectBtn.click();
            }
        } else if (target.id === 'headerInput') {
            const analyzeBtn = document.getElementById('analyzeBtn');
            if (analyzeBtn) {
                analyzeBtn.click();
            }
        }
    }
});

// Add active class to current nav item
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PhishLab;
}
