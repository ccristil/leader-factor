/* Dashboard client: the sortable commitments table. A progressive enhancement
   over the server-rendered HTML — rows arrive pre-sorted worst-first from the
   template, and clicking a header just re-sorts what's already there. */

(function () {
  "use strict";

  function makeSortable() {
    const table = document.getElementById("commitments");
    if (!table) return;
    const headers = table.querySelectorAll("thead th.sortable");
    const tbody = table.tBodies[0];

    headers.forEach((th, colIndex) => {
      th.addEventListener("click", () => {
        const numeric = th.dataset.type === "num";
        const asc = th.dataset.dir !== "asc"; // toggle

        headers.forEach((h) => delete h.dataset.dir);
        th.dataset.dir = asc ? "asc" : "desc";

        const rows = Array.from(tbody.rows);
        rows.sort((a, b) => {
          const av = cellValue(a.cells[colIndex], numeric);
          const bv = cellValue(b.cells[colIndex], numeric);
          if (av < bv) return asc ? -1 : 1;
          if (av > bv) return asc ? 1 : -1;
          return 0;
        });
        rows.forEach((r) => tbody.appendChild(r));
      });
    });
  }

  function cellValue(cell, numeric) {
    const raw = cell.dataset.sort !== undefined ? cell.dataset.sort : cell.textContent;
    return numeric ? parseFloat(raw) || 0 : raw.trim().toLowerCase();
  }

  makeSortable();
})();
