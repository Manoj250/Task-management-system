// Get references to the button and form
const toggleFormButton = document.getElementById('toggleFormButton');
const taskForm = document.getElementById('add_task_div');

// Hide the form initially
taskForm.style.display = 'none';

// Add click event listener to the button
toggleFormButton.addEventListener('click', function() {
    // Toggle the visibility of the form
    if (taskForm.style.display === 'none') {
        taskForm.style.display = 'block';
    } else {
        taskForm.style.display = 'none';
    }
});
