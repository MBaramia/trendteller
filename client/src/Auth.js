export function setUpAuth() {
  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: "username@email.com",
      password: "password123",
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
    })
    .catch((error) => {
      console.log(error);
    });
}
