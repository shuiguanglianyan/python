App({
  globalData: {
    userInfo: null,
    openid: '',
    profile: {
      nickname: '',
      phone: ''
    }
  },

  onLaunch() {
    const profile = wx.getStorageSync('profile') || { nickname: '', phone: '' };
    this.globalData.profile = profile;
  }
});
