import axios from "axios";
import {
  ElMessage
} from "element-plus";
import {
  getToken
} from "@/utils/auth";
import {
  Auth
} from 'aws-amplify';

axios.defaults.headers.post["Content-Type"] =
  "application/x-www-form-urlencoded";
axios.defaults.headers["X-Requested-With"] = "XMLHttpRequest"; 


window.HttpRequest = {
  /**
   * Get
   * @param url
   * @param params
   * @param isNeedFailback
   * @returns {Promise}
   */
  get(url, params, isNeedFailback) {
    axios.defaults.headers["Authorization"] = getToken();
    return new Promise((resolve, reject) => {
      axios
        .get(url, {
          params,
        })
        .then((response) => {
          if (!this.hook(response)) {
            if (isNeedFailback) {
              reject(response.data);
            } else {
              reject(response.data);
              return false;
            }
          }
          resolve(response.data);
        })
        .catch((error) => {
          if (error.response.status === 401) {
            // not log in 
            redirectToLogin();
          } else {
            ElMessage.error("service error!!!");
          }
          reject(error.response);
        });
    });
  },
  /**
   * Post
   * @param url
   * @param params
   * @param isNeedFailback return promise when response result > 0
   * @returns {Promise}
   */
  post(url, params, isNeedFailback) {
    axios.defaults.headers["Authorization"] = getToken();
    return new Promise((resolve, reject) => {
      axios
        .post(url, params)
        .then((response) => {
          if (!this.hook(response)) {
            if (isNeedFailback) {
              reject(response.data);
            } else {
              reject(response.data);
              return false;
            }
          }
          resolve(response.data);
        })
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            redirectToLogin();
          } else {
            ElMessage.error("service error!!!");
          }

          reject(error.response);
        });
    });
  },

  /**
   * http response
   * @param response
   * @returns {boolean}
   */
  hook(response) {
    if (response.data.error) {
      ElMessage.error("service error!!!");
      console.error(response.data.error);
      return false;
    }
    if (response.data.msg && response.data.msg.ElMessage) {
      ElMessage.error(response.data.msg.ElMessage);
      console.error(response.data.error);
      return false;
    }
    return true;
  },
};

function redirectToLogin() {
  Auth.signOut().then( () => {
    let url = `http://localhost:8080/`;
    location.href = url;
  });
}

/**
 * other methods
 */
(function () {
  let requestType = ["delete", "head", "options", "put", "patch"];
  for (let i = 0, len = requestType.length; i < len; i++) {
    let typeItem = requestType[i];
    HttpRequest[typeItem] = (url, params, isNeedFailback) => {
      axios.defaults.headers["Authorization"] = getToken();
      axios.defaults.headers[typeItem]["Content-Type"] =
        "application/x-www-form-urlencoded";
      return new Promise((resolve, reject) => {
        axios[typeItem](url, params)
          .then((response) => {
            if (!HttpRequest.hook(response)) {
              if (isNeedFailback) {
                reject(response.data);
              } else {
                reject(response.data);
                return false;
              }
            }
            resolve(response.data);
          })
          .catch((error) => {
            if (error.response.status === 401) {
              redirectToLogin();
            }
            reject(error.response);
          });
      });
    };
  }
})();
