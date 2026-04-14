(function () {
  const healthEl = document.getElementById("health-status");
  if (!healthEl || !window.API_BASE_URL) return;

  fetch(`${window.API_BASE_URL}/health`)
    .then((res) => {
      if (!res.ok) throw new Error("Healthcheck failed");
      return res.json();
    })
    .then((data) => {
      if (data && data.status === "ok") {
        healthEl.textContent = "OK";
        healthEl.classList.remove("status-pill--unknown", "status-pill--error");
        healthEl.classList.add("status-pill--ok");
      } else {
        throw new Error("Unexpected health payload");
      }
    })
    .catch(() => {
      healthEl.textContent = "Error";
      healthEl.classList.remove("status-pill--unknown", "status-pill--ok");
      healthEl.classList.add("status-pill--error");
    });
})();
