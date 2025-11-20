"use client";


import Footer from "../components/Footer";
import MainCnt from "../components/MainCnt";
import NavBar from "../components/NavBar";

const page = () => {


  return (
    <div className="h-full min-h-screen bg-linear-to-b from-[#090909] to-[#00222F]">
      <NavBar />
      <MainCnt />
      <Footer />
    </div>
  );
};

export default page;
