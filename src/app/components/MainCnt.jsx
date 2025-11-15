"use client";

import { useState } from "react";
import { GiMusicalNotes } from "react-icons/gi";
import TrackCard from "./TrackCard";

const MainCnt = () => {
  const [mood, setMood] = useState("");
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleRecommend = async (e) => {
    if (e.key !== "Enter") return;
    if (!mood.trim()) return;

    const userId = localStorage.getItem("ms_user");
    if (!userId) {
      alert("Please log in with Spotify first.");
      return;
    }

    setLoading(true);
    setTracks([]);
    setHasSearched(true);

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/ai/recommend?mood=${mood}&user_id=${userId}`
      );

      const data = await res.json();

      if (data.error) {
        if (data.error.includes("expired")) {
          alert("Your Spotify session expired. Please log in again.");
          localStorage.removeItem("ms_user");
          window.location.href = "/";
          return;
        } else {
          alert("Something went wrong. Try again.");
          return;
        }
      }

      setTracks(data.tracks || []);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      alert("Server unreachable. Try again later.");
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center w-full text-white min-h-[calc(100vh-8rem)] px-5 py-10">
      {/* Hero Section */}
      {!hasSearched && (
        <div className="flex flex-col items-center mt-28 text-center">
          <h1 className="Heading text-[2.8rem] mb-2 text-[#8BE8E5]">
            Welcome to MoodSwings
          </h1>
          <p className="mb-4 text-lg">
            Type a mood. Get music that feels the same.
          </p>
        </div>
      )}

      {/*  Search Bar */}
      <div
        className={`relative transition-all duration-500 ${
          hasSearched ? "mt-0" : "mt-6"
        }`}
      >
        <input
          type="text"
          placeholder="What's the vibe today?"
          value={mood}
          onChange={(e) => setMood(e.target.value)}
          onKeyDown={!loading ? handleRecommend : undefined}
          className="px-8 py-4 w-2xl rounded-full outline-none border border-[#8BE8E5]  text-white"
        />
        <GiMusicalNotes
          size={30}
          className="absolute right-6 top-1/2 -translate-y-1/2"
        />
      </div>

      {/* Loader */}
      {loading && (
        <div className="text-[#8BE8E5] mt-8 animate-pulse text-lg">
          Finding your vibe...
        </div>
      )}

      {/* Track List */}
      {hasSearched && !loading && (
        <div className="grid grid-cols-2 gap-10 mt-10 w-6xl">
          {tracks.map((t, idx) => (
            <TrackCard key={idx} track={t} />
          ))}
        </div>
      )}
    </div>
  );
};

export default MainCnt;
