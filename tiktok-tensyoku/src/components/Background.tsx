import React from "react";
import { AbsoluteFill } from "remotion";

const CITY_LIGHTS: [number, number, number, string, number][] = [
  [68,820,2.2,"#FFD966",0.90],[85,800,1.5,"#FF9900",0.80],[110,835,2.0,"#FFE599",0.85],
  [138,810,1.5,"#FFFFFF",0.65],[162,825,2.0,"#FF9900",0.80],[185,800,1.5,"#FFE599",0.70],
  [210,830,2.0,"#FFFFFF",0.75],[240,815,1.5,"#FF9900",0.70],[265,825,2.0,"#FFD966",0.85],
  [290,805,2.0,"#FF6644",0.65],[315,835,1.5,"#FFE599",0.80],[345,815,2.0,"#FFFFFF",0.65],
  [372,828,1.5,"#FF9900",0.75],[398,802,2.0,"#FFD966",0.80],[428,820,1.5,"#FFFFFF",0.65],
  [452,832,2.0,"#FF9900",0.80],[480,808,1.5,"#FFE599",0.75],[510,822,2.0,"#FFFFFF",0.65],
  [535,798,1.5,"#FF9900",0.80],[560,818,1.8,"#FFD966",0.75],
  [72,858,1.8,"#FFD966",0.70],[98,872,1.5,"#FFFFFF",0.60],[125,850,2.0,"#FF9900",0.75],
  [155,868,1.5,"#FFE599",0.65],[182,852,2.0,"#FFD966",0.78],[208,870,1.5,"#FFFFFF",0.60],
  [235,858,1.8,"#FF6644",0.70],[262,875,1.5,"#FFD966",0.65],[292,856,2.0,"#FF9900",0.72],
  [318,872,1.5,"#FFFFFF",0.60],[348,858,1.8,"#FFE599",0.70],[378,870,1.5,"#FF9900",0.65],
  [405,854,2.0,"#FFD966",0.75],[432,868,1.5,"#FFFFFF",0.60],[460,858,1.8,"#FF9900",0.70],
  [488,872,1.5,"#FFE599",0.65],[518,856,2.0,"#FFD966",0.72],[548,870,1.5,"#FFFFFF",0.60],
  [75,905,1.5,"#FF9900",0.60],[108,918,1.8,"#FFD966",0.68],[140,902,1.5,"#FFFFFF",0.55],
  [170,915,2.0,"#FF9900",0.65],[200,908,1.5,"#FFE599",0.60],[232,920,1.8,"#FFD966",0.65],
  [262,905,1.5,"#FFFFFF",0.55],[295,918,2.0,"#FF9900",0.62],[328,904,1.5,"#FFD966",0.60],
  [358,916,1.8,"#FFFFFF",0.55],[390,908,1.5,"#FF9900",0.62],[422,920,2.0,"#FFE599",0.60],
  [455,906,1.5,"#FFD966",0.65],[488,918,1.8,"#FF9900",0.58],[520,908,1.5,"#FFFFFF",0.55],
  [550,920,1.8,"#FFD966",0.60],
];

const BUILDINGS: [number, number, number, number][] = [
  [55,780,60,55],[118,790,45,45],[165,775,55,50],[220,785,40,40],
  [260,770,65,55],[325,780,50,45],[375,768,70,57],[445,778,45,47],
  [490,772,55,53],[545,768,40,57],
];

export const Background: React.FC = () => (
  <AbsoluteFill style={{ overflow: "hidden" }}>
    {/* Room base */}
    <div style={{ position: "absolute", inset: 0, background: "#080604" }} />

    <svg
      viewBox="0 0 1080 1920"
      style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#020810" />
          <stop offset="50%" stopColor="#060F1E" />
          <stop offset="100%" stopColor="#0D1408" />
        </linearGradient>
        <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#100C06" />
          <stop offset="100%" stopColor="#060402" />
        </linearGradient>
        <linearGradient id="wall" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#110D08" />
          <stop offset="100%" stopColor="#080604" />
        </linearGradient>
        <radialGradient id="ceilLight" cx="50%" cy="100%" r="50%">
          <stop offset="0%" stopColor="#7A5C28" stopOpacity="0.35" />
          <stop offset="100%" stopColor="#7A5C28" stopOpacity="0" />
        </radialGradient>
        <radialGradient id="windowGlow" cx="50%" cy="80%" r="60%">
          <stop offset="0%" stopColor="#1A3055" stopOpacity="0.4" />
          <stop offset="100%" stopColor="#020810" stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* Ceiling */}
      <rect x="0" y="0" width="1080" height="260" fill="#060402" />
      {/* Ceiling light glow */}
      <ellipse cx="540" cy="260" rx="420" ry="120" fill="url(#ceilLight)" />
      {/* Ceiling light fixture */}
      <ellipse cx="540" cy="220" rx="60" ry="12" fill="#2A1E0A" />
      <ellipse cx="540" cy="228" rx="32" ry="6" fill="#3A2A10" opacity="0.8" />

      {/* Left wall */}
      <rect x="0" y="260" width="660" height="1200" fill="#0E0A05" />

      {/* Window frame */}
      <rect x="30" y="275" width="590" height="890" rx="6" fill="#0A0806" stroke="#1E1510" strokeWidth="10" />

      {/* Window glass — night sky */}
      <rect x="40" y="285" width="570" height="870" fill="url(#sky)" />

      {/* Window inner glow */}
      <rect x="40" y="285" width="570" height="870" fill="url(#windowGlow)" />

      {/* Building silhouettes */}
      {BUILDINGS.map(([x, y, w, h], i) => (
        <rect key={i} x={x} y={y} width={w} height={h} fill="#030608" />
      ))}

      {/* City lights */}
      {CITY_LIGHTS.map(([x, y, r, color, opacity], i) => (
        <circle key={i} cx={x} cy={y} r={r} fill={color} opacity={opacity} />
      ))}

      {/* Window dividers */}
      <rect x="326" y="285" width="6" height="870" fill="#1A1208" />
      <rect x="40"  y="715" width="570" height="6"   fill="#1A1208" />

      {/* Right wall */}
      <rect x="660" y="260" width="420" height="1200" fill="url(#wall)" />

      {/* TV / monitor on right wall */}
      <rect x="720" y="380" width="320" height="200" rx="12" fill="#0A0C10" stroke="#1E1C18" strokeWidth="4" />
      <rect x="730" y="390" width="300" height="180" rx="8" fill="#0E1218" />
      {/* Screen glow */}
      <rect x="730" y="390" width="300" height="180" rx="8" fill="#1A2838" opacity="0.7" />
      {/* Screen content lines */}
      <rect x="748" y="408" width="180" height="12" rx="4" fill="#2A4060" opacity="0.8" />
      <rect x="748" y="428" width="240" height="8"  rx="4" fill="#1E3050" opacity="0.7" />
      <rect x="748" y="444" width="200" height="8"  rx="4" fill="#1E3050" opacity="0.6" />
      <rect x="748" y="460" width="220" height="8"  rx="4" fill="#1E3050" opacity="0.6" />
      <rect x="748" y="476" width="160" height="8"  rx="4" fill="#1E3050" opacity="0.5" />
      {/* TV stand */}
      <rect x="860" y="580" width="40" height="24" rx="4" fill="#1A1410" />
      <rect x="840" y="600" width="80" height="8"  rx="4" fill="#140E08" />

      {/* Ambient screen glow on wall */}
      <ellipse cx="880" cy="490" rx="200" ry="120" fill="#0A1830" opacity="0.3" />

      {/* Couch — just the top edge visible */}
      <path d="M 0 1320 Q 300 1300 580 1320 L 580 1380 Q 300 1360 0 1380 Z" fill="#2A1E10" />
      <path d="M 0 1318 Q 300 1298 580 1318" stroke="#3A2A16" strokeWidth="4" fill="none" />

      {/* Floor */}
      <rect x="0" y="1460" width="1080" height="460" fill="url(#floor)" />
      {/* Floor reflection line */}
      <line x1="0" y1="1462" x2="1080" y2="1462" stroke="#1A1208" strokeWidth="2" />

      {/* Overall vignette */}
      <radialGradient id="vignette" cx="50%" cy="50%" r="70%">
        <stop offset="0%"   stopColor="transparent" />
        <stop offset="100%" stopColor="#000000" stopOpacity="0.55" />
      </radialGradient>
      <rect x="0" y="0" width="1080" height="1920" fill="url(#vignette)" />
    </svg>
  </AbsoluteFill>
);
