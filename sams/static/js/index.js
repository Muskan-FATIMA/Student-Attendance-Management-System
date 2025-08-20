
document.addEventListener("DOMContentLoaded", function () {
  // PASSWORD TOGGLE FUNCTIONALITY
  document.querySelectorAll(".toggle-password").forEach((button) => {
    button.addEventListener("click", function () {
      var passwordField = this.previousElementSibling;
      if (passwordField && passwordField.type) {
        var icon = this.querySelector("i");
        if (passwordField.type === "password") {
          passwordField.type = "text";
          icon.classList.remove("fa-eye");
          icon.classList.add("fa-eye-slash");
        } else {
          passwordField.type = "password";
          icon.classList.remove("fa-eye-slash");
          icon.classList.add("fa-eye");
        }
      }
    });
  });


  // PASSWORD RESET MAIL
  const resetForm = document.getElementById("password-reset-form");
  if (resetForm) {
    resetForm.addEventListener("submit", function (event) {
      let btn = document.querySelector("button[type='submit']");
      btn.disabled = true;
      btn.innerText = "Sending...";

      let loadingMsg = document.getElementById("loading-message");
      if (loadingMsg) {
        loadingMsg.style.display = "block";
      }
    });
  }

  // POPUP & PAGE TOGGLE
  const cancelBtns = document.querySelectorAll(".cancel-btn");
  const profileContainer = document.querySelector(".profile-container");
  const profileEditBtn = document.querySelector(".profile-edit-btn");
  const profileEditPopupBox = document.querySelector(".profile-edit-popup-box");
  const passwordChangeBtn = document.querySelector(".password-change-btn");
  const passwordChangePopupBox = document.querySelector(".password-change-popup-box");
  const teachersListContainer = document.querySelector(".teachers-list-container");
  const addNewTeacherBtn = document.querySelector(".add-new-teacher-btn");
  const addNewTeacherContainer = document.querySelector(".add-new-teacher-container");
  const batchesListContainer = document.querySelector(".batches-list-container");
  const addNewBatchBtn = document.querySelector(".add-new-batch-btn");
  const addNewBatchContainer = document.querySelector(".add-new-batch-container");
  const coursesListContainer = document.querySelector(".courses-list-container");
  const addNewCourseBtn = document.querySelector(".add-new-course-btn");
  const addNewCourseContainer = document.querySelector(".add-new-course-container");
  const sectionsListContainer = document.querySelector(".sections-list-container");
  const addNewSectionBtn = document.querySelector(".add-new-section-btn");
  const addNewSectionContainer = document.querySelector(".add-new-section-container");
  const subjectsListContainer = document.querySelector(".subjects-list-container");
  const addNewSubjectBtn = document.querySelector(".add-new-subject-btn");
  const addNewSubjectContainer = document.querySelector(".add-new-subject-container");
  const studentsListContainer = document.querySelector(".students-list-container");
  const addNewStudentBtn = document.querySelector(".add-new-student-btn");
  const addNewStudentContainer = document.querySelector(".add-new-student-container");

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

  if (addNewTeacherBtn) {
    addNewTeacherBtn.addEventListener("click", () => {
      teachersListContainer.style.display = "none";
      addNewTeacherContainer.style.display = "flex";
      addNewTeacherContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  if (addNewBatchBtn) {
    addNewBatchBtn.addEventListener("click", () => {
      batchesListContainer.style.display = "none";
      addNewBatchContainer.style.display = "flex";
      addNewBatchContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  if (addNewCourseBtn) {
    addNewCourseBtn.addEventListener("click", () => {
      coursesListContainer.style.display = "none";
      addNewCourseContainer.style.display = "flex";
      addNewCourseContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  if (addNewSectionBtn) {
    addNewSectionBtn.addEventListener("click", () => {
      sectionsListContainer.style.display = "none";
      addNewSectionContainer.style.display = "flex";
      addNewSectionContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  if (addNewSubjectBtn) {
    addNewSubjectBtn.addEventListener("click", () => {
      subjectsListContainer.style.display = "none";
      addNewSubjectContainer.style.display = "flex";
      addNewSubjectContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  if (addNewStudentBtn) {
    addNewStudentBtn.addEventListener("click", () => {
      studentsListContainer.style.display = "none";
      addNewStudentContainer.style.display = "flex";
      addNewStudentContainer.style.animation = "popupGrow 0.3s forwards";
    });
  }

  if (cancelBtns) {
    cancelBtns.forEach((btn) => {
      btn.addEventListener("click", (event) => {
        event.preventDefault();

        if (profileEditPopupBox) profileEditPopupBox.style.display = "none";
        if (passwordChangePopupBox) passwordChangePopupBox.style.display = "none";
        if (addNewTeacherContainer) addNewTeacherContainer.style.display = "none";
        if (addNewBatchContainer) addNewBatchContainer.style.display = "none";
        if (addNewCourseContainer) addNewCourseContainer.style.display = "none";
        if (addNewSectionContainer) addNewSectionContainer.style.display = "none";
        if (addNewSubjectContainer) addNewSubjectContainer.style.display = "none";
        if (addNewStudentContainer) addNewStudentContainer.style.display = "none";

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


  // HAMBURGER MENU
  const hamburger = document.getElementById("hamburger");
  const sidebar = document.getElementById("sidebar");
  const closeBtn = document.getElementById("closeBtn");

  if (hamburger && sidebar) {
    hamburger.addEventListener("click", function () {
      sidebar.classList.add("active");
      hamburger.style.display = "none"; 
    });
  }

  if (closeBtn && sidebar) {
    closeBtn.addEventListener("click", function () {
      sidebar.classList.remove("active");
       hamburger.style.display = "block"; 
    });
  }


  //MESSAGE DISAPPEAR FUNCTIONALITY
  const messages = document.querySelectorAll(".messages .message");

    if (messages.length > 0) {
        setTimeout(() => {
            messages.forEach(msg => {
                msg.style.transition = "opacity 0.5s ease";
                msg.style.opacity = "0";
                setTimeout(() => {
                    msg.style.display = "none";
                }, 500); 
            });
        }, 5000);
    }

 // FILTER TOGGLE FUNCTIONALITY
  const filterToggleBtn = document.getElementById("filterToggleBtn");
  const filterOptions = document.getElementById("filterOptions");

  if (localStorage.getItem("filterState") === "open") {
    filterOptions.classList.remove("hide");
    filterToggleBtn.innerHTML = `<i class="fa-solid fa-filter"></i> Hide Filters`;
  }

  if (filterToggleBtn && filterOptions) {
    filterToggleBtn.addEventListener("click", function(e) {
      e.preventDefault();

      filterOptions.classList.toggle("hide");
      if (filterOptions.classList.contains("hide")) {
        filterToggleBtn.innerHTML = `<i class="fa-solid fa-filter"></i> Show Filters`;
        localStorage.setItem("filterState", "closed"); 
      } else {
        filterToggleBtn.innerHTML = `<i class="fa-solid fa-filter"></i> Hide Filters`;
        localStorage.setItem("filterState", "open");  
      }
      
    });
  }
  const filterForm = document.querySelector("#filterForm");
if (filterForm) {
  const filterSelects = filterForm.querySelectorAll("select");

  filterSelects.forEach((select) => {
    select.addEventListener("change", function() {
      filterForm.submit();
    });
  });
}
});






