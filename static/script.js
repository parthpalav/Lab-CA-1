const form = document.getElementById("agentForm");
const responseText = document.getElementById("responseText");
const submitButton = form.querySelector("button");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const message = (formData.get("message") || "").toString().trim();
  const file = formData.get("file");

  if (!message && (!file || !file.name)) {
    responseText.textContent = "Please enter a query or upload a file.";
    return;
  }

  submitButton.disabled = true;
  responseText.textContent = "Thinking...";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      responseText.textContent = data.error || "Something went wrong.";
      return;
    }

    responseText.textContent = data.response || "No response from agent.";
  } catch (error) {
    responseText.textContent = "Request failed. Please try again.";
  } finally {
    submitButton.disabled = false;
  }
});
