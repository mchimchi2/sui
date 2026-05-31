import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Character, Mood } from "../components/Character";
import { Background } from "../components/Background";

export const STORY_DURATION = 1800; // 60s @ 30fps

// ── Story phases ──────────────────────────────────────────
type Phase = {
  from: number;
  to: number;
  text: string;
  highlight?: string;
  mood: Mood;
  size?: number;
  impact?: boolean;     // Flash + zoom on entry
  showCard?: boolean;   // Floating result card
  cardText?: string;
};

const PHASES: Phase[] = [
  // ① HOOK
  {
    from: 0, to: 210,
    text: "45歳で突然\nリストラを告げられました",
    highlight: "リストラ",
    mood: "worried", size: 52, impact: true,
  },
  // ② Backstory 1
  {
    from: 210, to: 420,
    text: "20年間、朝7時から深夜まで働いた",
    highlight: "20年間",
    mood: "explaining", size: 46,
  },
  // ③ Backstory 2
  {
    from: 420, to: 610,
    text: "それでも後輩に\n次々と追い抜かれていく",
    highlight: "後輩に次々と追い抜かれ",
    mood: "worried", size: 42,
  },
  // ④ Crisis setup
  {
    from: 610, to: 790,
    text: "ある日、部長室に呼ばれた",
    highlight: undefined,
    mood: "surprised", size: 52,
  },
  // ⑤ THE BOMBSHELL
  {
    from: 790, to: 1000,
    text: "「早期退職制度を\n使ってほしい」",
    highlight: "早期退職制度",
    mood: "surprised", size: 50, impact: true,
  },
  // ⑥ Despair
  {
    from: 1000, to: 1185,
    text: "妻にも言えず3日間、\nひとりで抱え込んだ",
    highlight: "3日間",
    mood: "worried", size: 46,
  },
  // ⑦ Turning point
  {
    from: 1185, to: 1365,
    text: "初めて転職エージェントに\n電話した",
    highlight: "転職エージェント",
    mood: "neutral", size: 48,
  },
  // ⑧ HOPE
  {
    from: 1365, to: 1530,
    text: "「45歳でも動ける市場があります」\n—その言葉で泣きそうになった",
    highlight: "45歳でも動ける",
    mood: "surprised", size: 38,
  },
  // ⑨ RESULT
  {
    from: 1530, to: 1680,
    text: "3ヶ月後、年収130万円アップで\n転職成功",
    highlight: "年収130万円アップ",
    mood: "explaining", size: 44,
    showCard: true, cardText: "年収 ＋130万円↑",
  },
  // ⑩ CTA
  {
    from: 1680, to: 1800,
    text: "同じ悩みがある人へ\nプロフィールの無料相談リンクへ",
    highlight: "無料相談",
    mood: "explaining", size: 42,
  },
];

// ── Subtitle component ─────────────────────────────────────
const Sub: React.FC<{
  text: string; highlight?: string; opacity: number; size: number;
}> = ({ text, highlight, opacity, size }) => {
  const base: React.CSSProperties = {
    fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif',
    fontSize: size,
    fontWeight: 800,
    lineHeight: 1.6,
    textShadow: "0 2px 12px rgba(0,0,0,0.98), 0 0 28px rgba(0,0,0,0.9)",
    whiteSpace: "pre-wrap",
    textAlign: "center",
  };

  if (!highlight || !text.includes(highlight)) {
    return <span style={{ ...base, color: "#fff", opacity }}>{text}</span>;
  }

  const i = text.indexOf(highlight);
  return (
    <span style={{ opacity }}>
      <span style={{ ...base, color: "#fff" }}>{text.slice(0, i)}</span>
      <span style={{
        ...base, color: "#FFD60A",
        textShadow: "0 2px 12px rgba(0,0,0,0.98), 0 0 28px rgba(255,214,10,0.6)",
      }}>{highlight}</span>
      <span style={{ ...base, color: "#fff" }}>{text.slice(i + highlight.length)}</span>
    </span>
  );
};

// ── Main composition ───────────────────────────────────────
export const TensyokuStory: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fade = (start: number, dur = 10) =>
    interpolate(frame, [start, start + dur], [0, 1], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    });

  const sp = (start: number, cfg = {}) =>
    spring({ frame: frame - start, fps, config: { damping: 14, stiffness: 180, ...cfg } });

  // Current phase
  const phase = [...PHASES].reverse().find((p) => frame >= p.from) ?? PHASES[0];
  const mood = phase.mood;

  // Impact flash on phase entry (for phases with impact: true)
  const isImpact = phase.impact && frame >= phase.from && frame < phase.from + 8;
  const flashOpacity = isImpact
    ? interpolate(frame, [phase.from, phase.from + 8], [0.55, 0], { extrapolateRight: "clamp" })
    : 0;

  // Phase-entry zoom for impact phases
  const impactScale = phase.impact
    ? interpolate(sp(phase.from, { stiffness: 300, damping: 20 }), [0, 1], [1.06, 1])
    : 1;

  // Subtitle fade-in on each phase change
  const subOpacity = fade(phase.from, 12);

  // Character scale bounce at phase transitions
  const phaseStarts = PHASES.map((p) => p.from);
  const nearTransition = phaseStarts.find((bf) => frame >= bf && frame < bf + 16);
  const charScale = nearTransition !== undefined
    ? 1 + interpolate(sp(nearTransition, { stiffness: 250, damping: 15 }), [0, 1], [0, 0.025])
    : 1;

  // Result card animation (phase ⑨)
  const showCard = phase.showCard && frame >= phase.from;
  const cardScale = showCard
    ? interpolate(sp(phase.from + 8, { stiffness: 200, damping: 12 }), [0, 1], [0.5, 1])
    : 1;
  const cardOpacity = showCard ? fade(phase.from + 8, 14) : 0;

  // Progress bar (thin line at top)
  const progress = interpolate(frame, [0, STORY_DURATION], [0, 100], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif' }}>
      {/* Background */}
      <div style={{ transform: `scale(${impactScale})`, width: "100%", height: "100%", transformOrigin: "center center" }}>
        <Background />
      </div>

      {/* Progress bar */}
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 4, background: "rgba(255,255,255,0.15)", zIndex: 10 }}>
        <div style={{ width: `${progress}%`, height: "100%", background: "#FFD60A", transition: "none" }} />
      </div>

      {/* Impact flash overlay */}
      {flashOpacity > 0 && (
        <div style={{
          position: "absolute", inset: 0, zIndex: 9,
          background: "white", opacity: flashOpacity,
          pointerEvents: "none",
        }} />
      )}

      {/* CHARACTER */}
      <AbsoluteFill style={{
        display: "flex", alignItems: "flex-end",
        justifyContent: "center", paddingBottom: 460,
        pointerEvents: "none",
      }}>
        <div style={{
          opacity: fade(0, 18),
          transform: `scale(${charScale})`,
          transformOrigin: "bottom center",
        }}>
          <Character mood={mood} scale={2.05} />
        </div>
      </AbsoluteFill>

      {/* RESULT CARD (floats near character) */}
      {showCard && (
        <AbsoluteFill style={{
          display: "flex", alignItems: "flex-end",
          justifyContent: "flex-end",
          paddingBottom: 900, paddingRight: 80,
          pointerEvents: "none",
        }}>
          <div style={{
            opacity: cardOpacity,
            transform: `scale(${cardScale})`,
            background: "#FFD60A",
            borderRadius: 20,
            padding: "20px 36px",
            boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
          }}>
            <div style={{
              fontSize: 42, fontWeight: 900, color: "#111",
              fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif',
              lineHeight: 1.3,
            }}>
              {phase.cardText}
            </div>
          </div>
        </AbsoluteFill>
      )}

      {/* SUBTITLE AREA */}
      <AbsoluteFill style={{
        display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "flex-end",
        pointerEvents: "none",
      }}>
        {/* Gradient backing */}
        <div style={{
          position: "absolute", bottom: 0, left: 0, right: 0, height: 440,
          background: "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.45) 60%, transparent 100%)",
        }} />

        {/* Phase counter */}
        <div style={{
          opacity: 0.5, fontSize: 22, color: "#fff",
          marginBottom: 12, letterSpacing: 3,
          fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif',
          fontWeight: 500,
          zIndex: 2,
        }}>
          {frame < 210 ? "HOOK" :
           frame < 790 ? "STORY" :
           frame < 1185 ? "CRISIS" :
           frame < 1530 ? "HOPE" :
           frame < 1680 ? "RESULT" : ""}
        </div>

        {/* Main subtitle */}
        <div style={{ zIndex: 2, textAlign: "center", padding: "0 60px", marginBottom: 80 }}>
          <Sub
            text={phase.text}
            highlight={phase.highlight}
            opacity={subOpacity}
            size={phase.size ?? 46}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
