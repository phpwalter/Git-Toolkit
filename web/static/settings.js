const settingsButton = document.getElementById('settings-button');
const settingsModal = document.getElementById('settings-modal');
const closeSettingsModal = document.getElementById('close-settings-modal');

settingsButton.addEventListener('click', (event) => {
    event.stopPropagation();
    settingsModal.classList.add('show');
});

closeSettingsModal.addEventListener('click', () => {
    settingsModal.classList.remove('show');
});

document.addEventListener('click', (event) => {
    if (settingsModal.classList.contains('show') && !settingsModal.contains(event.target) && !settingsButton.contains(event.target)) {
        settingsModal.classList.remove('show');
    }
});
