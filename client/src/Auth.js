import io from "socket.io-client";

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

export function getNoOfNotifications() {
  let status = true;
  return fetch("/getNoOfNotifications", {
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
      console.log("No of Notifications")
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

export function searchCompanies(query) {
  let status = true;
  return fetch("/searchCompanies", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: query,
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
      console.log("Search Companies")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getRecommendedCompanies() {
  let status = true;
  return fetch("/getRecommendedCompanies", {
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
      console.log("Recommended companies")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getStockData(companyID) {
  let status = true;
  return fetch("/getStockData", {
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
      console.log("Stock Data")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getPredictedStockData(companyID) {
  let status = true;
  return fetch("/getPredictedStockData", {
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
      console.log("Predicted Stock Data")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getMainStockData(companyID) {
  let status = true;
  return fetch("/getMainStockData", {
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
      console.log("Main Stock Data")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getStockChanges(companyID) {
  let status = true;
  return fetch("/getStockChanges", {
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
      console.log("Stock Changes")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getStockDates(companyID) {
  let status = true;
  return fetch("/getStockDates", {
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
      console.log("Stock Dates")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getPredictedStockDates(companyID) {
  let status = true;
  return fetch("/getPredictedStockDates", {
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
      console.log("Predicted Stock Dates")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function processToggleFollowing(companyID) {
  let status = true;
  return fetch("/toggleFollowing", {
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
      console.log("Follow toggled")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export function getCompanyAnalysis(companyID) {
  let status = true;
  return fetch("/getCompanyAnalysis", {
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
      console.log("Company Analysis")
      console.log(data);
      return {
        status: status,
        data: data,
      };
    });
}

export const setUpSocketListener = (callback) => {
  const socket = io("http://127.0.0.1:5001", { withCredentials: true });
  socket.on("database_updated", (data) => {
    console.log(data);
    callback();
  });

  return () => socket.disconnect();
}
