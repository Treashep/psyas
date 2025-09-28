import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { loginAPI, registerAPI } from '../../apis/user';

export const fetchLogin = createAsyncThunk(
  'user/fetchLogin',
  async (loginForm, { rejectWithValue }) => {
    try {
      const res = await loginAPI(loginForm);
      return res.data; // 返回 { token, username }
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

// 定义 slice
const userSlice = createSlice({
  name: 'user',
  initialState: {
    username: '',
    token: '',
    isLoggedIn: false,
    error: null,
    loading: false,
  },
  reducers: {
    logout(state) {
      state.token = '';
      state.isLoggedIn = false;
      state.username = '';
      state.error = null;
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
        state.isLoggedIn = true;
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
  }
});

// 获取 actions 和 reducer
export const { logout, clearError } = userSlice.actions;
const userReducer = userSlice.reducer;

// 导出 reducer
export default userReducer;