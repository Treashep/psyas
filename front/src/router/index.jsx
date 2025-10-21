import { createBrowserRouter } from "react-router-dom";
import Talk from "../pages/talk/index.jsx";
import Login from "../pages/login/index.jsx"; // 修正路径
import Register from "../pages/register/index.jsx";
import { RootLayout, ProtectedRoute } from "../components/RootLayout";

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        path: '/talk',
        element: <ProtectedRoute />,
        children: [
          {
            index: true,
            element: <Talk></Talk>,
          }
        ]
      },
      {
        path: '/',
        element: <Login></Login>,
      },
      {
        path: '/register',
        element: <Register></Register>,
      },
    ]
  },
]);

export default router;