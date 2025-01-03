document.addEventListener('DOMContentLoaded', function () {
  const errors = document.querySelector('.alert-danger');
  if (errors) {
    errors.scrollIntoView({ behavior: 'smooth' });
  }


  document.getElementById('toggle-password').addEventListener('click', function () {
    var passwordInput = document.getElementById('password');
    if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      this.classList.remove('glyphicon-eye-open');
      this.classList.add('glyphicon-eye-close');
    } else {
      passwordInput.type = 'password';
      this.classList.remove('glyphicon-eye-close');
      this.classList.add('glyphicon-eye-open');
    }
  });


  document.getElementById('toggle-password2').addEventListener('click', function () {
    var passwordInput2 = document.getElementById('password2');
    if (passwordInput2.type === 'password') {
      passwordInput2.type = 'text';
      this.classList.remove('glyphicon-eye-open');
      this.classList.add('glyphicon-eye-close');
    } else {
      passwordInput2.type = 'password';
      this.classList.remove('glyphicon-eye-close');
      this.classList.add('glyphicon-eye-open');
    }
  });
});