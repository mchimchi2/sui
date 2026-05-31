import React from "react";
import { useCurrentFrame } from "remotion";

export type SuitMood = "neutral" | "shocked" | "worried" | "explaining" | "happy";
type Props = { mood: SuitMood; scale?: number };

export const CharacterSuit: React.FC<Props> = ({ mood, scale = 1 }) => {
  const frame = useCurrentFrame();

  const breatheY = Math.sin(frame * 0.055) * 2;
  const blinkCycle = frame % 95;
  const eyeH = blinkCycle > 90 ? 0.05 : 1;
  const isTalking = mood === "explaining" || mood === "shocked" || mood === "happy";
  const jawOpen = isTalking ? Math.max(0, Math.sin(frame * 0.38)) * 6 : 0;

  // Colors — matches generated character
  const SUIT   = "#1A2540";
  const SUIT2  = "#111828";
  const SHIRT  = "#F0F0F0";
  const TIE    = "#8B1A1A";
  const TIEDARK= "#5C0F0F";
  const SKIN   = "#F0DCBF";
  const SKSH   = "#D4B896";
  const HAIR   = "#181210";
  const BROW   = "#1A1414";
  const OUT    = "#111111";
  const W      = 3.5;

  const lbY = mood === "shocked" ? -10 : mood === "worried" ? 5  : mood === "happy" ? -4 : 0;
  const rbY = mood === "shocked" ? -10 : mood === "worried" ? -4 : mood === "happy" ? -4 : 0;
  const lbR = mood === "worried" ? 12 : 0;
  const rbR = mood === "worried" ? -12 : 0;

  const leftArm =
    mood === "shocked"    ? "M 55 196 C 30 170  6 148  0 118" :
    mood === "explaining" ? "M 55 196 C 38 178 24 162 16 150" :
    mood === "happy"      ? "M 55 196 C 38 178 24 162 16 150" :
                            "M 55 196 C 38 228 24 272 18 318";

  const rightArm =
    mood === "explaining" ? "M 225 196 C 245 168 262 132 272  98" :
    mood === "shocked"    ? "M 225 196 C 248 172 268 148 278 118" :
    mood === "worried"    ? "M 225 196 C 242 172 240 144 222 120" :
    mood === "happy"      ? "M 225 196 C 245 168 262 132 272  98" :
                            "M 225 196 C 242 228 258 272 264 318";

  return (
    <svg viewBox="0 0 280 400" width={280 * scale} height={400 * scale} style={{ overflow: "visible" }}>

      {/* ── ARMS ── */}
      <path d={leftArm}  stroke={SUIT}  strokeWidth={52} strokeLinecap="round" fill="none" />
      <path d={leftArm}  stroke={SUIT2} strokeWidth={4}  strokeLinecap="round" fill="none" opacity={0.4} />
      <path d={rightArm} stroke={SUIT}  strokeWidth={52} strokeLinecap="round" fill="none" />
      <path d={rightArm} stroke={SUIT2} strokeWidth={4}  strokeLinecap="round" fill="none" opacity={0.4} />

      {/* ── BODY / JACKET ── */}
      {/* Main jacket shape */}
      <path d="M 55 192 L 20 400 L 260 400 L 225 192 Z" fill={SUIT} stroke={OUT} strokeWidth={W} />

      {/* Left lapel */}
      <path d="M 118 192 L 90 240 L 100 192 Z" fill={SUIT2} stroke={OUT} strokeWidth={2} />
      {/* Right lapel */}
      <path d="M 162 192 L 190 240 L 180 192 Z" fill={SUIT2} stroke={OUT} strokeWidth={2} />

      {/* Shirt front (white, center) */}
      <path d="M 118 192 L 108 400 L 172 400 L 162 192 Z" fill={SHIRT} />
      <path d="M 118 192 L 108 400" stroke="#DDD" strokeWidth={1.5} />
      <path d="M 162 192 L 172 400" stroke="#DDD" strokeWidth={1.5} />

      {/* Shirt buttons */}
      <circle cx="140" cy="230" r="3.5" fill="#CCC" />
      <circle cx="140" cy="258" r="3.5" fill="#CCC" />
      <circle cx="140" cy="286" r="3.5" fill="#CCC" />

      {/* Jacket outline over shirt edges */}
      <path d="M 55 192 L 20 400" stroke={OUT} strokeWidth={W} fill="none" />
      <path d="M 225 192 L 260 400" stroke={OUT} strokeWidth={W} fill="none" />

      {/* Chest pocket */}
      <rect x="168" y="210" width="30" height="22" rx="2" fill={SHIRT} stroke="#BBB" strokeWidth={1.5} />
      <path d="M 168 217 L 198 217" stroke="#BBB" strokeWidth={1} />

      {/* ── TIE ── (loosened, slightly angled) */}
      <path
        d="M 133 192 L 128 220 L 134 260 L 140 350 L 146 260 L 152 220 L 147 192 Z"
        fill={TIE} stroke={TIEDARK} strokeWidth={1.5}
      />
      {/* Tie knot */}
      <path d="M 133 192 L 140 210 L 147 192 L 140 196 Z" fill={TIEDARK} />
      {/* Tie stripe highlight */}
      <path d="M 137 225 L 139 340" stroke={TIEDARK} strokeWidth={2} opacity={0.5} />

      {/* ── NECK ── */}
      <rect x="118" y="158" width="44" height="42" rx="6" fill={SKIN} stroke={OUT} strokeWidth={W} />
      {/* Collar buttons area (shirt collar visible) */}
      <path d="M 118 175 L 140 185 L 162 175" stroke="#DDD" strokeWidth={2} fill="none" />

      {/* ── HEAD (breathing) ── */}
      <g transform={`translate(0, ${breatheY})`}>

        {/* Shadow under chin */}
        <ellipse cx="140" cy="158" rx="42" ry="8" fill="rgba(0,0,0,0.12)" />

        {/* Ears */}
        <ellipse cx="72"  cy="98" rx="10" ry="14" fill={SKIN} stroke={OUT} strokeWidth="2.5" />
        <ellipse cx="208" cy="98" rx="10" ry="14" fill={SKIN} stroke={OUT} strokeWidth="2.5" />
        {/* Inner ear */}
        <ellipse cx="72"  cy="98" rx="5" ry="8" fill={SKSH} />
        <ellipse cx="208" cy="98" rx="5" ry="8" fill={SKSH} />

        {/* Face */}
        <ellipse cx="140" cy="94" rx="66" ry="70" fill={SKIN} stroke={OUT} strokeWidth={W} />

        {/* Age detail — subtle nasolabial lines */}
        <path d="M 114 112 Q 108 124 112 132" stroke={SKSH} strokeWidth={1.5} fill="none" opacity={0.7} />
        <path d="M 166 112 Q 172 124 168 132" stroke={SKSH} strokeWidth={1.5} fill="none" opacity={0.7} />

        {/* 5 o'clock shadow (lower face) */}
        <ellipse cx="140" cy="148" rx="38" ry="16" fill="rgba(50,30,30,0.12)" />
        <ellipse cx="116" cy="142" rx="14" ry="10" fill="rgba(50,30,30,0.08)" />
        <ellipse cx="164" cy="142" rx="14" ry="10" fill="rgba(50,30,30,0.08)" />

        {/* ── HAIR ── */}
        {/* Main hair block */}
        <path d="M 76 82 C 74 28 206 28 204 82 C 194 54 172 44 140 42 C 108 44 86 54 76 82 Z" fill={HAIR} />
        {/* Messy front strands */}
        <path d="M 105 46 C 112 34 135 30 148 38" stroke={HAIR} strokeWidth={8} strokeLinecap="round" fill="none" />
        <path d="M 120 40 C 128 28 155 28 164 40" stroke={HAIR} strokeWidth={6} strokeLinecap="round" fill="none" />
        {/* White hair highlights (matching generated character) */}
        <path d="M 108 50 C 115 38 128 34 136 40" stroke="#8A8070" strokeWidth={2.5} strokeLinecap="round" fill="none" opacity={0.7} />
        <path d="M 148 42 C 158 32 172 36 178 48" stroke="#8A8070" strokeWidth={2} strokeLinecap="round" fill="none" opacity={0.5} />
        {/* Side hair */}
        <ellipse cx="78"  cy="106" rx="16" ry="32" fill={HAIR} />
        <ellipse cx="202" cy="106" rx="16" ry="32" fill={HAIR} />

        {/* ── EYEBROWS (thick, defined) ── */}
        <path
          d={`M 104 ${70 + lbY} Q 118 ${64 + lbY} 132 ${70 + lbY}`}
          stroke={BROW} strokeWidth={5} fill="none" strokeLinecap="round"
          transform={`rotate(${lbR}, 104, ${70 + lbY})`}
        />
        <path
          d={`M 148 ${70 + rbY} Q 162 ${64 + rbY} 176 ${70 + rbY}`}
          stroke={BROW} strokeWidth={5} fill="none" strokeLinecap="round"
          transform={`rotate(${rbR}, 176, ${70 + rbY})`}
        />

        {/* ── EYES ── */}
        {/* Left */}
        <ellipse cx="118" cy="90" rx="13" ry={13 * eyeH} fill="white" stroke={OUT} strokeWidth={2.5} />
        {eyeH > 0.2 && <>
          <ellipse cx="119" cy="91" rx="7" ry={7 * eyeH} fill="#1A1010" />
          <circle   cx="122" cy="87" r="2.8" fill="white" />
          {/* Crow's feet */}
          <path d="M 132 84 L 136 80" stroke={SKSH} strokeWidth={1.5} opacity={0.8} />
          <path d="M 133 90 L 138 88" stroke={SKSH} strokeWidth={1.2} opacity={0.6} />
        </>}
        {/* Right */}
        <ellipse cx="162" cy="90" rx="13" ry={13 * eyeH} fill="white" stroke={OUT} strokeWidth={2.5} />
        {eyeH > 0.2 && <>
          <ellipse cx="163" cy="91" rx="7" ry={7 * eyeH} fill="#1A1010" />
          <circle   cx="166" cy="87" r="2.8" fill="white" />
          {/* Crow's feet */}
          <path d="M 148 84 L 144 80" stroke={SKSH} strokeWidth={1.5} opacity={0.8} />
          <path d="M 147 90 L 142 88" stroke={SKSH} strokeWidth={1.2} opacity={0.6} />
        </>}

        {/* ── NOSE ── */}
        <path d="M 136 114 Q 140 122 144 114" stroke="#C8A888" strokeWidth={2.5} fill="none" strokeLinecap="round" />

        {/* ── MOUTH ── */}
        {mood === "worried" ? (
          <path d="M 118 138 Q 140 130 162 138" stroke={OUT} strokeWidth={3} fill="none" strokeLinecap="round" />
        ) : mood === "happy" ? (
          <path d="M 116 132 Q 140 148 164 132" stroke={OUT} strokeWidth={3} fill="white" strokeLinecap="round" />
        ) : jawOpen > 1.5 ? (
          <>
            <path
              d={`M 120 ${132 + jawOpen * 0.2} Q 140 ${142 + jawOpen} 160 ${132 + jawOpen * 0.2}`}
              stroke={OUT} strokeWidth={3} fill="white" strokeLinecap="round"
            />
            <path
              d={`M 126 ${136 + jawOpen * 0.5} Q 140 ${139 + jawOpen * 0.5} 154 ${136 + jawOpen * 0.5}`}
              stroke="#C08080" strokeWidth={2} fill="none"
            />
          </>
        ) : (
          <path d="M 122 135 Q 140 142 158 135" stroke={OUT} strokeWidth={3} fill="none" strokeLinecap="round" />
        )}

        {/* Blush */}
        {(mood === "shocked" || mood === "happy") && (
          <>
            <ellipse cx="100" cy="112" rx="16" ry="10" fill="rgba(220,100,80,0.28)" />
            <ellipse cx="180" cy="112" rx="16" ry="10" fill="rgba(220,100,80,0.28)" />
          </>
        )}
      </g>
    </svg>
  );
};
