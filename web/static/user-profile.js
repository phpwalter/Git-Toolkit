const userAvatar = document.getElementById('user-avatar');
const userProfileModal = document.getElementById('user-profile-modal');

userAvatar.addEventListener('click', (event) => {
    event.stopPropagation();
    const rect = userAvatar.getBoundingClientRect();
    userProfileModal.style.top = `${rect.bottom - 3}px`;
    userProfileModal.style.left = `${rect.left - userProfileModal.offsetWidth + (rect.width / 2)}px`;
    userProfileModal.classList.toggle('show');
});

document.addEventListener('click', (event) => {
    if (!userProfileModal.contains(event.target) && !userAvatar.contains(event.target)) {
        userProfileModal.classList.remove('show');
    }
});
