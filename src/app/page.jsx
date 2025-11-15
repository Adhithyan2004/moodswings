"use client";

import { useEffect } from "react";
import { useSearchParams } from "next/navigation";
import Footer from "./components/Footer";
import MainCnt from "./components/MainCnt";
import NavBar from "./components/NavBar";

const page = () => {
  const params = useSearchParams();
  const user_id = params.get("user_id");

  useEffect(() => {
    if (user_id) {
      console.log("Saving user_id:", user_id);
      localStorage.setItem("ms_user", user_id);

      // cleanup URL after storing
      window.history.replaceState(null, "", "/");
    }
  }, [user_id]);

  return (
    <div className="h-full min-h-screen bg-linear-to-b from-[#090909] to-[#00222F]">
      <NavBar />
      <MainCnt />
      <Footer />
    </div>
  );
};

export default page;
