function initUserProfileModal() {
    const userAvatar = document.getElementById('user-avatar') as HTMLImageElement;
    const userProfileModal = document.getElementById('user-profile-modal') as HTMLDivElement;

    userAvatar.addEventListener('click', (event: MouseEvent) => {
        event.stopPropagation();
        const rect = userAvatar.getBoundingClientRect();
        
        // Calculate horizontal position: top right corner of modal sits in the middle of the gravatar
        const modalLeft = rect.left + (rect.width / 2) - userProfileModal.offsetWidth;
        userProfileModal.style.left = `${modalLeft}px`;

        // Calculate vertical position: top right corner of modal sits in the middle of the gravatar
        const modalTop = rect.top + (rect.height / 2);
        userProfileModal.style.top = `${modalTop}px`;

        userProfileModal.classList.toggle('show');
    });

    document.addEventListener('click', (event: MouseEvent) => {
        if (userProfileModal && !userProfileModal.contains(event.target as Node) && !userAvatar.contains(event.target as Node)) {
            userProfileModal.classList.remove('show');
        }
    });
}
