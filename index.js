// home-page-animation
window.onload = function () {
  setTimeout(() => {
    document.querySelector('.split-container').classList.add('hidden');
    setTimeout(() => {
      document.querySelector('.split-container').style.display = 'none';
      document.getElementById('loginAsPage').style.display = 'flex';
    }, 2000);
  }, 1000);
};

// loginAs-page
document.getElementById('adminBtn').addEventListener('click', () => loginAs('Admin'));
document.getElementById('facultyBtn').addEventListener('click', () => loginAs('Faculty'));

// loginAs-page Redirect to respective pages
function loginAs(userType) {
  if (userType === 'Admin') {
    window.location.href = 'admin-login.html'; 
  } else if (userType === 'Faculty') {
    window.location.href = 'faculty-login.html'; 
}
}


// login-page-setup
function validateForm() {
  const phone = document.getElementById('phone').value;
  const password = document.getElementById('password').value;

  if (!/^\d{10}$/.test(phone)) {
    alert('Please enter a valid 10-digit phone number.');
    return false;
  }

  if (password.length < 6) {
    alert('Password must be at least 6 characters long.');
    return false;
  }

  return true;
}

                                                                                                              