export function processLogin(username, password) {
  let status = true;
  return fetch("/processLogin", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        status = false;
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function processLogout() {
  let status = true;
  return fetch("/processLogout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        status = false;
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function checkLoggedIn() {
  let status = true;
  return fetch("/checkLoggedIn", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      console.log(response);
      if (!response.ok) {
        return false;
      } else {
        return true;
      }
    });
}
