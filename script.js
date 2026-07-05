const copyButtons = document.querySelectorAll("[data-copy-target]");

copyButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    const targetId = button.getAttribute("data-copy-target");
    const target = document.getElementById(targetId);
    if (!target) return;

    const text = target.innerText.trim();

    try {
      await navigator.clipboard.writeText(text);
      const originalText = button.textContent;
      button.textContent = "Copied";
      button.classList.add("copied");

      window.setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove("copied");
      }, 1800);
    } catch (error) {
      button.textContent = "Select text";
      button.classList.add("copied");
    }
  });
});
