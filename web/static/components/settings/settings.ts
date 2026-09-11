function initSettingsModal() {
    const settingsButton = document.getElementById('settings-button') as HTMLButtonElement;
    const settingsModal = document.getElementById('settings-modal') as HTMLDivElement;
    const closeSettingsModal = document.getElementById('close-settings-modal') as HTMLButtonElement;

    settingsButton.addEventListener('click', (event: MouseEvent) => {
        event.stopPropagation();
        settingsModal.classList.add('show');
    });

    closeSettingsModal.addEventListener('click', () => {
        settingsModal.classList.remove('show');
    });

    document.addEventListener('click', (event: MouseEvent) => {
        if (settingsModal && settingsModal.classList.contains('show') && !settingsModal.contains(event.target as Node) && !settingsButton.contains(event.target as Node)) {
            settingsModal.classList.remove('show');
        }
    });
}
