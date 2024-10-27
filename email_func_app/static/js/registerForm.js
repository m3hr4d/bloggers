document.addEventListener('DOMContentLoaded', function() {
    function toggleFields() {
        var userType = document.getElementById('user_type').value;
        var businessFields = document.getElementById('business-fields');
        var influencerFields = document.getElementById('influencer-fields');
        var avatarLabel = document.getElementById('avatar_label');

        businessFields.style.display = 'none';
        influencerFields.style.display = 'none';
        avatarLabel.classList.remove('required');

        if (userType === 'business') {
            businessFields.style.display = 'block';
        } else if (userType === 'influencer') {
            influencerFields.style.display = 'block';
            avatarLabel.classList.add('required');
        }
    }

    // Initial call to set the correct fields on page load
    toggleFields();

    // Change event to toggle fields when user_type changes
    document.getElementById('user_type').addEventListener('change', toggleFields);
});
