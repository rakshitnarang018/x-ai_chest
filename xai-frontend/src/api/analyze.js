export async function analyzeImage(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Backend error: " + response.statusText);
    }

    return await response.json();
}
