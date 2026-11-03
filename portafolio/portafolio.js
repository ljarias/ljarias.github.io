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
  const sections = Array.from(document.querySelectorAll(".catalog-section[data-section]"));
  const cards = Array.from(document.querySelectorAll(".catalog-card[data-state]"));
  if (!controls || !input || !result || !empty || !clear || !buttons.length || !cards.length) return;

  const normalize = (value) => value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("es")
    .trim();

  let active = "todos";
  const update = () => {
    const query = normalize(input.value);
    let visible = 0;
    for (const card of cards) {
      const matchesStatus = active === "todos" || card.dataset.state === active;
      const matchesText = !query || normalize(card.textContent).includes(query);
      const show = matchesStatus && matchesText;
      card.hidden = !show;
      if (show) visible += 1;
    }
    for (const section of sections) {
      section.hidden = !Array.from(section.querySelectorAll(".catalog-card")).some((card) => !card.hidden);
    }
    for (const button of buttons) {
      button.setAttribute("aria-pressed", String(button.dataset.filter === active));
    }
    result.textContent = visible === 1 ? "1 proyecto encontrado" : visible + " proyectos encontrados";
    empty.hidden = visible > 0;
    clear.hidden = !query && active === "todos";
  };

  for (const button of buttons) {
    button.addEventListener("click", () => {
      active = button.dataset.filter;
      update();
    });
  }
  input.addEventListener("input", update);
  clear.addEventListener("click", () => {
    input.value = "";
    active = "todos";
    update();
    input.focus();
  });
  controls.hidden = false;
  update();
})();
