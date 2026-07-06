const copyButtons = document.querySelectorAll("[data-copy-target]");
const progressItems = document.querySelectorAll("[data-progress-item]");
const progressCount = document.querySelector("[data-progress-count]");

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

function updateProgressCount() {
  if (!progressCount || !progressItems.length) return;

  const completed = [...progressItems].filter((item) => item.checked).length;
  progressCount.textContent = `${completed} of ${progressItems.length} completed`;
}

progressItems.forEach((item) => {
  const key = `finance-lab:${item.getAttribute("data-progress-item")}`;
  item.checked = window.localStorage.getItem(key) === "true";

  item.addEventListener("change", () => {
    window.localStorage.setItem(key, item.checked ? "true" : "false");
    updateProgressCount();
  });
});

updateProgressCount();
