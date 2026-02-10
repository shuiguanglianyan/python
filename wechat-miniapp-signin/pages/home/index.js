const { addRecord } = require('../../utils/storage');
const { formatDateTime } = require('../../utils/date');
const { request } = require('../../utils/request');

Page({
  data: {
    studentName: '',
    remark: '',
    selectedCourse: '钢琴课',
    courses: ['钢琴课', '古筝课'],
    profile: {
      nickname: '',
      phone: ''
    }
  },

  onShow() {
    const app = getApp();
    this.setData({ profile: app.globalData.profile });
  },

  onStudentInput(e) {
    this.setData({ studentName: e.detail.value });
  },

  onRemarkInput(e) {
    this.setData({ remark: e.detail.value });
  },

  onCourseChange(e) {
    const idx = Number(e.detail.value);
    this.setData({ selectedCourse: this.data.courses[idx] });
  },

  async doSignIn() {
    if (!this.data.studentName.trim()) {
      wx.showToast({ title: '请先填写学员姓名', icon: 'none' });
      return;
    }

    const record = {
      id: Date.now().toString(),
      course: this.data.selectedCourse,
      studentName: this.data.studentName.trim(),
      remark: this.data.remark.trim(),
      createdAt: formatDateTime(),
      operator: this.data.profile.nickname || '未设置昵称'
    };

    addRecord(record);

    try {
      await request('/attendance/sign-in', 'POST', record);
    } catch (error) {
      wx.showToast({ title: '本地签到成功，远端同步失败', icon: 'none' });
      return;
    }

    wx.showToast({ title: '签到成功', icon: 'success' });
    this.setData({ remark: '' });
  }
});
