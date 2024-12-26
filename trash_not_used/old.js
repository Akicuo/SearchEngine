document.addEventListener('DOMContentLoaded', function() {
    const responseElement = document.getElementById('response');
    const username = encodeURIComponent("{{ session['username'] }}");
    const password = encodeURIComponent("{{ session['uuid'] }}");
    const query = encodeURIComponent("{{ search_query }}");

    /**
     *
     * @param {HTMLElement} responseElement
     * @returns {number} 
     */
    function createLoadingAnimation(responseElement) {
        const loadingChars = ['-', '/', '|', '\\'];
        let charIndex = 0;

        const loadingInterval = setInterval(() => {
            responseElement.innerHTML = loadingChars[charIndex];
            charIndex = (charIndex + 1) % loadingChars.length;
        }, 100);

        return loadingInterval;
    }


    async function fetchResponse() {
   
        responseElement.innerHTML = '';

       
        const loadingInterval = createLoadingAnimation(responseElement);

        try {
            const response = await fetch(`/api/response?username=${username}&arg_uuid=${password}&query=${query}`, {
                method: 'GET',
                headers: {
                    'Accept': 'text/event-stream',
                },
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let done = false;
            let fullText = "";

            while (!done) {
                const { value, done: doneReading } = await reader.read();
                done = doneReading;

                if (value) {
                    const text = decoder.decode(value, { stream: true });
                    fullText += text;
                }
            }

           
            clearInterval(loadingInterval);

            
            typeWriter(fullText.trim());


        } catch (error) {
            console.error('Error fetching response:', error);
            responseElement.innerHTML = 'An error occurred while fetching the response.';
            clearInterval(loadingInterval);
        }
    }
    function convertToBoldHyperlink(text) {
        const regex = /\[(\d+)\]\[(https?:\/\/[^\]]+)\]/g;
        return text.replace(regex, '<b><a class="blue-text" href="$2">$1</a></b>');
}

    /**
     * 
     * @param {string} text
     */
     function typeWriter(text) {

        const processedTextv1 = text.replace(/\n/g, '<br>');
        const processedText = processedTextv1.replace("* ", '➣ ');
        
        responseElement.innerHTML = ''; 
        let i = 0;
        const typingSpeed = 1; 

        function type() {
            if (i < processedText.length) {
                // Check if the current substring is a <br> tag
                if (processedText.substr(i, 4) === '<br>') {
                    responseElement.innerHTML += '<br>';
                    i += 4;
                } else {
                    responseElement.innerHTML += processedText.charAt(i);
                    responseElement.innerHTML = convertToBoldHyperlink(responseElement.innerHTML)
                    responseElement.innerHTML = responseElement.innerHTML.replace("* ", '➣ ');
                    i++;

                }
                
                const randomSpeed = typingSpeed + Math.random() * 10;
                setTimeout(type, randomSpeed);
            } else {
                document.getElementById("StartCTButton").classList.toggle("display-none");
                document.getElementById("StartCTButton").style.display = "block";
                responseElement.innerHTML = convertToBoldHyperlink(responseElement.innerHTML);
                
            }
        }

        type();
    }


    fetchResponse();
});