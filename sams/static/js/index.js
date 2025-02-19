// HOME PAGE ANIMATION
window.onload = function () {
  setTimeout(() => {
    document.querySelector(".split-container").classList.add("hidden");
    setTimeout(() => {
      document.querySelector(".split-container").style.display = "none";
      document.getElementById("loginAsPage").style.display = "flex";
    }, 2000);
  }, 1000);
};

document.addEventListener("DOMContentLoaded", () => {
  // CANCEL BTN OF POPUPS
  const cancelBtns = document.querySelectorAll(".cancel-btn");
  // ADMIN PROFILE PAGE
  const profileContainer = document.querySelector(".profile-container");
  const profileEditBtn = document.querySelector(".profile-edit-btn");
  const profileEditPopupBox = document.querySelector(".profile-edit-popup-box");
  const passwordChangeBtn = document.querySelector(".password-change-btn");
  const passwordChangePopupBox = document.querySelector(
    ".password-change-popup-box"
  );
  // TEACHERS PAGE
  const teachersListContainer = document.querySelector(
    ".teachers-list-container"
  );
  const addNewTeacherBtn = document.querySelector(".add-new-teacher-btn");
  const addNewTeacherContainer = document.querySelector(
    ".add-new-teacher-container"
  );
  // BATCHES PAGE
  const batchesListContainer = document.querySelector(
    ".batches-list-container"
  );
  const addNewBatchBtn = document.querySelector(".add-new-batch-btn");
  const addNewBatchContainer = document.querySelector(
    ".add-new-batch-container"
  );
  // COURSES PAGE
  const coursesListContainer = document.querySelector(
    ".courses-list-container"
  );
  const addNewCourseBtn = document.querySelector(".add-new-course-btn");
  const addNewCourseContainer = document.querySelector(
    ".add-new-course-container"
  );
  // SECTIONS PAGE
  const sectionsListContainer = document.querySelector(
    ".sections-list-container"
  );
  const addNewSectionBtn = document.querySelector(".add-new-section-btn");
  const addNewSectionContainer = document.querySelector(
    ".add-new-section-container"
  );
  // SUBJECTS PAGE
  const subjectsListContainer = document.querySelector(
    ".subjects-list-container"
  );
  const addNewSubjectBtn = document.querySelector(".add-new-subject-btn");
  const addNewSubjectContainer = document.querySelector(
    ".add-new-subject-container"
  );
  // STUDENTS PAGE
  const studentsListContainer = document.querySelector(
    ".students-list-container"
  );
  const addNewStudentBtn = document.querySelector(".add-new-student-btn");
  const addNewStudentContainer = document.querySelector(
    ".add-new-student-container"
  );

  // ADMIN PROFILE PAGE
  if (profileEditBtn) {
    profileEditBtn.addEventListener("click", () => {
      profileContainer.style.display = "none";
      profileEditPopupBox.style.display = "flex";
      profileEditPopupBox.style.animation = "popupGrow 0.3s forwards";
    });
  }

  if (passwordChangeBtn) {
    passwordChangeBtn.addEventListener("click", () => {
      profileContainer.style.display = "none";
      passwordChangePopupBox.style.display = "flex";
      passwordChangePopupBox.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // TEACHERS PAGE
  if (addNewTeacherBtn) {
    addNewTeacherBtn.addEventListener("click", () => {
      teachersListContainer.style.display = "none";
      addNewTeacherContainer.style.display = "flex";
      addNewTeacherContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // BATCHES PAGE
  if (addNewBatchBtn) {
    addNewBatchBtn.addEventListener("click", () => {
      batchesListContainer.style.display = "none";
      addNewBatchContainer.style.display = "flex";
      addNewBatchContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // COURSES PAGE
  if (addNewCourseBtn) {
    addNewCourseBtn.addEventListener("click", () => {
      coursesListContainer.style.display = "none";
      addNewCourseContainer.style.display = "flex";
      addNewCourseContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // SECTIONS PAGE
  if (addNewSectionBtn) {
    addNewSectionBtn.addEventListener("click", () => {
      sectionsListContainer.style.display = "none";
      addNewSectionContainer.style.display = "flex";
      addNewSectionContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // SUBJECTS PAGE
  if (addNewSubjectBtn) {
    addNewSubjectBtn.addEventListener("click", () => {
      subjectsListContainer.style.display = "none";
      addNewSubjectContainer.style.display = "flex";
      addNewSubjectContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // STUDENTS PAGE
  if (addNewStudentBtn) {
    addNewStudentBtn.addEventListener("click", () => {
      studentsListContainer.style.display = "none";
      addNewStudentContainer.style.display = "flex";
      addNewStudentContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // CANCEL BTN OF POPUPS
  if (cancelBtns) {
     cancelBtns.forEach((btn) => {
      btn.addEventListener("click", (event) => {
        event.preventDefault();
      
      // Hide all popups
        if (profileEditPopupBox) profileEditPopupBox.style.display = "none";
        if (passwordChangePopupBox) passwordChangePopupBox.style.display = "none";
        if (addNewTeacherContainer) addNewTeacherContainer.style.display = "none";
        if (addNewBatchContainer) addNewBatchContainer.style.display = "none";
        if (addNewCourseContainer) addNewCourseContainer.style.display = "none";
        if (addNewSectionContainer) addNewSectionContainer.style.display = "none";
        if (addNewSubjectContainer) addNewSubjectContainer.style.display = "none";
        if (addNewStudentContainer) addNewStudentContainer.style.display = "none";

      // Restore the main section (Show previous container)
        if (profileContainer) profileContainer.style.display = "block";
        if (teachersListContainer) teachersListContainer.style.display = "block";
        if (batchesListContainer) batchesListContainer.style.display = "block";
        if (coursesListContainer) coursesListContainer.style.display = "block";
        if (sectionsListContainer) sectionsListContainer.style.display = "block";
        if (subjectsListContainer) subjectsListContainer.style.display = "block";
        if (studentsListContainer) studentsListContainer.style.display = "block";
     });
   });
 }
}); 

  // PASSWORD TOGGLE FUNCTIONALITY
  document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', function() {
        var passwordField = this.previousElementSibling;
        if (passwordField && passwordField.type) { 
            var icon = this.querySelector('i');
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordField.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        }
    });
});


//MAIL SENDING.... 
document.getElementById("password-reset-form").addEventListener("submit", function(event) {
  let btn = document.querySelector("button[type='submit']");
  btn.disabled = true;
  btn.innerText = "Sending...";
  
  let loadingMsg = document.getElementById("loading-message");
  if (loadingMsg) {
      loadingMsg.style.display = "block";
  }
});

