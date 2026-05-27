import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

type Mood = "neutral" | "surprised" | "worried" | "explaining";

type Props = { mood: Mood; scale?: number };

export const Character: React.FC<Props> = ({ mood, scale = 1 }) => {
  const frame = useCurrentFrame();

  // Gentle idle bob
  const bob = Math.sin(frame * 0.08) * 4;

  // Eye blink every ~90 frames
  const blinkCycle = frame % 90;
  const isBlinking = blinkCycle > 84 && blinkCycle < 90;
  const eyeScaleY = isBlinking ? 0.1 : 1;

  // Mouth shape per mood
  const mouthPath: Record<Mood, string> = {
    neutral:    "M 36 58 Q 50 65 64 58",
    explaining: "M 34 56 Q 50 68 66 56",
    surprised:  "M 40 56 Q 50 70 60 56",
    worried:    "M 36 62 Q 50 54 64 62",
  };

  // Eyebrow raise per mood
  const eyebrowY: Record<Mood, number> = {
    neutral: 0, explaining: -2, surprised: -8, worried: 3,
  };

  // Sweat drop for worried
  const showSweat = mood === "worried" || mood === "surprised";

  return (
    <svg
      viewBox="0 0 100 160"
      width={180 * scale}
      height={288 * scale}
      style={{ transform: `translateY(${bob}px)`, overflow: "visible" }}
    >
      {/* Shadow */}
      <ellipse cx="50" cy="158" rx="22" ry="5" fill="rgba(0,0,0,0.12)" />

      {/* Body - suit */}
      <rect x="22" y="88" width="56" height="68" rx="12" fill="#2D4A8F" />

      {/* Shirt / inner */}
      <rect x="42" y="88" width="16" height="50" rx="4" fill="#fff" />

      {/* Tie */}
      <polygon points="50,92 46,102 50,130 54,102" fill="#FF6B35" />

      {/* Left arm */}
      <rect x="6" y="90" width="18" height="38" rx="9" fill="#2D4A8F" />
      {/* Left hand */}
      <circle cx="15" cy="132" r="9" fill="#FFD5A8" />

      {/* Right arm */}
      <rect x="76" y="90" width="18" height="38" rx="9" fill="#2D4A8F" />
      {/* Right hand */}
      <circle cx="85" cy="132" r="9" fill="#FFD5A8" />

      {/* Legs */}
      <rect x="28" y="148" width="18" height="12" rx="6" fill="#1a2f5e" />
      <rect x="54" y="148" width="18" height="12" rx="6" fill="#1a2f5e" />

      {/* Neck */}
      <rect x="43" y="82" width="14" height="12" rx="4" fill="#FFD5A8" />

      {/* Head */}
      <ellipse cx="50" cy="60" rx="28" ry="30" fill="#FFD5A8" />

      {/* Hair */}
      <ellipse cx="50" cy="33" rx="28" ry="12" fill="#3D2B1F" />
      <rect x="22" y="33" width="56" height="10" rx="4" fill="#3D2B1F" />

      {/* Left eyebrow */}
      <path
        d={`M 32 ${42 + eyebrowY[mood]} Q 38 ${39 + eyebrowY[mood]} 44 ${42 + eyebrowY[mood]}`}
        stroke="#3D2B1F" strokeWidth="2.5" fill="none" strokeLinecap="round"
      />
      {/* Right eyebrow */}
      <path
        d={`M 56 ${42 + eyebrowY[mood]} Q 62 ${39 + eyebrowY[mood]} 68 ${42 + eyebrowY[mood]}`}
        stroke="#3D2B1F" strokeWidth="2.5" fill="none" strokeLinecap="round"
      />

      {/* Left eye */}
      <ellipse cx="38" cy="50" rx="5" ry={5 * eyeScaleY} fill="#3D2B1F" />
      <circle cx="39.5" cy="48.5" r="1.5" fill="#fff" />

      {/* Right eye */}
      <ellipse cx="62" cy="50" rx="5" ry={5 * eyeScaleY} fill="#3D2B1F" />
      <circle cx="63.5" cy="48.5" r="1.5" fill="#fff" />

      {/* Mouth */}
      <path
        d={mouthPath[mood]}
        stroke="#3D2B1F" strokeWidth="2.5" fill="none" strokeLinecap="round"
      />

      {/* Cheek blush */}
      {(mood === "surprised" || mood === "explaining") && (
        <>
          <ellipse cx="28" cy="56" rx="6" ry="4" fill="rgba(255,150,120,0.35)" />
          <ellipse cx="72" cy="56" rx="6" ry="4" fill="rgba(255,150,120,0.35)" />
        </>
      )}

      {/* Sweat drop */}
      {showSweat && (
        <g>
          <path d="M 76 38 Q 79 32 76 28 Q 73 32 76 38 Z" fill="#7EC8E3" />
        </g>
      )}
    </svg>
  );
};
