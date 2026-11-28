// Guide du labo CKAD : thème, barre de lecture, boutons Copier, coloration, menu mobile.
(function () {
  var root = document.documentElement;
  var EN = root.lang === "en";
  var T = { copy: EN ? "Copy" : "Copier", copied: EN ? "Copied" : "Copié" };
  try { var t = localStorage.getItem("ckad-theme"); if (t) root.setAttribute("data-theme", t); } catch (e) {}
  document.getElementById("theme").addEventListener("click", function () {
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("ckad-theme", next); } catch (e) {}
  });
  document.getElementById("menu").addEventListener("click", function () { document.body.classList.toggle("nav-open"); });

  var bar = document.getElementById("progress");
  function onScroll() {
    var h = document.documentElement.scrollHeight - innerHeight;
    bar.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + "%";
    var links = document.querySelectorAll("nav .toc a"), cur = null;
    links.forEach(function (a) {
      var el = document.getElementById(decodeURIComponent(a.hash.slice(1)));
      if (el && el.getBoundingClientRect().top < 120) cur = a;
    });
    links.forEach(function (a) { a.classList.toggle("active", a === cur); });
  }
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  document.querySelectorAll("pre").forEach(function (pre) {
    var code = pre.querySelector("code"); if (!code) return;
    if (pre.closest("#quiz-app")) return;
    if (!pre.classList.contains("terminal") && window.hljs) {
      if (/language-(yaml|bash|sh|text)/.test(code.className) || !/language-/.test(code.className)) {
        try { hljs.highlightElement(code); } catch (e) {}
      }
    }
    var b = document.createElement("button"); b.className = "copy"; b.textContent = T.copy;
    b.addEventListener("click", function () {
      var txt = code.innerText;
      if (pre.classList.contains("terminal")) txt = txt.split("\n")[0].replace(/^\$ /, "");  // seulement la commande
      navigator.clipboard.writeText(txt).then(function () { b.textContent = "Copié"; setTimeout(function () { b.textContent = T.copy; }, 1200); });
    });
    pre.appendChild(b);
  });
})();
