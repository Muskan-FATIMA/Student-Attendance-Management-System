// home-page-animation
window.onload = function () {
  setTimeout(() => {
    document.querySelector(".split-container").classList.add("hidden");
    setTimeout(() => {
      document.querySelector(".split-container").style.display = "none";
      document.getElementById("loginAsPage").style.display = "flex";
    }, 2000);
  }, 1000);
};

// loginAs-page
document
  .getElementById("adminBtn")
  .addEventListener("click", () => loginAs("Admin"));
document
  .getElementById("teacherBtn")
  .addEventListener("click", () => loginAs("Teacher"));

// loginAs-page Redirect to respective pages
function loginAs(userType) {
  if (userType === "Admin") {
    window.location.href = "admin-login.html";
  } else if (userType === "Teacher") {
    window.location.href = "teacher-login.html";
  }
}

// login-page-setup
function validateForm() {
  const phone = document.getElementById("phone").value;
  const password = document.getElementById("password").value;

  if (!/^\d{10}$/.test(phone)) {
    alert("Please enter a valid 10-digit phone number.");
    return false;
  }
  if (password.length < 6) {
    alert("Password must be at least 6 characters long.");
    return false;
  }
  return true;
}

document.addEventListener("DOMContentLoaded", () => {
  // cancel btn of popups
  const cancelBtn = document.querySelector(".cancel-btn");
  // admin profile page
  const profileContainer = document.querySelector(".profile-container");
  const profileEditBtn = document.querySelector(".profile-edit-btn");
  const profileEditPopupBox = document.querySelector(".profile-edit-popup-box");
  const passwordChangeBtn = document.querySelector(".password-change-btn");
  const passwordChangePopupBox = document.querySelector(
    ".password-change-popup-box"
  );
  // teachers page
  const teachersListContainer = document.querySelector(
    ".teachers-list-container"
  );
  const addNewTeacherBtn = document.querySelector(".add-new-teacher-btn");
  const addNewTeacherContainer = document.querySelector(
    ".add-new-teacher-container"
  );
  // batches page
  const batchesListContainer = document.querySelector(
    ".batches-list-container"
  );
  const addNewBatchBtn = document.querySelector(".add-new-batch-btn");
  const addNewBatchContainer = document.querySelector(
    ".add-new-batch-container"
  );
  // courses page
  const coursesListContainer = document.querySelector(
    ".courses-list-container"
  );
  const addNewCourseBtn = document.querySelector(".add-new-course-btn");
  const addNewCourseContainer = document.querySelector(
    ".add-new-course-container"
  );
  // sections page
  const sectionsListContainer = document.querySelector(
    ".sections-list-container"
  );
  const addNewSectionBtn = document.querySelector(".add-new-section-btn");
  const addNewSectionContainer = document.querySelector(
    ".add-new-section-container"
  );
  // students page
  const studentsListContainer = document.querySelector(
    ".students-list-container"
  );
  const addNewStudentBtn = document.querySelector(".add-new-student-btn");
  const addNewStudentContainer = document.querySelector(
    ".add-new-student-container"
  );

  // admin profile page
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

  // teachers page
  if (addNewTeacherBtn) {
    addNewTeacherBtn.addEventListener("click", () => {
      teachersListContainer.style.display = "none";
      addNewTeacherContainer.style.display = "flex";
      addNewTeacherContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // batches page
  if (addNewBatchBtn) {
    addNewBatchBtn.addEventListener("click", () => {
      batchesListContainer.style.display = "none";
      addNewBatchContainer.style.display = "flex";
      addNewBatchContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // courses page
  if (addNewCourseBtn) {
    addNewCourseBtn.addEventListener("click", () => {
      coursesListContainer.style.display = "none";
      addNewCourseContainer.style.display = "flex";
      addNewCourseContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // sections page
  if (addNewSectionBtn) {
    addNewSectionBtn.addEventListener("click", () => {
      sectionsListContainer.style.display = "none";
      addNewSectionContainer.style.display = "flex";
      addNewSectionContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // students page
  if (addNewStudentBtn) {
    addNewStudentBtn.addEventListener("click", () => {
      studentsListContainer.style.display = "none";
      addNewStudentContainer.style.display = "flex";
      addNewStudentContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  // cancel btn of popups
  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      if (profileEditPopupBox) profileEditPopupBox.style.display = "none";
      if (passwordChangePopupBox) passwordChangePopupBox.style.display = "none";
      if (addNewTeacherContainer) addNewTeacherContainer.style.display = "none";
      if (addNewBatchContainer) addNewBatchContainer.style.display = "none";
      if (addNewCourseContainer) addNewCourseContainer.style.display = "none";
      if (addNewSectionContainer) addNewSectionContainer.style.display = "none";
      if (addNewStudentContainer) addNewStudentContainer.style.display = "none";
    });
  }
});
