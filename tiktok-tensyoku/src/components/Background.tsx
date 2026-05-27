import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";

export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  // Very slow pan to give depth
  const pan = frame * 0.04;

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {/* Sky gradient */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "linear-gradient(180deg, #E8F4FD 0%, #FFF8F2 55%, #FFF0E0 100%)",
        }}
      />

      {/* Floating soft circles - depth bg */}
      <svg
        viewBox="0 0 1080 1920"
        style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
      >
        <circle cx={200 + pan} cy={300} r={220} fill="rgba(255,200,150,0.12)" />
        <circle cx={900 - pan} cy={600} r={300} fill="rgba(150,200,255,0.10)" />
        <circle cx={540} cy={1600 + pan} r={400} fill="rgba(255,180,120,0.10)" />

        {/* Office window top-right */}
        <rect x={700} y={60} width={320} height={400} rx={16} fill="rgba(150,210,255,0.25)" stroke="rgba(100,160,220,0.4)" strokeWidth={4} />
        {/* Window cross */}
        <line x1={860} y1={60} x2={860} y2={460} stroke="rgba(100,160,220,0.4)" strokeWidth={3} />
        <line x1={700} y1={260} x2={1020} y2={260} stroke="rgba(100,160,220,0.4)" strokeWidth={3} />
        {/* Window outside */}
        <rect x={720} y={80} width={130} height={170} rx={6} fill="rgba(135,206,235,0.3)" />
        <rect x={860} y={80} width={140} height={170} rx={6} fill="rgba(135,206,235,0.25)" />
        <rect x={720} y={270} width={130} height={170} rx={6} fill="rgba(135,206,235,0.22)" />
        <rect x={860} y={270} width={140} height={170} rx={6} fill="rgba(135,206,235,0.28)" />

        {/* Desk */}
        <rect x={0} y={1550} width={1080} height={40} rx={8} fill="#C8956C" />
        <rect x={0} y={1590} width={1080} height={330} fill="#D9A87A" />
        <rect x={40} y={1510} width={500} height={50} rx={6} fill="#BF8B5E" />

        {/* Monitor on desk */}
        <rect x={60} y={1360} width={380} height={240} rx={14} fill="#2D4A8F" stroke="#1a2f5e" strokeWidth={4} />
        <rect x={80} y={1380} width={340} height={200} rx={8} fill="#E8F4FD" />
        {/* Monitor text lines */}
        <rect x={100} y={1400} width={200} height={14} rx={4} fill="rgba(45,74,143,0.3)" />
        <rect x={100} y={1425} width={280} height={10} rx={4} fill="rgba(45,74,143,0.2)" />
        <rect x={100} y={1445} width={240} height={10} rx={4} fill="rgba(45,74,143,0.2)" />
        <rect x={100} y={1465} width={260} height={10} rx={4} fill="rgba(45,74,143,0.2)" />
        {/* Monitor stand */}
        <rect x={220} y={1600} width={60} height={30} rx={4} fill="#BF8B5E" />
        <rect x={180} y={1625} width={140} height={14} rx={4} fill="#A07040" />

        {/* Coffee mug */}
        <rect x={500} y={1510} width={70} height={80} rx={10} fill="#fff" stroke="#ddd" strokeWidth={2} />
        <path d="M 570 1530 Q 600 1530 600 1560 Q 600 1590 570 1590" stroke="#ddd" strokeWidth={4} fill="none" strokeLinecap="round" />
        <ellipse cx={535} cy={1520} rx={30} ry={8} fill="rgba(180,120,60,0.5)" />

        {/* Plant */}
        <rect x={920} y={1490} width={50} height={70} rx={8} fill="#C8956C" />
        <ellipse cx={945} cy={1490} rx={55} ry={35} fill="#5aab6e" />
        <ellipse cx={920} cy={1465} rx={35} ry={25} fill="#4a9b5e" />
        <ellipse cx={970} cy={1458} rx={30} ry={22} fill="#5aab6e" />

        {/* Documents on desk */}
        <rect x={480} y={1520} width={160} height={110} rx={6} fill="white" stroke="#ddd" strokeWidth={2} transform="rotate(-8, 560, 1575)" />
        <rect x={460} y={1530} width={160} height={110} rx={6} fill="white" stroke="#ddd" strokeWidth={2} transform="rotate(-3, 540, 1585)" />
        {/* Text lines on doc */}
        <rect x={475} y={1545} width={100} height={8} rx={2} fill="rgba(0,0,0,0.15)" transform="rotate(-3, 525, 1549)" />
        <rect x={475} y={1560} width={130} height={6} rx={2} fill="rgba(0,0,0,0.10)" transform="rotate(-3, 540, 1563)" />
        <rect x={475} y={1573} width={110} height={6} rx={2} fill="rgba(0,0,0,0.10)" transform="rotate(-3, 530, 1576)" />
      </svg>
    </AbsoluteFill>
  );
};
