const container = document.getElementById('searchContainer');
const input = document.getElementById('searchInput');
const trigger = document.getElementById('searchTrigger');
const clearBtn = document.getElementById('clearBtn');

trigger.addEventListener('click', (e) => {
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

clearBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    input.value = '';
    input.focus();
});

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const query = input.value.trim();
        if (query.length > 0) {
            console.log("Searching for:", query);
            alert("Searching: " + query);
        }
    }
});

document.addEventListener('click', (event) => {
    if (!container.contains(event.target) && container.classList.contains('active')) {
        container.classList.remove('active');
        input.value = '';
    }
});
