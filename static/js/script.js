document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('span');
    const loader = document.getElementById('loader');
    
    const resultPlaceholder = document.getElementById('result-placeholder');
    const resultContent = document.getElementById('result-content');
    const priceAmount = document.getElementById('price-amount');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            btnText.classList.add('hidden');
            loader.classList.remove('hidden');
            submitBtn.disabled = true;
            
            try {
                if (!resultPlaceholder.classList.contains('hidden')) {
                    resultPlaceholder.style.opacity = '0';
                    setTimeout(() => {
                        resultPlaceholder.classList.add('hidden');
                        showResult();
                    }, 300);
                } else {
                    resultContent.style.opacity = '0';
                    setTimeout(() => {
                        showResult();
                    }, 300);
                }

                async function showResult() {
                    try {
                        const response = await fetch('/predict', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(data)
                        });
                        
                        const result = await response.json();
                        
                        if (response.ok) {
                            animateValue(priceAmount, 0, result.price, 1000);
                            
                            const wordsElement = document.getElementById('price-words');
                            if (wordsElement) {
                                wordsElement.style.opacity = '0';
                                wordsElement.innerText = result.price_words;
                                setTimeout(() => {
                                    wordsElement.style.opacity = '1';
                                }, 800);
                            }
                            
                            resultContent.classList.remove('hidden');
                            resultContent.style.opacity = '1';
                        } else {
                            alert(result.error || 'An error occurred during prediction.');
                            resultContent.classList.add('hidden');
                            resultPlaceholder.classList.remove('hidden');
                            resultPlaceholder.style.opacity = '1';
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Failed to connect to the server.');
                    } finally {
                        btnText.classList.remove('hidden');
                        loader.classList.add('hidden');
                        submitBtn.disabled = false;
                    }
                }
                
            } catch (error) {
                console.error('Error:', error);
                btnText.classList.remove('hidden');
                loader.classList.add('hidden');
                submitBtn.disabled = false;
            }
        });
    }
    
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            
            const easeProgress = 1 - Math.pow(1 - progress, 4);
            
            const currentVal = start + easeProgress * (end - start);
            
            obj.innerHTML = currentVal.toLocaleString('en-US', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            });
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                obj.innerHTML = end.toLocaleString('en-US', {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0
                });
            }
        };
        window.requestAnimationFrame(step);
    }
});
