import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { loginAPI, registerAPI, getMeAPI } from '../../apis/user';

export const fetchLogin = createAsyncThunk(
  'user/fetchLogin',
  async (loginForm, { rejectWithValue }) => {
    try {
      const res = await loginAPI(loginForm);
      // 登录接口返回格式: { code: 200, message: "登录成功", data: { user: {id, username, email}, access_token, refresh_token } }
      const { user, access_token } = res.data;
      return {
        token: access_token,
        username: user.username,
        id: user.id
      };
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || '登录失败');
    }
  }
);

export const fetchRegister = createAsyncThunk(
  'user/fetchRegister',
  async (registerForm, { rejectWithValue }) => {
    try {
      const res = await registerAPI(registerForm);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || '注册失败');
    }
  }
);

// 获取用户信息
export const fetchUserInfo = createAsyncThunk(
  'user/fetchUserInfo',
  async (_, { rejectWithValue }) => {
    try {
      const res = await getMeAPI();
      // 用户信息接口返回格式: { code: 200, data: { id, username, email, is_admin } }
      return res.data; // 返回用户信息，包括id和username
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || '获取用户信息失败');
    }
  }
);

// 定义 slice
const userSlice = createSlice({
  name: 'user',
  initialState: {
    username: '',
    userId: '', // 添加用户ID字段
    token: localStorage.getItem('token') || '', // 从localStorage恢复token
    isLoggedIn: !!localStorage.getItem('token'), // 根据token是否存在设置登录状态
    error: null,
    loading: false,
  },
  reducers: {
    logout(state) {
      state.token = '';
      state.isLoggedIn = false;
      state.username = '';
      state.userId = ''; // 清空用户ID
      state.error = null;
      // 清除localStorage中的token
      localStorage.removeItem('token');
    },
    clearError(state) {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchLogin.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLogin.fulfilled, (state, action) => {
        state.loading = false;
        state.token = action.payload.token;
        state.username = action.payload.username;
        state.userId = action.payload.id || ''; // 添加用户ID
        state.isLoggedIn = true;
        // 保存token到localStorage
        localStorage.setItem('token', action.payload.token);
      })
      .addCase(fetchLogin.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });

    builder
      .addCase(fetchRegister.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchRegister.fulfilled, (state, action) => {
        state.loading = false;
        state.username = action.payload.username;
      })
      .addCase(fetchRegister.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });

    // 处理获取用户信息
    builder
      .addCase(fetchUserInfo.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUserInfo.fulfilled, (state, action) => {
        state.loading = false;
        state.username = action.payload.username;
        state.userId = action.payload.id;
        state.isLoggedIn = true;
      })
      .addCase(fetchUserInfo.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

// 获取 actions 和 reducer
export const { logout, clearError } = userSlice.actions;
const userReducer = userSlice.reducer;

// 导出 reducer
export default userReducer;