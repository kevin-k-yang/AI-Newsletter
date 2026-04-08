export const Colors = {
  background: "#ffffff",
  surface: "#f6f6f8",
  card: "#ffffff",
  text: "#111111",
  textSecondary: "#555555",
  textTertiary: "#999999",
  border: "#ebebeb",
  divider: "#f0f0f0",
  sports: "#e63946",
  tech: "#457b9d",
  finance: "#2a9d8f",
  world: "#6c5ce7",
  like: "#2a9d8f",
  dislike: "#e63946",
  likeActive: "#d4f5ef",
  dislikeActive: "#fde8ea",
  accent: "#111111",
} as const;

export const SectionLabels: Record<string, string> = {
  sports: "Sports",
  tech: "Tech",
  finance: "Finance",
  world: "World",
};

export const SectionIcons: Record<string, string> = {
  sports: "football-outline",
  tech: "hardware-chip-outline",
  finance: "trending-up-outline",
  world: "globe-outline",
};
