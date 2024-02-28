export function processLogin(username, password) {
  fetch("/processLogin", {
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
        throw new Error("Error logging in");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      return {
        status: true,
        data: data,
      };
    })
    .catch((error) => {
      console.log(error);
      return {
        status: false,
        data: error,
      };
    });
}
