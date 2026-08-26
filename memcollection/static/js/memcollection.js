/**
 * Ensures that certain fields on CustomImage are only shown when the appropriate
 * image type is selected.
 */
function initializeFieldVisibility() {
    const imageTypeSelect = document.querySelector('select[name*="image_type"]');

    if (!imageTypeSelect) return;

    const formContainer = imageTypeSelect.closest('form');

    if (!formContainer) return;

    const fieldsByType = {
        specimen: ['specimen_record', 'position'],
        insect: ['species', 'species_page', 'sex', 'stage', 'status'],
        plant: ['scientific_name', 'common_name', 'plant_species_page'],
        habitat: ['habitat_species_page'],
        location: ['country', 'state', 'county', 'locality', 'gps', 'collecting_trip'],
    };

    /**
     * Gets the wrapper element around a given field
     * @param {string} fieldName - The name of the field
     * @returns The field wrapper element or null
     */
    function getFieldWrapper(fieldName) {
        const fieldElement = formContainer.querySelector(`[data-contentpath="${fieldName}"]`);
        if (fieldElement) {
            return fieldElement.closest('.w-field__wrapper');
        }
        return null;
    }

    /**
     * Updates the visibility of custom fields
     */
    function updateFieldVisibility() {
        const selectedType = imageTypeSelect.value;

        // Hide all type-specific fields first
        Object.keys(fieldsByType).forEach(type => {
            fieldsByType[type].forEach(fieldName => {
                const wrapper = getFieldWrapper(fieldName);
                if (wrapper && type !== 'location') {
                    if (wrapper.parentElement === 'li') {
                        wrapper.parentElement.style.display = 'none';
                    } else {
                        wrapper.style.display = 'none';
                    }
                }
            });
        });

        // Show fields for selected type
        if (fieldsByType[selectedType]) {
            fieldsByType[selectedType].forEach(fieldName => {
                const wrapper = getFieldWrapper(fieldName);
                if (wrapper) {
                    if (wrapper.parentElement === 'li') {
                        wrapper.parentElement.style.display = 'block';
                    } else {
                        wrapper.style.display = 'block';
                    }
                }
            });
        }

        // Handle location fields - show for all types except specimen
        fieldsByType.location.forEach(fieldName => {
            const wrapper = getFieldWrapper(fieldName);
            if (wrapper) {
                if (wrapper.parentElement === 'li') {
                    wrapper.parentElement.style.display = selectedType === 'specimen' ? 'none' : 'block';
                } else {
                    wrapper.style.display = selectedType === 'specimen' ? 'none' : 'block';
                }
            }
        });
    }

    updateFieldVisibility();

    imageTypeSelect.addEventListener('change', updateFieldVisibility);
}

document.addEventListener('DOMContentLoaded', initializeFieldVisibility);

// Also try to initialize immediately in case DOM is already loaded
if (document.readyState !== 'loading') {
    initializeFieldVisibility();
}

// Use MutationObserver to catch dynamically loaded forms (for modals, AJAX, etc.)
const observer = new MutationObserver((mutations) => {
    const imageTypeSelect = document.querySelector('select[name*="image_type"]');
    if (imageTypeSelect && !imageTypeSelect.dataset.fieldVisibilityInitialized) {
        imageTypeSelect.dataset.fieldVisibilityInitialized = 'true';
        initializeFieldVisibility();
    }
});

observer.observe(document.body, {
    childList: true,
    subtree: true,
});