const container = document.getElementById('searchContainer') as HTMLDivElement;
const input = document.getElementById('searchInput') as HTMLInputElement;
const trigger = document.getElementById('searchTrigger') as HTMLButtonElement;
const clearBtn = document.getElementById('clearBtn') as HTMLButtonElement;

trigger.addEventListener('click', (e: MouseEvent) => {
    e.stopPropagation();
    const isActive = container.classList.contains('active');
    const query = input.value.trim();

    if (!isActive) {
        container.classList.add('active');
        setTimeout(() => input.focus(), 200);
    } else if (query.length > 0) {
        console.log("Searching for:", query);
        alert("Searching: " + query);
    }
});

clearBtn.addEventListener('click', (e: MouseEvent) => {
    e.stopPropagation();
    input.value = '';
    input.focus();
});

input.addEventListener('keydown', (e: KeyboardEvent) => {
    if (e.key === 'Enter') {
        const query = input.value.trim();
        if (query.length > 0) {
            console.log("Searching for:", query);
            alert("Searching: " + query);
        }
    }
});

document.addEventListener('click', (event: MouseEvent) => {
    if (!container.contains(event.target as Node) && container.classList.contains('active')) {
        container.classList.remove('active');
        input.value = '';
    }
});
