// QCU interactif du guide (aucune IA, aucun serveur) : questions dans assets/quiz.json, score dans le navigateur.
(function () {
  var app = document.getElementById("quiz-app");
  if (!app) return;
  var L = app.getAttribute("data-lang") || "fr";
  var base = L === "en" ? "../" : "";
  var T = {
    fr: { all: "Tous les domaines", start: "Commencer", shuffle: "Ordre aléatoire", count: "Questions",
          score: "Score", answered: "répondues", reset: "Effacer mes réponses", verified: "✔ commande exécutée par scripts/verify-quiz.py",
          concept: "question conceptuelle : commande d'observation", cmd: "La commande", right: "Bonne réponse.",
          wrong: "Ce n'est pas la bonne réponse.", only: "Revoir seulement mes erreurs", domain: "Domaine" },
    en: { all: "All domains", start: "Start", shuffle: "Shuffle", count: "Questions",
          score: "Score", answered: "answered", reset: "Clear my answers", verified: "✔ command executed by scripts/verify-quiz.py",
          concept: "conceptual question: observation command", cmd: "The command", right: "Correct.",
          wrong: "That is not the right answer.", only: "Review my mistakes only", domain: "Domain" }
  }[L];
  var KEY = "ckad-quiz-" + L;
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { saved = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) {} }
  function txt(v) { return typeof v === "string" ? v : (v[L] || v.fr); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function md(s) { return esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>"); }

  fetch(base + "assets/quiz.json").then(function (r) { return r.json(); }).then(function (data) {
    var qs = data.questions, verified = data.verified || {};
    var bar = document.createElement("div"); bar.className = "qbar";
    var sel = document.createElement("select");
    sel.innerHTML = '<option value="">' + T.all + " (" + qs.length + ")</option>" + Object.keys(data.domains).map(function (d) {
      var n = qs.filter(function (q) { return q.domain === d; }).length;
      return '<option value="' + d + '">' + d + " · " + esc(txt(data.domains[d])) + " (" + n + ")</option>";
    }).join("");
    var shuf = document.createElement("label"); shuf.innerHTML = '<input type="checkbox"> ' + T.shuffle;
    var only = document.createElement("label"); only.innerHTML = '<input type="checkbox"> ' + T.only;
    var reset = document.createElement("button"); reset.textContent = T.reset;
    var score = document.createElement("span"); score.className = "score";
    bar.append(sel, shuf, only, reset, score);
    var list = document.createElement("div");
    app.append(bar, list);

    function updateScore(shown) {
      var a = 0, ok = 0;
      shown.forEach(function (q) { if (q.id in saved) { a++; if (saved[q.id] === q.answer) ok++; } });
      score.textContent = T.score + " : " + ok + " / " + a + " (" + a + "/" + shown.length + " " + T.answered + ")";
    }

    function render() {
      var shown = qs.filter(function (q) { return !sel.value || q.domain === sel.value; });
      if (only.querySelector("input").checked) shown = shown.filter(function (q) { return q.id in saved && saved[q.id] !== q.answer; });
      if (shuf.querySelector("input").checked) shown = shown.slice().sort(function () { return Math.random() - 0.5; });
      list.innerHTML = "";
      shown.forEach(function (q, i) {
        var box = document.createElement("div"); box.className = "q"; box.id = "q-" + q.id;
        box.innerHTML = '<div class="meta">' + T.domain + " " + q.domain + " · " + esc(txt(data.domains[q.domain])) + " · #" + (i + 1) + "</div>" +
          "<h3>" + md(txt(q.q)) + "</h3>";
        var btns = [];
        q.choices.forEach(function (c, k) {
          var b = document.createElement("button"); b.className = "choice";
          var label = txt(c);
          b.innerHTML = "<span>" + String.fromCharCode(65 + k) + ".</span> " + (typeof c === "string" ? "<code>" + esc(label) + "</code>" : md(label));
          b.addEventListener("click", function () { saved[q.id] = k; save(); show(); updateScore(shown); });
          box.appendChild(b); btns.push(b);
        });
        var ex = document.createElement("div"); ex.className = "expl"; ex.hidden = true; box.appendChild(ex);
        function show() {
          if (!(q.id in saved)) return;
          var k = saved[q.id];
          btns.forEach(function (b, j) { b.classList.toggle("ok", j === q.answer); b.classList.toggle("ko", j === k && k !== q.answer); });
          var v = verified[q.id] === "PASS" ? T.verified : T.concept;
          ex.hidden = false;
          ex.innerHTML = "<p><strong>" + (k === q.answer ? T.right : T.wrong) + "</strong> " + md(txt(q.why)) + "</p>" +
            "<p><strong>" + T.cmd + "</strong> <small>(" + v + ")</small></p><pre><code>" + esc(q.cmd) + "</code></pre>";
        }
        show();
        list.appendChild(box);
      });
      updateScore(shown);
    }
    [sel, shuf.querySelector("input"), only.querySelector("input")].forEach(function (el) { el.addEventListener("change", render); });
    reset.addEventListener("click", function () { saved = {}; save(); render(); });
    render();
  });
})();
