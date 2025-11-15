"use client";
import { useEffect, useState } from "react";
import { FaSpotify } from "react-icons/fa";

const NavBar = () => {
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);

  // Fetch user info if logged in
  useEffect(() => {
    const userId = localStorage.getItem("ms_user");
    if (!userId) return;

    const fetchUser = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/spotify/me?user_id=${userId}`
        );
        const data = await res.json();
        if (!data.error) setUser(data);
      } catch (err) {
        console.error("Failed to fetch user:", err);
      }
    };

    fetchUser();
  }, []);

  const handleSpotifyLogin = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/spotify/login`
      );
      const data = await res.json();
      if (data.auth_url) {
        window.location.href = data.auth_url;
      } else {
        alert("Unable to initiate Spotify login.");
      }
    } catch (e) {
      console.error(e);
      alert("Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-between items-center mx-20 pt-10">
      <h1 className="Logo text-3xl text-[#8BE8E5]">MoodSwings</h1>

      {!user ? (
        <button
          onClick={handleSpotifyLogin}
          className="bg-[#8BE8E5] glow py-3 px-5 rounded-lg font-semibold flex gap-4 items-center"
        >
          <FaSpotify size={20} />
          {loading ? "Connecting..." : "Log in with Spotify"}
        </button>
      ) : (
        <div className="flex items-center gap-3">
          {user.images?.length > 0 && (
            <img
              src={user.images[0].url}
              alt="User Avatar"
              className="w-10 h-10 rounded-full border border-[#8BE8E5]"
            />
          )}
          <span className="text-[#8BE8E5] font-semibold">
            {user.display_name || "Spotify User"}
          </span>
        </div>
      )}
    </div>
  );
};

export default NavBar;
