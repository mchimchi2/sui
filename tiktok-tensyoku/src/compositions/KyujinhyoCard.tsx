import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from "remotion";
import { Character } from "../components/Character";
import { Background } from "../components/Background";
import { DangerStars } from "../components/DangerStars";

export type NgWord = {
  id: number;
  phrase: string;
  surface_meaning: string;
  real_meaning: string;
  danger_level: 1 | 2 | 3;
  category: string;
};

// Timing (frames @ 30fps)
const HOOK_END    = 50;   // 0〜1.7s
const PHRASE_END  = 130;  // 1.7〜4.3s
const BRIDGE_END  = 175;  // 4.3〜5.8s
const REVEAL_END  = 285;  // 5.8〜9.5s
const DANGER_END  = 360;  // 9.5〜12s
const CTA_END     = 420;  // 12〜14s

export const DURATION = CTA_END;

type Props = { word: NgWord };

const dangerMeta = {
  1: { color: "#34C759", label: "参考程度", bg: "rgba(52,199,89,0.15)" },
  2: { color: "#FF9500", label: "注意",     bg: "rgba(255,149,0,0.15)"  },
  3: { color: "#FF3B30", label: "要注意！", bg: "rgba(255,59,48,0.15)"  },
} as const;

export const KyujinhyoCard: React.FC<Props> = ({ word }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const sp = (start: number, cfg = {}) =>
    spring({ frame: frame - start, fps, config: { damping: 14, stiffness: 160, ...cfg } });

  const fade = (start: number, dur = 18) =>
    interpolate(frame, [start, start + dur], [0, 1], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    });

  const fadeOut = (start: number, dur = 12) =>
    interpolate(frame, [start, start + dur], [1, 0], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    });

  const slideY = (start: number, from = 40) =>
    interpolate(sp(start), [0, 1], [from, 0]);

  const { color, label, bg } = dangerMeta[word.danger_level as 1|2|3];

  // Character mood per phase
  const mood =
    frame < PHRASE_END  ? "explaining" :
    frame < BRIDGE_END  ? "neutral"    :
    frame < REVEAL_END  ? "surprised"  :
    frame < DANGER_END  ? "worried"    : "explaining";

  // Character bounce on BRIDGE
  const charBounce =
    frame >= BRIDGE_END - 5 && frame < BRIDGE_END + 20
      ? Math.sin((frame - BRIDGE_END) * 0.6) * 18
      : 0;

  return (
    <AbsoluteFill style={{ fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif' }}>
      <Background />

      {/* ===== HOOK ===== */}
      <Sequence from={0} durationInFrames={HOOK_END + 12}>
        <AbsoluteFill
          style={{
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "flex-start",
            paddingTop: 100,
            opacity: frame > HOOK_END ? fadeOut(HOOK_END) : 1,
          }}
        >
          <div
            style={{
              opacity: fade(0), transform: `translateY(${slideY(0)}px)`,
              background: "#2D4A8F", borderRadius: 16,
              padding: "18px 44px", marginBottom: 24,
            }}
          >
            <span style={{ color: "#fff", fontSize: 32, fontWeight: 900, letterSpacing: 3 }}>
              ⚠️ 求人票 裏読み辞典
            </span>
          </div>
          <div
            style={{
              opacity: fade(12), transform: `translateY(${slideY(12)}px)`,
              fontSize: 52, fontWeight: 900, color: "#1a1a1a",
              textAlign: "center", lineHeight: 1.45,
              textShadow: "0 2px 12px rgba(255,255,255,0.9)",
            }}
          >
            この求人票の言葉<br />
            本当の意味<br />
            知ってますか？
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* ===== NG PHRASE ===== */}
      <Sequence from={HOOK_END} durationInFrames={PHRASE_END - HOOK_END + 12}>
        <AbsoluteFill
          style={{
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "flex-start",
            paddingTop: 90,
            opacity: frame > PHRASE_END ? fadeOut(PHRASE_END) : 1,
          }}
        >
          {/* Category tag */}
          <div style={{ opacity: fade(HOOK_END), marginBottom: 20 }}>
            <span style={{
              background: "#FF6B35", color: "#fff",
              borderRadius: 50, padding: "8px 28px",
              fontSize: 28, fontWeight: 700, letterSpacing: 2,
            }}>
              # {word.category}
            </span>
          </div>

          {/* NGワード card */}
          <div
            style={{
              opacity: fade(HOOK_END + 6),
              transform: `scale(${interpolate(sp(HOOK_END + 6), [0, 1], [0.85, 1])})`,
              background: "rgba(255,255,255,0.92)",
              border: `4px solid #2D4A8F`,
              borderRadius: 24, padding: "32px 48px",
              textAlign: "center", marginBottom: 28,
              boxShadow: "0 8px 32px rgba(45,74,143,0.18)",
              maxWidth: 900,
            }}
          >
            <div style={{ fontSize: 26, color: "#FF6B35", fontWeight: 700, marginBottom: 10 }}>
              求人票によく書かれている言葉
            </div>
            <div style={{ fontSize: 62, color: "#1a1a1a", fontWeight: 900, lineHeight: 1.3 }}>
              「{word.phrase}」
            </div>
          </div>

          {/* Surface meaning */}
          <div
            style={{
              opacity: fade(HOOK_END + 22),
              transform: `translateY(${slideY(HOOK_END + 22)}px)`,
              background: "rgba(255,255,255,0.75)", borderRadius: 16,
              padding: "18px 36px", textAlign: "center",
              maxWidth: 860,
            }}
          >
            <span style={{ fontSize: 30, color: "#555", lineHeight: 1.6 }}>
              表向き「{word.surface_meaning}」
            </span>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* ===== BRIDGE ===== */}
      <Sequence from={PHRASE_END} durationInFrames={BRIDGE_END - PHRASE_END + 12}>
        <AbsoluteFill
          style={{
            display: "flex", alignItems: "center", justifyContent: "center",
            opacity: frame > BRIDGE_END ? fadeOut(BRIDGE_END) : 1,
          }}
        >
          <div
            style={{
              opacity: fade(PHRASE_END, 10),
              transform: `scale(${interpolate(sp(PHRASE_END, { stiffness: 300, damping: 10 }), [0, 1], [0.5, 1])})`,
              fontSize: 92, fontWeight: 900,
              color: "#2D4A8F",
              textAlign: "center", lineHeight: 1.3,
              textShadow: "0 4px 20px rgba(45,74,143,0.25)",
            }}
          >
            でも実は…
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* ===== REAL MEANING ===== */}
      <Sequence from={BRIDGE_END} durationInFrames={REVEAL_END - BRIDGE_END + 12}>
        <AbsoluteFill
          style={{
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "flex-start",
            paddingTop: 80,
            opacity: frame > REVEAL_END ? fadeOut(REVEAL_END) : 1,
          }}
        >
          <div style={{ opacity: fade(BRIDGE_END, 10), marginBottom: 20 }}>
            <span style={{
              background: color, color: "#fff",
              borderRadius: 50, padding: "10px 36px",
              fontSize: 30, fontWeight: 900, letterSpacing: 3,
            }}>
              💀 本当の意味
            </span>
          </div>
          <div
            style={{
              opacity: fade(BRIDGE_END + 8),
              transform: `translateY(${slideY(BRIDGE_END + 8, 50)}px)`,
              background: "rgba(255,255,255,0.93)",
              border: `4px solid ${color}`,
              borderRadius: 24, padding: "36px 48px",
              textAlign: "center",
              boxShadow: `0 8px 40px ${bg}`,
              maxWidth: 920,
            }}
          >
            <div style={{ fontSize: 50, color: "#1a1a1a", fontWeight: 800, lineHeight: 1.5 }}>
              {word.real_meaning}
            </div>
          </div>

          {/* Speech bubble from character */}
          <div
            style={{
              opacity: fade(BRIDGE_END + 25),
              transform: `translateY(${slideY(BRIDGE_END + 25, 30)}px)`,
              marginTop: 28, background: "#fff",
              border: "3px solid #2D4A8F", borderRadius: 16,
              padding: "14px 32px",
              position: "relative",
            }}
          >
            <div style={{ fontSize: 28, color: "#2D4A8F", fontWeight: 700 }}>
              ← 僕も入社前に知りたかった…
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* ===== DANGER LEVEL ===== */}
      <Sequence from={REVEAL_END} durationInFrames={DANGER_END - REVEAL_END + 12}>
        <AbsoluteFill
          style={{
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "center",
            gap: 24,
            opacity: frame > DANGER_END ? fadeOut(DANGER_END) : 1,
          }}
        >
          <div style={{ opacity: fade(REVEAL_END, 12), fontSize: 38, color: "#1a1a1a", fontWeight: 800 }}>
            危険度
          </div>
          <DangerStars level={word.danger_level} delay={REVEAL_END + 10} />
          <div
            style={{
              opacity: fade(REVEAL_END + 22),
              transform: `scale(${interpolate(sp(REVEAL_END + 22), [0, 1], [0.7, 1])})`,
              background: color, borderRadius: 50,
              padding: "16px 52px",
              fontSize: 40, color: "#fff", fontWeight: 900, letterSpacing: 4,
            }}
          >
            {label}
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* ===== CTA ===== */}
      <Sequence from={DANGER_END} durationInFrames={CTA_END - DANGER_END}>
        <AbsoluteFill
          style={{
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "flex-start",
            paddingTop: 100, gap: 24,
          }}
        >
          <div
            style={{
              opacity: fade(DANGER_END),
              transform: `scale(${interpolate(sp(DANGER_END), [0, 1], [0.85, 1])})`,
              background: "#2D4A8F", borderRadius: 20,
              padding: "28px 52px", textAlign: "center",
              boxShadow: "0 8px 32px rgba(45,74,143,0.3)",
            }}
          >
            <div style={{ fontSize: 46, color: "#fff", fontWeight: 900, lineHeight: 1.5 }}>
              転職活動中の人は<br />保存して活用して！
            </div>
          </div>
          <div style={{ opacity: fade(DANGER_END + 18), fontSize: 28, color: "#555", textAlign: "center", lineHeight: 2 }}>
            #転職 #求人票 #ブラック企業<br />#転職活動 #仕事探し
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* ===== CHARACTER (always visible, reacts to phase) ===== */}
      <AbsoluteFill
        style={{
          display: "flex", alignItems: "flex-end",
          justifyContent: "flex-end",
          paddingBottom: 340, paddingRight: 40,
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            opacity: fade(6),
            transform: `translateY(${charBounce}px)`,
          }}
        >
          <Character mood={mood} scale={1.1} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
