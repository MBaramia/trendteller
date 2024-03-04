export function processRegister(username, password) {
  let status = true;
  return fetch("/processRegister", {
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

export function processUpdate(username, password) {
  let status = true;
  return fetch("/processUpdate", {
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
        return {
          status: false,
          data: {"message": "Error"},
        };
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

export function getUserData() {
  let status = true;
  return fetch("/getUserData", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        return {
          status: false,
          data: {"message": "Error"},
        };
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

export function getFollowedCompanies() {
  let status = true;
  return fetch("/getFollowedCompanies", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        return {
          status: false,
          data: {"message": "Error"},
        };
      }
      return response.json();
    })
    .then((data) => {
      console.log("Followed companies")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getAllNews() {
  let status = true;
  return fetch("/getAllNews", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        return {
          status: false,
          data: {"message": "Error"},
        };
      }
      return response.json();
    })
    .then((data) => {
      console.log("All news")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getAllCompanies() {
  let status = true;
  return fetch("/getAllCompanies", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        return {
          status: false,
          data: {"message": "Error"},
        };
      }
      return response.json();
    })
    .then((data) => {
      console.log("All companies")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getNotifications() {
  let status = true;
  return fetch("/getNotifications", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        return {
          status: false,
          data: {"message": "Error"},
        };
      }
      return response.json();
    })
    .then((data) => {
      console.log("Notifications")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getCompanyInfo(companyID) {
  let status = true;
  return fetch("/getCompanyInfo", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      companyID: companyID,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        return {
          status: false,
          data: {"message": "Error"},
        };
      }
      return response.json();
    })
    .then((data) => {
      console.log("Company Info")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getCompanyNews(companyID) {
  let status = true;
  return fetch("/getCompanyNews", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      companyID: companyID,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        return {
          status: false,
          data: {"message": "Error"},
        };
      }
      return response.json();
    })
    .then((data) => {
      console.log("Company News")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getArticleInfo(articleID, companyID) {
  let status = true;
  return fetch("/getArticleInfo", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      articleID: articleID,
      companyID: companyID,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        return {
          status: false,
          data: {"message": "Error"},
        };
      }
      return response.json();
    })
    .then((data) => {
      console.log("Article Info")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}
