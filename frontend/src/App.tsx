import { FC } from "react";
import HomePage from "@/pages/Home/HomePage";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { Layout } from "./Layout";
import { setAuthToken } from "./Middlewares/setAuthTokens";
import ArticleDetail from "./pages/Home/ArticleDetail";
import AboutUs from "./pages/Home/AboutUs";
import ContactUs from "./pages/Home/ContactUs";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/articles/:id",
        element: <ArticleDetail/>
      },
      {
        path: "/aboutus",
        element: <AboutUs/>
      },
      {
        path: "/contactus",
        element: <ContactUs/>
      },
      {
        path: "*",
        element: <HomePage/>
      }
    ],
  },
]);
const App: FC = () => {
  
  const token = localStorage.getItem("token");
  if (token) {
      setAuthToken(token);
  }

  return (
    <RouterProvider router={router} />
  );
};

export default App;
