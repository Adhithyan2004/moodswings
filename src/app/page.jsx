"use client";
import { useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { TbMusicSearch } from "react-icons/tb";
import Image from "next/image";

const Page = () => {
  const router = useRouter();
  const [hovered, setHovered] = useState(false);
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
    <div className="h-full relative flex flex-col items-center justify-center min-h-screen bg-linear-to-b from-[#090909] to-[#00222F] overflow-hidden">
      <div className="text-center flex flex-col gap-3">
        <h1 className="Heading text-[#8BE8E5] text-6xl">MoodSwings</h1>
        <p className="text-white text-xl">What's the vibe today?</p>
      </div>

      {/* Hover container */}
      <div
        className=" mt-10 z-10 glow rounded-full cursor-pointer flex items-center justify-center transition-all duration-300 hover:scale-110"
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        <AnimatePresence mode="wait">
          {hovered ? (
            <motion.button
              key="button"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.3 }}
              className="px-8 py-5 rounded-full text-[#8BE8E5] font-semibold text-lg transition-all duration-300"
              onClick={() => router.push("/home")}
            >
              Enter <span className="Heading">MoodSwings</span>
            </motion.button>
          ) : (
            <motion.div
              key="icon"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.3 }}
            >
              <TbMusicSearch size={40} className="m-5 text-[#8BE8E5]" />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <Image
        src="/images/glowbg.png"
        width={0}
        height={0}
        alt="Glowing Background ring"
        className="w-full absolute -bottom-16 "
      />
    </div>
  );
};

export default Page;
