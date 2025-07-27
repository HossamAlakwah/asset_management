document.addEventListener('DOMContentLoaded', function () {
    const modelSelect = document.getElementById('id_model');
    const fieldInput = document.getElementById('id_field_name');

    if (!modelSelect || !fieldInput) return;

    // Convert input to select (if it's not already a select)
    let fieldSelect;
    if (fieldInput.tagName.toLowerCase() === 'input') {
        fieldSelect = document.createElement('select');
        fieldSelect.name = fieldInput.name;
        fieldSelect.id = fieldInput.id;
        fieldSelect.className = fieldInput.className;
        fieldInput.parentNode.replaceChild(fieldSelect, fieldInput);
    } else {
        fieldSelect = fieldInput;
    }

    modelSelect.addEventListener('change', function () {
        const modelPath = modelSelect.options[modelSelect.selectedIndex].text.trim();


        fetch(`/assets/report-fields/?model_path=${encodeURIComponent(modelPath)}`)
            .then(response => response.json())
            .then(data => {
                fieldSelect.innerHTML = ''; // clear old options

                if (data.fields && data.fields.length) {
                    const defaultOption = document.createElement('option');
                    defaultOption.textContent = '---------';
                    defaultOption.value = '';
                    fieldSelect.appendChild(defaultOption);

                    data.fields.forEach(field => {
                        const option = document.createElement('option');
                        option.value = field.name;
                        option.textContent = field.verbose_name;
                        fieldSelect.appendChild(option);
                    });
                } else {
                    const option = document.createElement('option');
                    option.textContent = 'No fields found';
                    option.disabled = true;
                    fieldSelect.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Error loading fields:', error);
            });
    });

    // Optionally auto-trigger on load
    if (modelSelect.value) {
        modelSelect.dispatchEvent(new Event('change'));
    }
});
