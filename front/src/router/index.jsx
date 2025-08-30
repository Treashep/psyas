import { createBrowserRouter } from "react-router-dom";
import Talk from "../pages/talk/index.jsx";
import Login from "../pages/login/index.jsx"; // 修正路径
import Register from "../pages/register/index.jsx";

const router = createBrowserRouter([
  {
    path: '/',
    element: <Talk></Talk>,
  },
  {
    path: '/login',
    element: <Login></Login>,
  },
  {
    path: '/register',
    element: <Register></Register>,
  },
]);

export default router;