export interface Substory {
  id: string;
  title: string;
  summary: string;
  url: string;
}

export interface SectionSummary {
  section: "sports" | "tech" | "finance" | "world";
  summary: string;
  substories: [Substory, Substory, Substory];
}

export interface DailyDigest {
  date: string;
  sections: SectionSummary[];
}

export interface Feedback {
  article_id: string;
  reaction: "like" | "dislike";
  timestamp: string;
}
