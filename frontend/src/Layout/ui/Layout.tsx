import { FC } from "react";
import Header from "@/components/Header";
import { Outlet } from "react-router-dom";
import Footer from "@/components/Footer";

const Layout: FC = () => {
  return (
    <div className="w-full h-auto min-h-[100vh] flex flex-col">
      <Header />
      <main id="main" className="w-full h-auto overflow-x-hidden bg-[white]">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
