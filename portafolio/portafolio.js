/* Arias Data Lab · filtros progresivos del portafolio público.
   No hace peticiones de red, no guarda búsquedas ni expone datos internos. */
(() => {
  "use strict";
  const controls = document.getElementById("portfolio-controls");
  const input = document.getElementById("portfolio-search");
  const result = document.getElementById("portfolio-results");
  const empty = document.getElementById("portfolio-empty");
  const clear = document.getElementById("portfolio-clear");
  const buttons = Array.from(document.querySelectorAll("[data-filter]"));
  const scopes = Array.from(document.querySelectorAll(".adl-scope-buttons button[data-scope]"));
  const scopeClear = document.getElementById("portfolio-scope-clear");
  const nature = document.getElementById("nature-filter");
  const access = document.getElementById("access-filter");
  const sections = Array.from(document.querySelectorAll(".catalog-section[data-section]"));
  const cards = Array.from(document.querySelectorAll(".catalog-card[data-state]"));
  if (!controls || !input || !result || !empty || !clear || !buttons.length || !cards.length) return;

  const normalize = (value) => value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("es")
    .trim();

  let active = "todos";
  let selectedScope = "todos";
  const update = () => {
    const query = normalize(input.value);
    let visible = 0;
    for (const card of cards) {
      const matchesStatus = active === "todos" || card.dataset.state === active;
      const matchesText = !query || normalize(card.textContent).includes(query);
      const matchesScope = selectedScope === "todos" || card.dataset.scope === selectedScope;
      const matchesNature = !nature || nature.value === "todos" || card.dataset.naturaleza === nature.value;
      const matchesAccess = !access || access.value === "todos" || card.dataset.acceso === access.value;
      const show = matchesStatus && matchesText && matchesScope && matchesNature && matchesAccess;
      card.hidden = !show;
      if (show) visible += 1;
    }
    for (const section of sections) {
      section.hidden = !Array.from(section.querySelectorAll(".catalog-card")).some((card) => !card.hidden);
    }
    for (const button of buttons) {
      button.setAttribute("aria-pressed", String(button.dataset.filter === active));
    }
    for (const button of scopes) button.setAttribute("aria-pressed", String(button.dataset.scope === selectedScope));
    if (scopeClear) scopeClear.hidden = selectedScope === "todos";
    result.textContent = visible === 1 ? "1 proyecto encontrado" : visible + " proyectos encontrados";
    empty.hidden = visible > 0;
    clear.hidden = !query && active === "todos" && selectedScope === "todos" && (!nature || nature.value === "todos") && (!access || access.value === "todos");
  };

  for (const button of buttons) {
    button.addEventListener("click", () => {
      active = button.dataset.filter;
      update();
    });
  }
  for (const button of scopes) button.addEventListener("click", () => {
    selectedScope = selectedScope === button.dataset.scope ? "todos" : button.dataset.scope;
    update();
    controls.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  if (scopeClear) scopeClear.addEventListener("click", () => { selectedScope = "todos"; update(); });
  input.addEventListener("input", update);
  if (nature) nature.addEventListener("change", update);
  if (access) access.addEventListener("change", update);
  clear.addEventListener("click", () => {
    input.value = "";
    active = "todos";
    selectedScope = "todos";
    if (nature) nature.value = "todos";
    if (access) access.value = "todos";
    update();
    input.focus();
  });
  controls.hidden = false;
  update();
})();
