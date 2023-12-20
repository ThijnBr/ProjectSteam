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
