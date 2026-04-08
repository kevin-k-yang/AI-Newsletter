import { View, Text, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { SectionSummary } from "../types";
import { Colors, SectionLabels, SectionIcons } from "../constants/colors";
import SubstoryCard from "./SubstoryCard";

interface Props {
  section: SectionSummary;
  onFeedback: (articleId: string, reaction: "like" | "dislike") => void;
}

const sectionColors: Record<string, string> = {
  sports: Colors.sports,
  tech: Colors.tech,
  finance: Colors.finance,
  world: Colors.world,
};

export default function SectionCard({ section, onFeedback }: Props) {
  const color = sectionColors[section.section];

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Ionicons
          name={SectionIcons[section.section] as any}
          size={18}
          color={color}
        />
        <Text style={[styles.label, { color }]}>
          {SectionLabels[section.section]}
        </Text>
      </View>

      <Text style={styles.summary}>{section.summary}</Text>

      <View style={styles.substories}>
        {section.substories.map((substory, i) => (
          <SubstoryCard
            key={substory.id}
            substory={substory}
            accentColor={color}
            isLast={i === section.substories.length - 1}
            onFeedback={onFeedback}
          />
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingVertical: 20,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 12,
  },
  label: {
    fontSize: 14,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  summary: {
    fontSize: 15,
    color: Colors.textSecondary,
    lineHeight: 23,
    marginBottom: 20,
  },
  substories: {},
});
