document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('reminderModal');
    const span = document.getElementsByClassName('close')[0];
    const selectedDateSpan = document.getElementById('selectedDate');
    const dateInput = document.getElementById('dateInput');

    // Open modal when a calendar day is clicked
    document.querySelectorAll('.calendar-day').forEach(day => {
        day.addEventListener('click', () => {
            const date = day.dataset.date;
            selectedDateSpan.textContent = date;
            dateInput.value = date;
            modal.style.display = 'block';
        });
    });

    // Close the modal
    span.onclick = () => {
        modal.style.display = 'none';
    };

    // Close the modal if clicked outside
    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    // Handle form submission
    document.getElementById('reminderForm').addEventListener('submit', (event) => {
        event.preventDefault();
        // Add your AJAX or form submission logic here
        modal.style.display = 'none';
    });
});




function openAddReminderForm() {
    document.getElementById("reminderModal").style.display = "block";
}

function closeAddReminderForm() {
    document.getElementById("reminderModal").style.display = "none";
}

function openDisplayReminderForm() {
    document.getElementById("displayModal").style.display = "block";
}

function closeDisplayReminderForm() {
    document.getElementById("displayModal").style.display = "none";
}
