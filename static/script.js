let home = document.getElementById("home");

home.addEventListener("mouseover", function () {
  document.getElementsByClassName("hr-line")[0].className = "hr-line active";
});
home.addEventListener("mouseout", function () {
  document.getElementsByClassName("hr-line")[0].className = "hr-line";
});
let main = document.getElementById("main");
const loginRequest = (path, params, method = "post") => {
  const form = document.createElement("form");
  form.method = method;
  form.action = path;
  const UsernameField = document.createElement("input");
  UsernameField.type = "hidden";
  UsernameField.name = "username";
  UsernameField.value = params["username"];
  form.appendChild(UsernameField);
  const PasswordField = document.createElement("input");
  PasswordField.type = "hidden";
  PasswordField.name = "password";
  PasswordField.value = params["password"];

  form.appendChild(PasswordField);
  document.body.appendChild(form);
  form.submit();
};
let logButton = document.getElementsByClassName("logButton")[0];
const loginContainer = () => {
  if (document.getElementsByClassName("container-box")[0]) {
    document.getElementsByClassName("container-box")[0].remove();
  }
  let containerBox = document.createElement("div");
  containerBox.classList.add("container-box");
  containerBox.innerHTML = `
    <div class="login-box-container">
    <span class="error">Wrong username and password</span>
        <div class="username-container">
            <input type="text" name="username" id="username" placeholder=" ">
            <div class="placeholder-text">
                <span>Username</span>
            </div>
        </div>
        <div class="password-container">
            <input type="password" name="password" id="password" placeholder=" ">
            <div class="placeholder-text">
                <span>Password</span>
            </div>
        </div>
        <div class="login-button-container">
            <input type="button" value="Login" id="login-button">
        </div>
        <div class="register-switch-container">
            <a>New here? Create an account</a>
        </div>
    </div>`;
  main.appendChild(containerBox);
  document
    .getElementsByClassName("register-switch-container")[0]
    .addEventListener("click", signupContainer);
  document.addEventListener("click", function (e) {
    if (e.target.classList.contains("container-box")) {
      if (e.target.classList.contains("login-box-container") == false) {
        document.getElementsByClassName("container-box")[0].style.display =
          "none";
      }
    }
  });
  //   let jsonData = {
  //     username: document.getElementById("username").value,
  //     password: document.getElementById("password").value,
  //   };
  document
    .getElementById("login-button")
    .addEventListener("click", function () {
      let jsonData = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
      };
      fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data) {
            if (data["status"] == "success") {
              window.location = "/user";
            } else {
              document.getElementsByClassName("error")[0].style.visibility =
                "visible";
            }
          }
        });
      //   loginRequest("/login", jsonData);
    });

  //       fetch("/login", {
  //         method: "POST",
  //         headers: {
  //           "Content-Type": "application/json",
  //         },
  //         body: JSON.stringify(jsonData),
  //       })
  //         .then((response) => response.json())
  //         .then((data) => {
  //           console.log("Success: ", data);
  //         })
  //         .catch((error) => {
  //           console.error("Error:", error);
  //         });
  //     });
};
if (logButton) {
  logButton.addEventListener("click", loginContainer);
}

const signupContainer = () => {
  if (main.contains(document.getElementsByClassName("container-box")[0])) {
    document.getElementsByClassName("container-box")[0].remove();
  }
  //   if (document.getElementsByClassName("container-box")[0]) {
  //   }
  let containerBox = document.createElement("div");
  containerBox.classList.add("container-box");

  //   let containerBox = document.getElementsByClassName("container-box")[0];
  containerBox.innerHTML = ` 
    <div class="signup-box-container">
    <span class="error">Somethin went wrong.</span>
        <div class="fullname-container">
            <input type="text" name="fullname" id="fullname" placeholder=" ">
            <div class="placeholder-text">
                <span>Fullname</span>
            </div>
        </div>
        <div class="email-container">
            <input type="email" name="email" id="email" placeholder=" ">
            <div class="placeholder-text">
                <span>Email</span>
            </div>
        </div>
        <div class="password-container">
            <input type="password" name="password" id="password" placeholder=" ">
            <div class="placeholder-text">
                <span>Password</span>
            </div>
        </div>
        <div class="signup-button-container">
            <input type="button" value="Create an account" id="signup-submit">
        </div>
        <div class="login-switch-container">
            <a>Already have a account? Login</a>
        </div>
    </div>`;
  main.appendChild(containerBox);
  document
    .getElementsByClassName("login-switch-container")[0]
    .addEventListener("click", loginContainer);
  document
    .getElementById("signup-submit")
    .addEventListener("click", function () {
      let jsonData = {
        fullname: document.getElementById("fullname").value,
        username: document.getElementById("email").value,
        password: document.getElementById("password").value,
      };
      fetch("/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] == "success") {
            let error = document.getElementsByClassName("error")[0];
            error.style.backgroundColor = "green";
            error.style.visibility = "visible";
            error.innerHTML = "Account created successfully";
            setTimeout(function () {
              document.getElementsByClassName("container-box")[0].remove();
            }, 600);
          } else {
            let error = document.getElementsByClassName("error")[0];
            error.style.visibility = "visible";
          }
        });
    });
};
let logoutButton = document.getElementsByClassName("logoutButton")[0];
logoutButton.addEventListener("click", function () {
  const form = document.createElement("form");
  form.action = "/logout";
  form.method = "POST";
  document.body.appendChild(form);
  form.submit();
});
