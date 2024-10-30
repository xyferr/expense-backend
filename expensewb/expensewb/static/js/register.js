const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector('.invalid_feedback');
const submitBtn = document.querySelector('.submit-btn');



usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display = 'none';

    
    // Only send the request if the username is not empty
    if (usernameVal.length > 0) {
        fetch("/auth/validate-username/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Ensure the server knows this is JSON
                // If you need a CSRF token, include it like this
                // 'X-CSRFToken': csrftoken  // Assuming csrftoken is defined somewhere
            },
            body: JSON.stringify({
                username: usernameVal
            })
        })
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            console.log('data', data);
            if(data.username_error) {
                submitBtn.setAttribute('disabled', true);
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = 'block';
                feedbackArea.innerHTML = `<p> ${data.username_error} </p>`;

                // document.querySelector('.username-error').innerHTML = data.username_error;
            }else{
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display = 'none';

    
    // Only send the request if the username is not empty
    if (emailVal.length > 0) {
        fetch("/auth/validate-email/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Ensure the server knows this is JSON
                // If you need a CSRF token, include it like this
                // 'X-CSRFToken': csrftoken  // Assuming csrftoken is defined somewhere
            },
            body: JSON.stringify({
                email: emailVal
            })
        })
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            console.log('data', data);
            if(data.email_error) {
                submitBtn.ATTRIBUTE_NODE('disabled', true);
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display = 'block';
                emailFeedbackArea.innerHTML = `<p> ${data.email_error} </p>`;

                // document.querySelector('.username-error').innerHTML = data.username_error;
            }else{
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});

