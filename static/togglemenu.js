document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.friends-group-title').forEach(title => {
    title.addEventListener('click', () => {
      let group = title.closest('.friends-group');
      let list = group.querySelector('.friends-list');
      list.style.display = list.style.display === 'none' ? 'block' : 'none';
      title.querySelector('i').classList.toggle('bx-chevron-up', list.style.display === 'block');
      title.querySelector('i').classList.toggle('bx-chevron-down', list.style.display === 'none');
    });
  });
});


// toggle button voor news
document.addEventListener("DOMContentLoaded", function() {
  var toggleBtn = document.getElementById("toggle-news-button");
  var gameTab = document.getElementById("game-tab");

  toggleBtn.addEventListener("click", function() {
    gameTab.classList.toggle("hidden");

    // Update button text based on the state
    toggleBtn.textContent = gameTab.classList.contains("hidden") ? "⮞" : "⮜";
  });
});
