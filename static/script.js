document.addEventListener('DOMContentLoaded', () => {
    // Set default analysis date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('analysis_date').value = today;

    const form = document.getElementById('analysis-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.analysts = formData.getAll('analysts');

        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'block';

        const progressDiv = document.getElementById('progress');
        const messagesDiv = document.getElementById('messages');
        const reportDiv = document.getElementById('report');

        progressDiv.innerHTML = 'Starting analysis...';
        messagesDiv.innerHTML = '';
        reportDiv.innerHTML = '';

        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.body) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');

            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    break;
                }

                const chunk = decoder.decode(value);
                const lines = chunk.split('\\n');

                for (const line of lines) {
                    if (line.startsWith('data:')) {
                        const eventData = JSON.parse(line.substring(5));
                        if (eventData.type === 'progress') {
                            progressDiv.innerHTML = eventData.message;
                        } else if (eventData.type === 'message') {
                            messagesDiv.innerHTML += `<p>${eventData.message}</p>`;
                        } else if (eventData.type === 'report') {
                            reportDiv.innerHTML += `<div>${eventData.message}</div>`;
                        }
                    }
                }
            }
        }
    });
});
