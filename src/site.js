// Reality series site: solid nav after the hero, current-app highlight, screenshot lightbox.
(() => {
  const nav = document.getElementById("nav");
  const hero = document.querySelector(".hero");
  const minis = [...document.querySelectorAll(".mini a")];

  // nav turns solid once the dark hero has scrolled away
  new IntersectionObserver(([e]) => nav.classList.toggle("solid", !e.isIntersecting), {
    rootMargin: `-${nav.offsetHeight}px 0px 0px 0px`,
  }).observe(hero);

  // highlight the app whose section is in view
  const apps = [...document.querySelectorAll("section.app")];
  const seen = new Map();
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => seen.set(e.target.dataset.app, e.isIntersecting ? e.intersectionRatio : 0));
    let best = null, ratio = 0;
    seen.forEach((r, k) => { if (r > ratio) { ratio = r; best = k; } });
    minis.forEach((a) => a.classList.toggle("on", a.dataset.app === best));
    const on = minis.find((a) => a.dataset.app === best);
    if (on) on.scrollIntoView({ block: "nearest", inline: "nearest" });
  }, { threshold: [0, .15, .3, .5, .7], rootMargin: "-40% 0px -40% 0px" });
  apps.forEach((s) => io.observe(s));

  // lightbox: every screenshot of one app, in order
  const box = document.getElementById("lightbox");
  const img = box.querySelector("img"), cap = box.querySelector("figcaption");
  let list = [], at = 0;
  const show = (i) => {
    at = (i + list.length) % list.length;
    const b = list[at], im = b.querySelector("img");
    img.src = im.dataset.full;   // the full-resolution crop
    img.alt = im.alt;
    cap.textContent = im.alt;
  };
  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("button.zoom");
    if (!b) return;
    const app = b.closest("section.app");
    list = [...app.querySelectorAll("button.zoom")];
    show(list.indexOf(b));
    box.showModal();
  });
  box.querySelector(".lb-close").addEventListener("click", () => box.close());
  box.querySelector(".lb-prev").addEventListener("click", () => show(at - 1));
  box.querySelector(".lb-next").addEventListener("click", () => show(at + 1));
  box.addEventListener("click", (ev) => { if (ev.target === box) box.close(); });
  box.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowLeft") show(at - 1);
    if (ev.key === "ArrowRight") show(at + 1);
  });
})();
