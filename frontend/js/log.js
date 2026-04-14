(function () {
  const form = document.getElementById("time-entry-form");
  if (!form) return;

  const submitBtn = document.getElementById("submit-btn");
  const loadingEl = document.getElementById("form-loading");
  const successEl = document.getElementById("form-success");
  const errorEl = document.getElementById("form-error");

  function setFieldError(fieldName, message) {
    const errorNode = document.querySelector(
      `.field-error[data-error-for="${fieldName}"]`
    );
    if (errorNode) {
      errorNode.textContent = message || "";
    }
  }

  function clearFieldErrors() {
    document
      .querySelectorAll(".field-error")
      .forEach((el) => (el.textContent = ""));
  }

  function setSubmitting(isSubmitting) {
    if (isSubmitting) {
      submitBtn.disabled = true;
      loadingEl.hidden = false;
    } else {
      submitBtn.disabled = false;
      loadingEl.hidden = true;
    }
  }

  function showSuccess(message) {
    successEl.textContent = message;
    successEl.hidden = false;
    errorEl.hidden = true;
  }

  function showError(message) {
    errorEl.textContent = message;
    errorEl.hidden = false;
    successEl.hidden = true;
  }

  function validateForm(data) {
    let valid = true;
    clearFieldErrors();

    if (!data.date) {
      setFieldError("date", "Please select a date.");
      valid = false;
    }

    if (!data.person || !data.person.trim()) {
      setFieldError("person", "Please enter a person name.");
      valid = false;
    }

    if (!data.team || !data.team.trim()) {
      setFieldError("team", "Please enter a team name.");
      valid = false;
    }

    if (!data.activity || !data.activity.trim()) {
      setFieldError("activity", "Please describe the activity.");
      valid = false;
    }

    if (
      data.duration_minutes == null ||
      data.duration_minutes === "" ||
      Number.isNaN(Number(data.duration_minutes)) ||
      Number(data.duration_minutes) <= 0
    ) {
      setFieldError("duration_minutes", "Duration must be a positive number.");
      valid = false;
    }

    return valid;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(form);
    const payload = {
      date: formData.get("date"),
      person: String(formData.get("person") || "").trim(),
      team: String(formData.get("team") || "").trim(),
      activity: String(formData.get("activity") || "").trim(),
      duration_minutes: formData.get("duration_minutes"),
    };

    if (!validateForm(payload)) {
      showError("Please fix the highlighted fields and try again.");
      return;
    }

    payload.duration_minutes = Number(payload.duration_minutes);

    setSubmitting(true);
    successEl.hidden = true;
    errorEl.hidden = true;

    try {
      const res = await fetch(`${window.API_BASE_URL}/entries`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const maybeJson = await res.json().catch(() => null);

      if (!res.ok) {
        if (res.status === 422 && maybeJson && maybeJson.detail) {
          showError("Validation error from server. Please check your input.");
        } else {
          showError(
            maybeJson && maybeJson.message
              ? `Failed to save entry: ${maybeJson.message}`
              : "Failed to save entry. Please try again."
          );
        }
        return;
      }

      showSuccess("Entry saved successfully.");
      form.reset();
    } catch (err) {
      console.error(err);
      showError("Network error while saving entry. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  form.addEventListener("submit", handleSubmit);
})();
