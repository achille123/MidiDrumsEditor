const canvas = document.getElementById("stars-bg");
const ctx = canvas.getContext("2d");

let stars = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

function createStars(count) {
  stars = [];
  for (let i = 0; i < count; i++) {
    stars.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 1.4 + 0.5,
      alpha: Math.random(),
      speed: Math.random() * 0.002 + 0.005
    });
  }
}
createStars(150);

function animateStars() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  stars.forEach(star => {
    star.alpha += star.speed;
    if (star.alpha >= 1 || star.alpha <= 0) star.speed = -star.speed;

    ctx.beginPath();
    ctx.arc(star.x, star.y, star.radius, 0, 2 * Math.PI);
    ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
    ctx.fill();
  });

  requestAnimationFrame(animateStars);
}
animateStars();
