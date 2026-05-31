import React from "react";
import { useCurrentFrame } from "remotion";

export type Mood = "neutral" | "surprised" | "worried" | "explaining";
type Props = { mood: Mood; scale?: number };

export const Character: React.FC<Props> = ({ mood, scale = 1 }) => {
  const frame = useCurrentFrame();

  const breatheY = Math.sin(frame * 0.06) * 2.5;

  const blinkCycle = frame % 90;
  const eyeH = blinkCycle > 85 ? 0.05 : 1;

  const isTalking = mood === "explaining" || mood === "surprised";
  const jawOpen = isTalking ? Math.max(0, Math.sin(frame * 0.38)) * 7 : 0;

  // Colors (monochrome anime style matching reference)
  const SKIN  = "#FFFFFF";
  const SKINSH = "#E4E4E4";
  const HAIR  = "#1A1A1A";
  const HOOD  = "#909098";
  const HOODS = "#686870";
  const OUT   = "#111111";
  const W     = 4;

  // Eyebrow adjustments per mood
  const lbY  = mood === "surprised" ? -10 : mood === "worried" ?  5 : 0;
  const rbY  = mood === "surprised" ? -10 : mood === "worried" ? -4 : 0;
  const lbR  = mood === "worried"   ?  8  : 0;
  const rbR  = mood === "worried"   ? -8  : 0;

  // Arm paths per mood (arms drawn with thick stroke = hoodie sleeve)
  const leftArm =
    mood === "surprised"
      ? "M 62 204 C 38 180 14 158  4 128"
      : mood === "explaining"
      ? "M 62 204 C 44 188 28 172 18 158"
      : "M 62 204 C 44 236 28 278 20 322";

  const rightArm =
    mood === "explaining"
      ? "M 218 204 C 238 174 258 138 270 100"
      : mood === "surprised"
      ? "M 218 204 C 242 180 266 158 276 128"
      : mood === "worried"
      ? "M 218 204 C 234 178 232 148 212 122"
      : "M 218 204 C 236 236 252 278 260 322";

  return (
    <svg
      viewBox="0 0 280 420"
      width={280 * scale}
      height={420 * scale}
      style={{ overflow: "visible" }}
    >
      {/* ── ARMS (behind body) ── */}
      <path d={leftArm}  stroke={HOOD} strokeWidth={50} strokeLinecap="round" fill="none" />
      <path d={leftArm}  stroke={OUT}  strokeWidth={W}  strokeLinecap="round" fill="none" opacity={0.18} />
      <path d={rightArm} stroke={HOOD} strokeWidth={50} strokeLinecap="round" fill="none" />
      <path d={rightArm} stroke={OUT}  strokeWidth={W}  strokeLinecap="round" fill="none" opacity={0.18} />

      {/* ── BODY / HOODIE ── */}
      <path d="M 62 200 L 28 420 L 252 420 L 218 200 Z" fill={HOOD} stroke={OUT} strokeWidth={W} strokeLinejoin="round" />
      {/* Center shadow stripe */}
      <path d="M 124 200 L 114 420 L 166 420 L 156 200 Z" fill={HOODS} opacity={0.55} />
      {/* Pocket */}
      <rect x="94" y="295" width="92" height="65" rx="8" fill={HOODS} stroke={OUT} strokeWidth="3" />
      <line x1="140" y1="295" x2="140" y2="360" stroke={HOOD} strokeWidth="2" />
      {/* Drawstring dots */}
      <circle cx="116" cy="216" r="5" fill={HOODS} />
      <circle cx="164" cy="216" r="5" fill={HOODS} />

      {/* ── NECK ── */}
      <rect x="120" y="162" width="40" height="46" rx="7" fill={SKIN} stroke={OUT} strokeWidth={W} />

      {/* ── HEAD (breathes gently) ── */}
      <g transform={`translate(0, ${breatheY})`}>
        {/* Ears */}
        <ellipse cx="74"  cy="104" rx="10" ry="14" fill={SKIN} stroke={OUT} strokeWidth="3" />
        <ellipse cx="206" cy="104" rx="10" ry="14" fill={SKIN} stroke={OUT} strokeWidth="3" />

        {/* Face */}
        <ellipse cx="140" cy="100" rx="66" ry="72" fill={SKIN} stroke={OUT} strokeWidth={W} />
        {/* Chin shadow */}
        <ellipse cx="140" cy="156" rx="38" ry="10" fill={SKINSH} opacity={0.45} />

        {/* ── HAIR ── */}
        {/* Top block */}
        <path d="M 76 86 C 74 34 206 34 204 86 C 194 60 172 48 140 46 C 108 48 86 60 76 86 Z" fill={HAIR} />
        {/* Side pieces */}
        <ellipse cx="78"  cy="108" rx="16" ry="34" fill={HAIR} />
        <ellipse cx="202" cy="108" rx="16" ry="34" fill={HAIR} />

        {/* ── EYEBROWS ── */}
        <path
          d={`M 108 ${74 + lbY} Q 121 ${68 + lbY} 134 ${74 + lbY}`}
          stroke={HAIR} strokeWidth="4.5" fill="none" strokeLinecap="round"
          transform={`rotate(${lbR}, 108, ${74 + lbY})`}
        />
        <path
          d={`M 146 ${74 + rbY} Q 159 ${68 + rbY} 172 ${74 + rbY}`}
          stroke={HAIR} strokeWidth="4.5" fill="none" strokeLinecap="round"
          transform={`rotate(${rbR}, 172, ${74 + rbY})`}
        />

        {/* ── EYES ── */}
        {/* Left */}
        <ellipse cx="121" cy="96" rx="12" ry={13 * eyeH} fill="white" stroke={OUT} strokeWidth="2.5" />
        {eyeH > 0.2 && <>
          <ellipse cx="122" cy="97" rx="6.5" ry={6.5 * eyeH} fill={HAIR} />
          <circle   cx="124" cy="93" r="2.4" fill="white" />
        </>}

        {/* Right */}
        <ellipse cx="159" cy="96" rx="12" ry={13 * eyeH} fill="white" stroke={OUT} strokeWidth="2.5" />
        {eyeH > 0.2 && <>
          <ellipse cx="160" cy="97" rx="6.5" ry={6.5 * eyeH} fill={HAIR} />
          <circle   cx="162" cy="93" r="2.4" fill="white" />
        </>}

        {/* ── NOSE ── */}
        <path d="M 137 118 Q 140 124 143 118" stroke="#C8B090" strokeWidth="2.2" fill="none" strokeLinecap="round" />

        {/* ── MOUTH ── */}
        {mood === "worried" ? (
          <path d="M 122 136 Q 140 129 158 136" stroke={OUT} strokeWidth="3" fill="none" strokeLinecap="round" />
        ) : jawOpen > 1.5 ? (
          <>
            <path
              d={`M 120 ${130 + jawOpen * 0.25} Q 140 ${139 + jawOpen} 160 ${130 + jawOpen * 0.25}`}
              stroke={OUT} strokeWidth="3" fill="white" strokeLinecap="round"
            />
            <path
              d={`M 128 ${133 + jawOpen * 0.5} Q 140 ${136 + jawOpen * 0.55} 152 ${133 + jawOpen * 0.5}`}
              stroke="#E0A0A0" strokeWidth="1.8" fill="none"
            />
          </>
        ) : (
          <path d="M 124 133 Q 140 141 156 133" stroke={OUT} strokeWidth="3" fill="none" strokeLinecap="round" />
        )}

        {/* Blush */}
        {(mood === "explaining" || mood === "surprised") && (
          <>
            <ellipse cx="98"  cy="118" rx="15" ry="9" fill="rgba(255,145,125,0.32)" />
            <ellipse cx="182" cy="118" rx="15" ry="9" fill="rgba(255,145,125,0.32)" />
          </>
        )}
      </g>
    </svg>
  );
};
