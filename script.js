const copyButtons = document.querySelectorAll("[data-copy-target]");
const progressItems = document.querySelectorAll("[data-progress-item]");
const progressCount = document.querySelector("[data-progress-count]");

async function copyText(text) {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (error) {
      // Fall through to the textarea method for browsers that block clipboard access.
    }
  }

  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.setAttribute("readonly", "");
  textArea.style.position = "fixed";
  textArea.style.left = "-9999px";
  document.body.appendChild(textArea);
  textArea.select();

  const copied = document.execCommand("copy");
  textArea.remove();
  return copied;
}

function selectPromptText(target) {
  const selection = window.getSelection();
  const range = document.createRange();
  range.selectNodeContents(target);
  selection.removeAllRanges();
  selection.addRange(range);
}

copyButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    const targetId = button.getAttribute("data-copy-target");
    const target = document.getElementById(targetId);
    if (!target) return;

    const text = target.innerText.trim();

    try {
      const copied = await copyText(text);
      if (!copied) throw new Error("Copy command was not available.");

      const originalText = button.textContent;
      button.textContent = "Copied";
      button.classList.add("copied");

      window.setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove("copied");
      }, 1800);
    } catch (error) {
      selectPromptText(target);
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
