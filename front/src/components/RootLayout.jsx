import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Outlet, Navigate } from 'react-router-dom';
import { fetchUserInfo } from '../store/modules/user';

// 受保护的路由组件
const ProtectedRoute = () => {
  const { isLoggedIn } = useSelector(state => state.user);
  return isLoggedIn ? <Outlet /> : <Navigate to="/" replace />;
};

const RootLayout = () => {
  const dispatch = useDispatch();
  const { isLoggedIn, token } = useSelector(state => state.user);

  useEffect(() => {
    // 如果有token但没有用户信息，则获取用户信息
    if (token && !isLoggedIn) {
      dispatch(fetchUserInfo());
    }
  }, [token, isLoggedIn, dispatch]);

  return <Outlet />;
};

export { RootLayout, ProtectedRoute };