/* Dashboard client: the ApexCharts engagement bar + sortable commitments table.
   Both are progressive enhancements over server-rendered HTML. */

(function () {
  "use strict";

  const ACCENT = "#2A77EA";
  const INK_MUTED = "#4E5160";
  const LINE = "#E6E6E8";

  /* ---- KPI #2: engagement bar chart -------------------------------------- */

  function renderChart() {
    const el = document.getElementById("chart");
    const dataEl = document.getElementById("chart-data");
    if (!el || !dataEl || typeof ApexCharts === "undefined") return;

    const { labels, counts } = JSON.parse(dataEl.textContent);
    // Explicit integer headroom: keeps a uniform column (e.g. all learners at 1)
    // off the exact axis max, which otherwise renders degenerately. Counts are
    // small (0–5), so one tick per unit stays clean.
    const yMax = Math.max(1, ...counts) + 1;

    const options = {
      chart: {
        type: "bar",
        height: 300,
        fontFamily: "inherit",
        toolbar: { show: false },
        animations: { enabled: false },
      },
      series: [{ name: "Check-ins", data: counts }],
      colors: [ACCENT],
      plotOptions: {
        bar: {
          columnWidth: "52%",
          borderRadius: 4,
          borderRadiusApplication: "end",
          dataLabels: { position: "top" },
        },
      },
      legend: { show: false }, // single series — the card title names it
      dataLabels: {
        enabled: true,
        offsetY: -18,
        formatter: (v) => (v > 0 ? v : ""),
        style: { fontSize: "12px", fontWeight: 600, colors: [INK_MUTED] },
      },
      grid: {
        borderColor: LINE,
        strokeDashArray: 3,
        xaxis: { lines: { show: false } },
        yaxis: { lines: { show: true } },
        padding: { top: 0, right: 4, bottom: 0, left: 4 },
      },
      xaxis: {
        categories: labels,
        axisBorder: { show: false },
        axisTicks: { show: false },
        labels: {
          rotate: -32,
          rotateAlways: labels.length > 4,
          hideOverlappingLabels: false,
          trim: true,
          style: { fontSize: "11.5px", colors: INK_MUTED },
        },
      },
      yaxis: {
        min: 0,
        max: yMax,
        tickAmount: yMax,
        labels: {
          formatter: (v) => Math.round(v),
          style: { fontSize: "11.5px", colors: INK_MUTED },
        },
      },
      states: { hover: { filter: { type: "darken", value: 0.9 } } },
      tooltip: {
        custom: ({ dataPointIndex }) => {
          const name = labels[dataPointIndex];
          const n = counts[dataPointIndex];
          return (
            '<div style="padding:9px 12px;font-family:inherit;">' +
            '<div style="font-weight:600;margin-bottom:2px;">' + name + "</div>" +
            '<div style="font-size:12px;color:#4E5160;">' +
            n + " check-in" + (n === 1 ? "" : "s") +
            "</div></div>"
          );
        },
      },
    };

    new ApexCharts(el, options).render();
  }

  /* ---- KPI #3: sortable table -------------------------------------------- */

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

  renderChart();
  makeSortable();
})();
