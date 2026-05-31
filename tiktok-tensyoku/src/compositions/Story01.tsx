import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CharacterSuit, SuitMood } from "../components/CharacterSuit";
import { Background } from "../components/Background";

export const STORY01_DURATION = 1800; // 60s @ 30fps

type Phase = {
  from: number;
  to: number;
  text: string;
  highlight?: string;
  mood: SuitMood;
  size?: number;
  impact?: boolean;
  showCard?: boolean;
  cardText?: string;
  label?: string;
};

const PHASES: Phase[] = [
  // ① HOOK 0-2s (0-60f)
  {
    from: 0, to: 60,
    text: "転職したいと妻に\n相談した夜のこと",
    highlight: "妻に",
    mood: "neutral", size: 52, label: "HOOK",
  },
  // ② BOMBSHELL 2-5s (60-150f)
  {
    from: 60, to: 150,
    text: "「あなたには、\nもう無理よ」",
    highlight: "もう無理よ",
    mood: "shocked", size: 56, impact: true, label: "CRISIS",
  },
  // ③ BACKSTORY 5-12s (150-360f)
  {
    from: 150, to: 270,
    text: "年収420万円。\n15年間、昇進なし。",
    highlight: "15年間、昇進なし",
    mood: "worried", size: 48, label: "STORY",
  },
  {
    from: 270, to: 360,
    text: "毎朝、会社に向かうのが\n怖かった",
    highlight: "怖かった",
    mood: "worried", size: 50, label: "STORY",
  },
  // ④ TURNING POINT 12-20s (360-600f)
  {
    from: 360, to: 480,
    text: "それでも動けなかった。\n妻の言葉が頭から離れない",
    highlight: undefined,
    mood: "worried", size: 44, label: "STORY",
  },
  {
    from: 480, to: 600,
    text: "思い切って\n転職エージェントに電話した",
    highlight: "転職エージェント",
    mood: "explaining", size: 46, label: "STORY",
  },
  // ⑤ REVELATION 20-28s (600-840f)
  {
    from: 600, to: 840,
    text: "「40代こそ企業が\n一番欲しい年代です」",
    highlight: "40代こそ",
    mood: "shocked", size: 46, impact: true, label: "HOPE",
  },
  // ⑥ WHY 28-38s (840-1140f)
  {
    from: 840, to: 960,
    text: "①即戦力として\n現場を動かせる",
    highlight: "即戦力",
    mood: "explaining", size: 48, label: "HOPE",
  },
  {
    from: 960, to: 1050,
    text: "②チームを\nまとめる力がある",
    highlight: "チームをまとめる力",
    mood: "explaining", size: 48, label: "HOPE",
  },
  {
    from: 1050, to: 1140,
    text: "③若手より\n定着率が高い",
    highlight: "定着率が高い",
    mood: "explaining", size: 48, label: "HOPE",
  },
  // ⑦ RESULT 38-48s (1140-1440f)
  {
    from: 1140, to: 1290,
    text: "3ヶ月後、\n年収560万円で転職成功",
    highlight: "年収560万円",
    mood: "happy", size: 48, impact: true,
    showCard: true, cardText: "年収 ＋140万円↑", label: "RESULT",
  },
  {
    from: 1290, to: 1440,
    text: "残業は月12時間。\n月曜日が待ち遠しい。",
    highlight: "月曜日が待ち遠しい",
    mood: "happy", size: 46, label: "RESULT",
  },
  // ⑧ EMOTIONAL CLOSE 48-55s (1440-1650f)
  {
    from: 1440, to: 1650,
    text: "「無理」と言われた自分が\n挑戦してよかった",
    highlight: "挑戦してよかった",
    mood: "happy", size: 46, label: "RESULT",
  },
  // ⑨ CTA 55-60s (1650-1800f)
  {
    from: 1650, to: 1800,
    text: "同じ状況の40代へ。\nプロフィールの無料相談リンクへ",
    highlight: "無料相談リンク",
    mood: "explaining", size: 40, label: "",
  },
];

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

export const Story01: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fade = (start: number, dur = 10) =>
    interpolate(frame, [start, start + dur], [0, 1], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    });

  const sp = (start: number, cfg = {}) =>
    spring({ frame: frame - start, fps, config: { damping: 14, stiffness: 180, ...cfg } });

  const phase = [...PHASES].reverse().find((p) => frame >= p.from) ?? PHASES[0];
  const mood = phase.mood;

  const isImpact = phase.impact && frame >= phase.from && frame < phase.from + 8;
  const flashOpacity = isImpact
    ? interpolate(frame, [phase.from, phase.from + 8], [0.55, 0], { extrapolateRight: "clamp" })
    : 0;

  const impactScale = phase.impact
    ? interpolate(sp(phase.from, { stiffness: 300, damping: 20 }), [0, 1], [1.06, 1])
    : 1;

  const subOpacity = fade(phase.from, 12);

  const phaseStarts = PHASES.map((p) => p.from);
  const nearTransition = phaseStarts.find((bf) => frame >= bf && frame < bf + 16);
  const charScale = nearTransition !== undefined
    ? 1 + interpolate(sp(nearTransition, { stiffness: 250, damping: 15 }), [0, 1], [0, 0.025])
    : 1;

  const showCard = phase.showCard && frame >= phase.from;
  const cardScale = showCard
    ? interpolate(sp(phase.from + 8, { stiffness: 200, damping: 12 }), [0, 1], [0.5, 1])
    : 1;
  const cardOpacity = showCard ? fade(phase.from + 8, 14) : 0;

  const progress = interpolate(frame, [0, STORY01_DURATION], [0, 100], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif' }}>
      <div style={{ transform: `scale(${impactScale})`, width: "100%", height: "100%", transformOrigin: "center center" }}>
        <Background />
      </div>

      {/* Progress bar */}
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 4, background: "rgba(255,255,255,0.15)", zIndex: 10 }}>
        <div style={{ width: `${progress}%`, height: "100%", background: "#FFD60A" }} />
      </div>

      {/* Impact flash */}
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
          <CharacterSuit mood={mood} scale={2.05} />
        </div>
      </AbsoluteFill>

      {/* RESULT CARD */}
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
        <div style={{
          position: "absolute", bottom: 0, left: 0, right: 0, height: 440,
          background: "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.45) 60%, transparent 100%)",
        }} />

        {phase.label && (
          <div style={{
            opacity: 0.5, fontSize: 22, color: "#fff",
            marginBottom: 12, letterSpacing: 3,
            fontFamily: '"Hiragino Sans","Noto Sans JP",sans-serif',
            fontWeight: 500,
            zIndex: 2,
          }}>
            {phase.label}
          </div>
        )}

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
