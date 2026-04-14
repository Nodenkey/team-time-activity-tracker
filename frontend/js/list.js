(function () {
  const filtersForm = document.getElementById("filters-form");
  const clearBtn = document.getElementById("clear-filters");
  const loadingEl = document.getElementById("entries-loading");
  const emptyEl = document.getElementById("entries-empty");
  const errorEl = document.getElementById("entries-error");
  const filtersErrorEl = document.getElementById("filters-error");
  const tableWrapper = document.getElementById("entries-table-wrapper");
  const tbody = document.getElementById("entries-tbody");

  if (!filtersForm || !tbody) return;

  function setLoading(isLoading) {
    loadingEl.hidden = !isLoading;
  }

  function clearMessages() {
    emptyEl.hidden = true;
    errorEl.hidden = true;
    filtersErrorEl.hidden = true;
  }

  function renderEntries(entries) {
    tbody.innerHTML = "";

    if (!entries || entries.length === 0) {
      tableWrapper.hidden = true;
      emptyEl.hidden = false;
      return;
    }

    tableWrapper.hidden = false;
    emptyEl.hidden = true;

    for (const entry of entries) {
      const tr = document.createElement("tr");

      const dateTd = document.createElement("td");
      dateTd.textContent = entry.date || "";
      tr.appendChild(dateTd);

      const personTd = document.createElement("td");
      personTd.textContent = entry.person || "";
      tr.appendChild(personTd);

      const teamTd = document.createElement("td");
      teamTd.textContent = entry.team || "";
      tr.appendChild(teamTd);

      const activityTd = document.createElement("td");
      activityTd.textContent = entry.activity || "";
      tr.appendChild(activityTd);

      const durationTd = document.createElement("td");
      durationTd.textContent = String(entry.duration_minutes ?? "");
      tr.appendChild(durationTd);

      tbody.appendChild(tr);
    }
  }

  async function fetchEntries(params) {
    const search = new URLSearchParams();
    if (params?.date) search.set("date", params.date);
    if (params?.person) search.set("person", params.person);

    const url = search.toString()
      ? `${window.API_BASE_URL}/entries?${search.toString()}`
      : `${window.API_BASE_URL}/entries`;

    setLoading(true);
    clearMessages();

    try {
      const res = await fetch(url);
      const maybeJson = await res.json().catch(() => null);

      if (!res.ok) {
        if (res.status === 400 && maybeJson && maybeJson.error === "invalid_date") {
          filtersErrorEl.textContent = maybeJson.message || "Invalid date filter.";
          filtersErrorEl.hidden = false;
        } else {
          errorEl.textContent =
            maybeJson && maybeJson.message
              ? `Failed to load entries: ${maybeJson.message}`
              : "Failed to load entries. Please try again.";
          errorEl.hidden = false;
        }
        tableWrapper.hidden = true;
        return;
      }

      renderEntries(Array.isArray(maybeJson) ? maybeJson : []);
    } catch (err) {
      console.error(err);
      errorEl.textContent = "Network error while loading entries. Please try again.";
      errorEl.hidden = false;
      tableWrapper.hidden = true;
    } finally {
      setLoading(false);
    }
  }

  filtersForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(filtersForm);
    const date = formData.get("date");
    const person = String(formData.get("person") || "").trim();

    fetchEntries({
      date: date || undefined,
      person: person || undefined,
    });
  });

  clearBtn.addEventListener("click", function () {
    filtersForm.reset();
    fetchEntries();
  });

  // Initial load
  fetchEntries();
})();
