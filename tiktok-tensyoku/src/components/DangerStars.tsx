import React from "react";
import { interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";

type Props = { level: number; delay: number };

export const DangerStars: React.FC<Props> = ({ level, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", gap: 8, justifyContent: "center" }}>
      {[1, 2, 3].map((star) => {
        const starDelay = delay + (star - 1) * 4;
        const opacity = spring({
          frame: frame - starDelay,
          fps,
          config: { damping: 12, stiffness: 200 },
        });
        const scale = spring({
          frame: frame - starDelay,
          fps,
          config: { damping: 8, stiffness: 300 },
        });
        const filled = star <= level;
        return (
          <div
            key={star}
            style={{
              opacity,
              transform: `scale(${scale})`,
              fontSize: 48,
              color: filled ? "#FF3B30" : "#444",
              textShadow: filled ? "0 0 20px rgba(255,59,48,0.8)" : "none",
            }}
          >
            ★
          </div>
        );
      })}
    </div>
  );
};
