const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const count = document.getElementById("count");
const submitBtn = document.getElementById("submitBtn");
const result = document.getElementById("result");
const loading = document.getElementById("loading");
const status = document.getElementById("status");
const copyBtn = document.getElementById("copyBtn");
const quizControls = document.getElementById("quizControls");

const endpoints = {
  qa: "/qa",
  explain: "/explain",
  quiz: "/quiz",
  summarize: "/summarize",
  learn: "/learn/recommendations",
};

function updateQuizVisibility() {
  quizControls.classList.toggle("visible", task.value === "quiz");
}

task.addEventListener("change", updateQuizVisibility);
updateQuizVisibility();

async function checkHealth() {
  try {
    const response = await fetch("/health");
    const data = await response.json();
    status.textContent = data.demo_mode ? "Demo mode" : "Backend ready";
  } catch {
    status.textContent = "Backend unavailable";
  }
}

function renderQuiz(questions) {
  result.innerHTML = questions.map((item, index) => `
    <div class="quiz-question">
      <h3>${index + 1}. ${escapeHtml(item.question)}</h3>
      ${item.options.map((option) =>
        `<div class="quiz-option">${escapeHtml(option)}</div>`
      ).join("")}
      <p><strong>Answer:</strong> ${escapeHtml(item.correct_answer)}</p>
    </div>
  `).join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

submitBtn.addEventListener("click", async () => {
  const text = inputText.value.trim();
  if (!text) {
    result.textContent = "Please enter a question, topic or passage.";
    return;
  }

  const endpoint = endpoints[task.value];
  const payload = task.value === "quiz"
    ? { text, count: Number(count.value) }
    : { text };

  submitBtn.disabled = true;
  loading.classList.remove("hidden");
  result.textContent = "";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Request failed.");
    }

    if (task.value === "qa") result.textContent = data.answer;
    if (task.value === "explain") result.textContent = data.explanation;
    if (task.value === "summarize") result.textContent = data.summary;
    if (task.value === "learn") result.textContent = data.learning_path;
    if (task.value === "quiz") renderQuiz(data.quiz);
  } catch (error) {
    result.textContent = `Error: ${error.message}`;
  } finally {
    submitBtn.disabled = false;
    loading.classList.add("hidden");
  }
});

copyBtn.addEventListener("click", async () => {
  const text = result.innerText || result.textContent;
  try {
    await navigator.clipboard.writeText(text);
    copyBtn.textContent = "Copied";
    setTimeout(() => copyBtn.textContent = "Copy", 1200);
  } catch {
    copyBtn.textContent = "Copy failed";
    setTimeout(() => copyBtn.textContent = "Copy", 1200);
  }
});

checkHealth();
