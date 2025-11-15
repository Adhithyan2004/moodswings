"use client";

import { useRef, useState } from "react";
import { FaExternalLinkAlt } from "react-icons/fa";

const TrackCard = ({ track }) => {
  const audioRef = useRef(null);
  const [playing, setPlaying] = useState(false);

  const handlePreview = () => {
    if (!track.preview_url) return;

    // Pause if playing the same song
    if (playing) {
      audioRef.current.pause();
      setPlaying(false);
      return;
    }

    // Stop previous audio if exists
    if (audioRef.current) {
      audioRef.current.pause();
    }

    const audio = new Audio(track.preview_url);
    audioRef.current = audio;
    audio.play();
    setPlaying(true);

    audio.onended = () => setPlaying(false);
  };

  return (
    <div className="flex items-center gap-4 p-4 glow-track rounded-xl ">
      {/* Album Art */}
      <img
        src={track.image}
        alt={track.name}
        className="w-16 h-16 rounded-lg object-cover"
      />

      {/* Track Info */}
      <div className="flex-1">
        <p className="font-semibold text-[#8BE8E5]">{track.name}</p>
        <p className="text-sm ">{track.artist}</p>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-6">
        <button
          onClick={handlePreview}
          disabled={!track.preview_url}
          className={`text-sm px-3 py-1 rounded-full ${
            track.preview_url
              ? "bg-[#8BE8E5] "
              : "bg-gray-600 text-gray-300 cursor-not-allowed"
          }`}
        >
          {playing ? "Pause" : "Preview"}
        </button>

        <a
          href={track.url}
          target="_blank"
          className="text-[#8BE8E5] underline text-sm"
        >
          <FaExternalLinkAlt size={20} />
        </a>
      </div>
    </div>
  );
};

export default TrackCard;
