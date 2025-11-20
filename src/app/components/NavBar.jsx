"use client";
import { useEffect, useState } from "react";
import { FaSpotify } from "react-icons/fa";

const NavBar = () => {
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [userId, setUserId] = useState(null);

  // Detect Spotify redirect with user_id param and store in localStorage
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const newUserId = params.get("user_id");

    if (newUserId) {
      localStorage.setItem("ms_user", newUserId);
      setUserId(newUserId);

      // Clean up URL (remove ?user_id=xyz from address bar)
      const cleanUrl = window.location.origin + window.location.pathname;
      window.history.replaceState({}, document.title, cleanUrl);
    } else {
      // Fallback to stored user ID
      const storedUser = localStorage.getItem("ms_user");
      if (storedUser) setUserId(storedUser);
    }
  }, []);

  // Fetch user profile from backend once userId is set
  useEffect(() => {
    if (!userId) return;

    const fetchUser = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:8000/spotify/me?user_id=${userId}`
        );
        const data = await res.json();

        if (data.error && data.error.includes("expired")) {
          // Handle expired session gracefully
          alert("Your Spotify session expired. Please log in again.");
          localStorage.removeItem("ms_user");
          setUserId(null);
          setUser(null);
          return;
        }

        if (!data.error) setUser(data);
      } catch (err) {
        console.error("Failed to fetch user:", err);
      }
    };

    fetchUser();
  }, [userId]);

  // Handle login redirect
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
      console.error("Spotify login error:", e);
      alert("Login failed. Try again later.");
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
          disabled={loading}
          className="bg-[#8BE8E5] glow py-3 px-5 rounded-lg font-semibold flex gap-4 items-center hover:scale-105 transition-transform disabled:opacity-60"
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
              className="w-10 h-10 rounded-full border"
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
