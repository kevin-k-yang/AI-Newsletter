import { useState } from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { Substory } from "../types";
import { Colors } from "../constants/colors";

interface Props {
  substory: Substory;
  accentColor: string;
  isLast?: boolean;
  onFeedback: (articleId: string, reaction: "like" | "dislike") => void;
}

export default function SubstoryCard({ substory, accentColor, isLast, onFeedback }: Props) {
  const router = useRouter();
  const [reaction, setReaction] = useState<"like" | "dislike" | null>(null);

  const handleReaction = (type: "like" | "dislike") => {
    const newReaction = reaction === type ? null : type;
    setReaction(newReaction);
    if (newReaction) {
      onFeedback(substory.id, newReaction);
    }
  };

  return (
    <Pressable
      style={({ pressed }) => [
        styles.card,
        !isLast && styles.cardBorder,
        pressed && styles.cardPressed,
      ]}
      onPress={() =>
        router.push({
          pathname: "/story/[id]",
          params: {
            id: substory.id,
            title: substory.title,
            summary: substory.summary,
            url: substory.url,
          },
        })
      }
    >
      <View style={styles.content}>
        <Text style={styles.title}>{substory.title}</Text>
        <Text style={styles.summary}>{substory.summary}</Text>
        <View style={styles.actions}>
          <Pressable
            onPress={(e) => {
              e.stopPropagation();
              handleReaction("like");
            }}
            hitSlop={8}
            style={[
              styles.button,
              reaction === "like" && { backgroundColor: Colors.likeActive },
            ]}
          >
            <Ionicons
              name={reaction === "like" ? "arrow-up-circle" : "arrow-up-circle-outline"}
              size={18}
              color={reaction === "like" ? Colors.like : Colors.textTertiary}
            />
          </Pressable>
          <Pressable
            onPress={(e) => {
              e.stopPropagation();
              handleReaction("dislike");
            }}
            hitSlop={8}
            style={[
              styles.button,
              reaction === "dislike" && { backgroundColor: Colors.dislikeActive },
            ]}
          >
            <Ionicons
              name={reaction === "dislike" ? "arrow-down-circle" : "arrow-down-circle-outline"}
              size={18}
              color={reaction === "dislike" ? Colors.dislike : Colors.textTertiary}
            />
          </Pressable>
        </View>
      </View>
      <Ionicons name="chevron-forward" size={16} color={Colors.textTertiary} style={styles.chevron} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 14,
  },
  cardBorder: {
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: Colors.border,
  },
  cardPressed: {
    opacity: 0.6,
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: 16,
    fontWeight: "600",
    color: Colors.text,
    marginBottom: 4,
    lineHeight: 22,
  },
  summary: {
    fontSize: 14,
    color: Colors.textSecondary,
    lineHeight: 20,
    marginBottom: 8,
  },
  actions: {
    flexDirection: "row",
    gap: 4,
  },
  button: {
    padding: 4,
    borderRadius: 20,
  },
  chevron: {
    marginLeft: 12,
  },
});
