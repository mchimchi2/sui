import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Character, Mood } from "../components/Character";
import { Background } from "../components/Background";

export type NgWord = {
  id: number;
  phrase: string;
  surface_meaning: string;
  real_meaning: string;
  danger_level: 1 | 2 | 3;
  category: string;
};

// Timing (frames @ 30fps)
const HOOK_END    = 78;   // 0〜2.6s
const PHRASE_END  = 168;  // 2.6〜5.6s
const BRIDGE_END  = 218;  // 5.6〜7.3s
const REVEAL_END  = 338;  // 7.3〜11.3s
const DANGER_END  = 408;  // 11.3〜13.6s
const CTA_END     = 468;  // 13.6〜15.6s

export const DURATION = CTA_END;

const STARS  = { 1: "★☆☆", 2: "★★☆", 3: "★★★" } as const;
const LABELS = { 1: "参考程度", 2: "注意", 3: "要注意！" } as const;

type Phase = { from: number; to: number; text: string; highlight?: string; mood: Mood };

// ── Subtitle renderer (white text + yellow keyword) ──
const Sub: React.FC<{ text: string; highlight?: string; opacity: number; size?: number }> = ({
  text, highlight, opacity, size = 50,
}) => {
  const base: React.CSSProperties = {
    fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif',
    fontSize: size,
    fontWeight: 800,
    lineHeight: 1.55,
    textShadow: "0 2px 10px rgba(0,0,0,0.95), 0 0 24px rgba(0,0,0,0.8)",
  };

  if (!highlight || !text.includes(highlight)) {
    return (
      <span style={{ ...base, color: "#fff", opacity }}>
        {text}
      </span>
    );
  }

  const i = text.indexOf(highlight);
  return (
    <span style={{ opacity }}>
      <span style={{ ...base, color: "#fff" }}>{text.slice(0, i)}</span>
      <span style={{ ...base, color: "#FFD60A", textShadow: "0 2px 10px rgba(0,0,0,0.95), 0 0 24px rgba(255,214,10,0.55)" }}>
        {highlight}
      </span>
      <span style={{ ...base, color: "#fff" }}>{text.slice(i + highlight.length)}</span>
    </span>
  );
};

export const KyujinhyoCard: React.FC<{ word: NgWord }> = ({ word }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fade = (start: number, dur = 12) =>
    interpolate(frame, [start, start + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const sp = (start: number) =>
    spring({ frame: frame - start, fps, config: { damping: 13, stiffness: 180 } });

  // Phase definitions
  const phases: Phase[] = [
    {
      from: 0,          to: HOOK_END,
      text: "この求人票の言葉、本当の意味知ってますか？",
      highlight: "本当の意味",
      mood: "explaining",
    },
    {
      from: HOOK_END,   to: PHRASE_END,
      text: `「${word.phrase}」`,
      highlight: word.phrase,
      mood: "neutral",
    },
    {
      from: PHRASE_END, to: BRIDGE_END,
      text: "でも実は…",
      highlight: "実は",
      mood: "surprised",
    },
    {
      from: BRIDGE_END, to: REVEAL_END,
      text: word.real_meaning,
      highlight: undefined,
      mood: "worried",
    },
    {
      from: REVEAL_END, to: DANGER_END,
      text: `危険度　${STARS[word.danger_level]}　${LABELS[word.danger_level]}`,
      highlight: LABELS[word.danger_level],
      mood: "explaining",
    },
    {
      from: DANGER_END, to: CTA_END,
      text: "転職活動中の人は保存して！",
      highlight: "保存",
      mood: "explaining",
    },
  ];

  const currentPhase = [...phases].reverse().find((p) => frame >= p.from) ?? phases[0];
  const mood = currentPhase.mood;

  // Subtitle font size (shorter text = bigger)
  const subSize =
    currentPhase.text.length > 28 ? 40 :
    currentPhase.text.length > 20 ? 46 : 52;

  // Character subtle bounce on phase transitions
  const bounceFrames = [HOOK_END, PHRASE_END, BRIDGE_END, REVEAL_END, DANGER_END];
  const nearBounce = bounceFrames.some((bf) => frame >= bf && frame < bf + 18);
  const charScale = nearBounce
    ? 1 + interpolate(sp(bounceFrames.find((bf) => frame >= bf && frame < bf + 18)!), [0, 1], [0, 0.03])
    : 1;

  return (
    <AbsoluteFill style={{ fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif' }}>
      {/* Dark cinematic background */}
      <Background />

      {/* ── CHARACTER (centered, large, front-facing) ── */}
      <AbsoluteFill
        style={{
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "center",
          paddingBottom: 460,
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            opacity: fade(0, 18),
            transform: `scale(${charScale})`,
            transformOrigin: "bottom center",
          }}
        >
          <Character mood={mood} scale={2.05} />
        </div>
      </AbsoluteFill>

      {/* ── SUBTITLE AREA (bottom) ── */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-end",
          pointerEvents: "none",
        }}
      >
        {/* Bottom gradient for text readability */}
        <div
          style={{
            position: "absolute",
            bottom: 0, left: 0, right: 0,
            height: 420,
            background: "linear-gradient(to top, rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.45) 55%, transparent 100%)",
          }}
        />

        {/* Category tag (visible only during phrase phase) */}
        {frame >= HOOK_END && frame < BRIDGE_END && (
          <div
            style={{
              opacity: fade(HOOK_END + 6),
              marginBottom: 16,
              background: "rgba(255,255,255,0.14)",
              border: "1px solid rgba(255,255,255,0.28)",
              borderRadius: 50,
              padding: "7px 26px",
              zIndex: 2,
            }}
          >
            <span style={{ color: "rgba(255,255,255,0.85)", fontSize: 26, fontWeight: 600, letterSpacing: 2 }}>
              # {word.category}
            </span>
          </div>
        )}

        {/* Main subtitle text */}
        <div
          style={{
            textAlign: "center",
            padding: "0 64px",
            marginBottom: 80,
            zIndex: 2,
          }}
        >
          <Sub
            text={currentPhase.text}
            highlight={currentPhase.highlight}
            opacity={fade(currentPhase.from, 10)}
            size={subSize}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
