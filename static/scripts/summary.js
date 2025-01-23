async function fetchStreamedResponse() {
    const query = document.getElementById('searchInput').value.trim();
    const response = await fetch(`/api/k-summary?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    const url = data.link;
    console.log(url);
    const contentDiv = document.querySelector('#summaryContent'); 

    try {
        const response = await fetch(url);
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let buffer = ''; // Buffer to accumulate content

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');

            lines.forEach(line => {
                if (line.startsWith('data:')) {
                    const data = line.replace('data:', '').trim();
                    if (data !== '[DONE]') {
                        const jsonData = JSON.parse(data);
                        if (jsonData.choices && jsonData.choices[0].delta.content) {
                            // Append the content to the buffer
                            buffer += jsonData.choices[0].delta.content;

                            // Update the content div with the buffer
                            if(contentDiv) {
                                contentDiv.textContent = buffer;
                                contentDiv.scrollTop = contentDiv.scrollHeight;
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error fetching streamed response:', error);
    }
}

fetchStreamedResponse();