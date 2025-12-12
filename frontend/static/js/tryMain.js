document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    // Store selected values
    const selections = {
        major: null,
        softSkillsRating: null,
        technicalSkills: null,
        softSkills: null,
        careerInterest: null
    };
    
    dropdowns.forEach(dropdown => {
        const btn = dropdown.querySelector('.dropdown-btn');
        const content = dropdown.querySelector('.dropdown-content');
        const links = dropdown.querySelectorAll('.dropdown-content a');
        const field = btn.getAttribute('data-field');
        
        // Toggle dropdown on button click
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Close other dropdowns
            dropdowns.forEach(other => {
                if (other !== dropdown) {
                    other.classList.remove('active');
                }
            });
            
            // Toggle current dropdown
            dropdown.classList.toggle('active');
        });
        
        // Update button text when an item is selected
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const value = this.getAttribute('data-value');
                btn.textContent = this.textContent;
                btn.classList.remove('error');
                dropdown.classList.remove('active');
                
                // Store the selected value
                selections[field] = value;
            });
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    });

    // Get rating inputs
    const softSkillsRatingInput = document.getElementById('softSkillsRating');

    // Check if rating inputs exist
    if (softSkillsRatingInput) {
        // Store rating values

        softSkillsRatingInput.addEventListener('input', function() {
            selections.softSkillsRating = this.value;
        });
    }

    // ---------------------------------------
    // SUBMIT AND GET PREDICTION FROM BACKEND
    // ---------------------------------------

    const submitBtn = document.querySelector('.submit-btn');
    const resultPanel = document.getElementById('resultPanel');

    if (submitBtn && resultPanel && softSkillsRatingInput) {
        submitBtn.addEventListener('click', async function() {
            let valid = true;

            if (!softSkillsRatingInput.value || softSkillsRatingInput.value < 1 || softSkillsRatingInput.value > 10) {
                valid = false;
                softSkillsRatingInput.style.borderColor = '#ff3b3b';
                softSkillsRatingInput.style.background = 'rgba(255, 59, 59, 0.2)';
            } else {
                softSkillsRatingInput.style.borderColor = '#ff7200';
                softSkillsRatingInput.style.background = 'rgba(255, 255, 255, 0.1)';
            }

            // Validate dropdowns
            document.querySelectorAll('.dropdown-btn').forEach(btn => {
                let value = btn.textContent.trim();

                if (value.startsWith("Select")) {
                    valid = false;
                    btn.classList.add('error');
                }
            });

            if (!valid) {
                alert("Please complete all fields before getting prediction!");
                return;
            }

            // Prepare request data with exact column names that match the trained model
            const requestData = {
                "SoftSkillsRating": parseInt(softSkillsRatingInput.value),
                "Major": selections.major,
                "Technical Skills": selections.technicalSkills,
                "Soft Skills": selections.softSkills,
                "Career Interest": selections.careerInterest
            };

            console.log("Sending data:", requestData);

            // Disable button and show loading
            submitBtn.disabled = true;
            submitBtn.textContent = "Analyzing...";
            resultPanel.style.display = "none";

            try {
                // Send POST request to Flask backend
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData)
                });

                const data = await response.json();

                if (data.success) {
                    // Show successful prediction
                    resultPanel.className = "result-panel success";
                    resultPanel.style.display = "block";
                    resultPanel.innerHTML = `
                        <h2 style="color: #4ade80; margin-bottom: 15px;">🎯 Career Prediction Results</h2>
                        <p style="font-size: 1.2em; margin-bottom: 10px;">
                            <strong>Recommended Career Path:</strong>
                        </p>
                        <p style="font-size: 1.5em; color: #4ade80; font-weight: bold; margin-bottom: 20px;">
                            ${data.prediction}
                        </p>
                        <hr style="border: 1px solid rgba(255, 255, 255, 0.3); margin: 20px 0;">
                        <p style="margin-top: 15px; font-size: 0.95em; color: rgba(255, 255, 255, 0.8);">
                            Based on your soft skills (${softRatingInput.value}/10), 
                            and technical expertise in ${selections.technicalSkills}.
                        </p>
                    `;
                } else {
                    // Show error
                    resultPanel.className = "result-panel error";
                    resultPanel.style.display = "block";
                    resultPanel.innerHTML = `
                        <h2 style="color: #ff3b3b; margin-bottom: 15px;">❌ Error</h2>
                        <p>${data.error || 'An error occurred while processing your request.'}</p>
                    `;
                }

            } catch (error) {
                console.error('Error:', error);
                resultPanel.className = "result-panel error";
                resultPanel.style.display = "block";
                resultPanel.innerHTML = `
                    <h2 style="color: #ff3b3b; margin-bottom: 15px;">❌ Connection Error</h2>
                    <p>Could not connect to the server. Please make sure the Flask backend is running.</p>
                    <p style="margin-top: 10px; font-size: 0.9em; color: rgba(255, 255, 255, 0.7);">
                        Error details: ${error.message}
                    </p>
                `;
            } finally {
                // Re-enable button
                submitBtn.disabled = false;
                submitBtn.textContent = "Get Career Prediction";
            }
        });
    }
});