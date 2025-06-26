function getCourseRecommendations() {
    const question = document.getElementById('question').value;
    if (!question) return;

    const recommendationsSection = document.getElementById('recommendations-section');
    const recommendationsDiv = document.getElementById('recommendations');
    const resultsDiv = document.getElementById('results');

    recommendationsDiv.innerHTML = '<div class="text-center text-gray-600">Loading recommendations...</div>';
    resultsDiv.classList.remove('hidden');
    recommendationsSection.classList.remove('hidden');

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
    })
    .then(response => response.json())
    .then(data => {
        recommendationsDiv.innerHTML = '';
        data.forEach(course => {
            const card = document.createElement('div');
            card.className = 'course-card bg-gray-50 p-4 rounded-lg border border-gray-200';
            card.innerHTML = `
                <h3 class="font-bold text-lg text-indigo-600 mb-2">${course.Module}</h3>
                <p class="text-gray-600 mb-2">${course.Course_Learning_Material}</p>
                <div class="flex justify-between items-center">
                    <span class="bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full text-sm">
                        ${course.Course_Level}
                    </span>
                    <span class="text-gray-500 text-sm">${course.Duration}</span>
                </div>
                <div class="mt-4">
                    <a href="${course.Links}" target="_blank" 
                       class="text-indigo-600 hover:text-indigo-800 text-sm font-medium">
                        View Course →
                    </a>
                </div>
            `;
            recommendationsDiv.appendChild(card);
        });
    })
    .catch(error => {
        recommendationsDiv.innerHTML = '<div class="text-red-600">Error fetching recommendations</div>';
    });
}

function getQA() {
    const question = document.getElementById('question').value;
    if (!question) return;

    const answerSection = document.getElementById('answer-section');
    const qaResult = document.getElementById('qa-result');
    const resultsDiv = document.getElementById('results');

    qaResult.textContent = 'Loading answer...';
    resultsDiv.classList.remove('hidden');
    answerSection.classList.remove('hidden');

    fetch('/qa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
    })
    .then(response => response.json())
    .then(data => {
        qaResult.textContent = data.answer;
    })
    .catch(error => {
        qaResult.innerHTML = '<span class="text-red-600">Error fetching answer</span>';
    });
}

// Add event listener for Enter key
document.getElementById('question').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        getCourseRecommendations();
    }
});
