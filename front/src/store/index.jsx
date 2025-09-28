import { configureStore } from "@reduxjs/toolkit";  
import userReducer from "./modules/user";

//创建根store组合子模块
const store = configureStore({
  reducer:{
    user:userReducer
  }
})
export default store