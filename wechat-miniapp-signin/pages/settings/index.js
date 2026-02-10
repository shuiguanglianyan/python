const config = require('../../config');

Page({
  data: {
    profile: {
      nickname: '',
      phone: ''
    },
    keyPreview: ''
  },

  onShow() {
    const app = getApp();
    const profile = app.globalData.profile;
    const key = config.WECHAT_SCHEDULER_KEY || '';

    this.setData({
      profile,
      keyPreview: key.length > 8 ? `${key.slice(0, 4)}****${key.slice(-4)}` : key || '未配置'
    });
  },

  onNicknameInput(e) {
    this.setData({ 'profile.nickname': e.detail.value });
  },

  onPhoneInput(e) {
    this.setData({ 'profile.phone': e.detail.value });
  },

  onSaveProfile() {
    const app = getApp();
    app.globalData.profile = this.data.profile;
    wx.setStorageSync('profile', this.data.profile);
    wx.showToast({ title: '保存成功', icon: 'success' });
  },

  onCopyGuide() {
    const guide =
      '请打开项目根目录 config.js，替换 WECHAT_SCHEDULER_KEY 为你的微信调度 key。';
    wx.setClipboardData({ data: guide });
  }
});
