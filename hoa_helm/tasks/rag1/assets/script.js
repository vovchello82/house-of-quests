async function postAndReload(contentElementId, targetElementId) {
    const inputElement = document.getElementById(contentElementId);
    const loader = document.getElementById("loader");
    const btnPost = document.getElementById("btnPost");

    if (loader) {
        loader.style.display = "block";
    }
    if (!inputElement) {
        console.error(`Element with ID '${targetElementId}' not found.`);
        return;
    }

    btnPost.disabled = true

    inputElement.disabled = true
    const jsonData = {
        "model": "phi3",
        "messages": [
            {
                "role": "user",
                "content": inputElement.value
            }
        ],
        "stream": false
    }

    try {
        //const url = "http://localhost:11434/api/chat";
        const url = "/{{ .Release.Namespace }}/{{ .Release.Name }}/ai/api/chat"
        const response = await fetch(url, {
            method: 'POST',
            mode: "cors",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData)
        });

        inputElement.disabled = false
        btnPost.disabled = false
        // Check if the response is OK
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const rawResponse = await response.text();
        const updatedContent = JSON.parse(rawResponse)['message']['content']

        // Update the target element with the new content
        const targetElement = document.getElementById(targetElementId);
        if (targetElement) {
            targetElement.innerHTML = updatedContent;
        } else {
            console.error(`Element with ID '${targetElementId}' not found.`);
        }
    } catch (error) {
        console.error('Error during the POST request or DOM update:', error);
    }

    if (loader) {
        loader.style.display = "none";
    }
}
