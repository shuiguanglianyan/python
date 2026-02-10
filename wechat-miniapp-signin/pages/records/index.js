const { getRecords, clearRecords } = require('../../utils/storage');

Page({
  data: {
    records: []
  },

  onShow() {
    this.setData({ records: getRecords() });
  },

  onClearRecords() {
    wx.showModal({
      title: '确认清空',
      content: '将删除所有本地签到记录，是否继续？',
      success: (res) => {
        if (res.confirm) {
          clearRecords();
          this.setData({ records: [] });
          wx.showToast({ title: '已清空', icon: 'success' });
        }
      }
    });
  }
});
