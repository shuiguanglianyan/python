const { API_BASE_URL, WECHAT_SCHEDULER_KEY, USE_REMOTE_API } = require('../config');

function request(path, method = 'GET', data = {}) {
  if (!USE_REMOTE_API) {
    return Promise.resolve({ code: 0, data: null, msg: '本地模式未启用远程 API' });
  }

  return new Promise((resolve, reject) => {
    wx.request({
      url: `${API_BASE_URL}${path}`,
      method,
      data,
      header: {
        'content-type': 'application/json',
        'x-wechat-scheduler-key': WECHAT_SCHEDULER_KEY
      },
      success(res) {
        resolve(res.data);
      },
      fail(err) {
        reject(err);
      }
    });
  });
}

module.exports = {
  request
};
