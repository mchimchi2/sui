import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from "remotion";
import { DangerStars } from "../components/DangerStars";

export type NgWord = {
  id: number;
  phrase: string;
  surface_meaning: string;
  real_meaning: string;
  danger_level: 1 | 2 | 3;
  category: string;
};

// Timing constants (frames at 30fps)
const HOOK_END = 45;        // 0-1.5s  hook
const PHRASE_END = 120;     // 1.5-4s  NGワード表示
const BRIDGE_END = 165;     // 4-5.5s  「実は…」
const REVEAL_END = 270;     // 5.5-9s  本当の意味
const DANGER_END = 345;     // 9-11.5s 危険度
const CTA_END = 390;        // 11.5-13s CTA

export const DURATION = CTA_END;

type Props = { word: NgWord };

export const KyujinhyoCard: React.FC<Props> = ({ word }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = (start: number, duration = 20) =>
    interpolate(frame, [start, start + duration], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  const slideUp = (start: number) =>
    spring({ frame: frame - start, fps, config: { damping: 14, stiffness: 160 } });

  const dangerColor =
    word.danger_level === 3 ? "#FF3B30" : word.danger_level === 2 ? "#FF9500" : "#34C759";

  const dangerLabel =
    word.danger_level === 3 ? "要注意" : word.danger_level === 2 ? "注意" : "参考程度";

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(160deg, #0f0c29 0%, #302b63 50%, #1a1a2e 100%)",
        fontFamily:
          '"Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", sans-serif',
        overflow: "hidden",
      }}
    >
      {/* Background grid lines */}
      <AbsoluteFill
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
      />

      {/* HOOK */}
      <Sequence from={0} durationInFrames={HOOK_END + 15}>
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            padding: "0 60px",
            opacity: frame < HOOK_END ? 1 : fadeIn(HOOK_END, 15) < 0.5 ? 1 - (frame - HOOK_END) / 15 : 0,
          }}
        >
          <div
            style={{
              opacity: fadeIn(0),
              transform: `translateY(${interpolate(slideUp(0), [0, 1], [40, 0])}px)`,
              fontSize: 36,
              color: "#FF3B30",
              fontWeight: 900,
              letterSpacing: 4,
              marginBottom: 20,
            }}
          >
            ⚠️ 求人票 裏読み辞典
          </div>
          <div
            style={{
              opacity: fadeIn(10),
              transform: `translateY(${interpolate(slideUp(10), [0, 1], [40, 0])}px)`,
              fontSize: 44,
              color: "#fff",
              fontWeight: 800,
              textAlign: "center",
              lineHeight: 1.4,
            }}
          >
            この言葉の
            <br />
            本当の意味、
            <br />
            知ってますか？
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* PHRASE */}
      <Sequence from={HOOK_END} durationInFrames={PHRASE_END - HOOK_END + 20}>
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            padding: "0 60px",
            opacity: frame >= PHRASE_END ? interpolate(frame, [PHRASE_END, PHRASE_END + 20], [1, 0], { extrapolateRight: "clamp" }) : 1,
          }}
        >
          <div
            style={{
              opacity: fadeIn(HOOK_END, 15),
              fontSize: 28,
              color: "rgba(255,255,255,0.5)",
              fontWeight: 600,
              letterSpacing: 3,
              marginBottom: 24,
            }}
          >
            # {word.category}
          </div>
          <div
            style={{
              opacity: fadeIn(HOOK_END + 5, 20),
              transform: `scale(${interpolate(slideUp(HOOK_END + 5), [0, 1], [0.7, 1])})`,
              background: "rgba(255,59,48,0.15)",
              border: "3px solid #FF3B30",
              borderRadius: 20,
              padding: "32px 48px",
              textAlign: "center",
            }}
          >
            <div style={{ fontSize: 24, color: "#FF3B30", fontWeight: 700, marginBottom: 12 }}>
              求人票でよく見るこの言葉
            </div>
            <div
              style={{
                fontSize: 58,
                color: "#ffffff",
                fontWeight: 900,
                lineHeight: 1.3,
              }}
            >
              「{word.phrase}」
            </div>
          </div>
          <div
            style={{
              opacity: fadeIn(HOOK_END + 20, 15),
              marginTop: 32,
              fontSize: 30,
              color: "rgba(255,255,255,0.6)",
              textAlign: "center",
              lineHeight: 1.6,
            }}
          >
            表向きの意味は
            <br />
            「{word.surface_meaning}」
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* BRIDGE */}
      <Sequence from={PHRASE_END} durationInFrames={BRIDGE_END - PHRASE_END + 15}>
        <AbsoluteFill
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            opacity: frame >= BRIDGE_END ? interpolate(frame, [BRIDGE_END, BRIDGE_END + 15], [1, 0], { extrapolateRight: "clamp" }) : 1,
          }}
        >
          <div
            style={{
              opacity: fadeIn(PHRASE_END, 10),
              transform: `scale(${interpolate(slideUp(PHRASE_END), [0, 1], [0.5, 1])})`,
              fontSize: 80,
              color: "#FF9500",
              fontWeight: 900,
              textAlign: "center",
              lineHeight: 1.4,
            }}
          >
            でも実は…
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* REVEAL */}
      <Sequence from={BRIDGE_END} durationInFrames={REVEAL_END - BRIDGE_END + 20}>
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            padding: "0 60px",
            opacity: frame >= REVEAL_END ? interpolate(frame, [REVEAL_END, REVEAL_END + 20], [1, 0], { extrapolateRight: "clamp" }) : 1,
          }}
        >
          <div
            style={{
              opacity: fadeIn(BRIDGE_END, 10),
              fontSize: 30,
              color: "#FF3B30",
              fontWeight: 800,
              letterSpacing: 4,
              marginBottom: 28,
            }}
          >
            💀 本当の意味
          </div>
          <div
            style={{
              opacity: fadeIn(BRIDGE_END + 8, 25),
              transform: `translateY(${interpolate(slideUp(BRIDGE_END + 8), [0, 1], [50, 0])}px)`,
              background: "rgba(255,59,48,0.2)",
              border: "2px solid rgba(255,59,48,0.6)",
              borderRadius: 24,
              padding: "40px 48px",
              textAlign: "center",
            }}
          >
            <div
              style={{
                fontSize: 48,
                color: "#ffffff",
                fontWeight: 800,
                lineHeight: 1.5,
              }}
            >
              {word.real_meaning}
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* DANGER LEVEL */}
      <Sequence from={REVEAL_END} durationInFrames={DANGER_END - REVEAL_END + 15}>
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 24,
            opacity: frame >= DANGER_END ? interpolate(frame, [DANGER_END, DANGER_END + 15], [1, 0], { extrapolateRight: "clamp" }) : 1,
          }}
        >
          <div style={{ opacity: fadeIn(REVEAL_END, 15), fontSize: 36, color: "#fff", fontWeight: 700 }}>
            危険度
          </div>
          <DangerStars level={word.danger_level} delay={REVEAL_END + 10} />
          <div
            style={{
              opacity: fadeIn(REVEAL_END + 20, 15),
              background: dangerColor,
              borderRadius: 50,
              padding: "12px 40px",
              fontSize: 36,
              color: "#fff",
              fontWeight: 900,
              letterSpacing: 4,
            }}
          >
            {dangerLabel}
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* CTA */}
      <Sequence from={DANGER_END} durationInFrames={CTA_END - DANGER_END}>
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 28,
            padding: "0 60px",
          }}
        >
          <div
            style={{
              opacity: fadeIn(DANGER_END, 15),
              transform: `scale(${interpolate(slideUp(DANGER_END), [0, 1], [0.8, 1])})`,
              fontSize: 44,
              color: "#fff",
              fontWeight: 900,
              textAlign: "center",
              lineHeight: 1.5,
            }}
          >
            転職活動中の人は
            <br />
            保存して活用して！
          </div>
          <div style={{ opacity: fadeIn(DANGER_END + 15, 15), fontSize: 30, color: "rgba(255,255,255,0.6)", textAlign: "center", lineHeight: 1.8 }}>
            #転職 #求人票 #ブラック企業
            <br />
            #転職活動 #仕事探し
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
