import { ScrollView, View, Text, StyleSheet, RefreshControl } from "react-native";
import { useState, useCallback, useEffect } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { mockDigest } from "../data/mockDigest";
import { DailyDigest, Substory } from "../types";
import { Colors } from "../constants/colors";
import { API_URL } from "../constants/api";
import SectionCard from "../components/SectionCard";

async function fetchDigest(): Promise<DailyDigest | null> {
  try {
    const res = await fetch(`${API_URL}/digest/today`);
    return await res.json();
  } catch {
    return null;
  }
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

export default function HomeScreen() {
  const insets = useSafeAreaInsets();
  const [digest, setDigest] = useState<DailyDigest>(mockDigest);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchDigest().then((data) => {
      if (data) setDigest(data);
    });
  }, []);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    const data = await fetchDigest();
    if (data) setDigest(data);
    setRefreshing(false);
  }, []);

  const handleFeedback = useCallback(
    async (articleId: string, reaction: "like" | "dislike") => {
      try {
        const res = await fetch(`${API_URL}/feedback`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            article_id: articleId,
            reaction,
            timestamp: new Date().toISOString(),
          }),
        });
        const data = await res.json();

        // If dislike returned a replacement, swap it in
        if (reaction === "dislike" && data.replacement) {
          setDigest((prev) => ({
            ...prev,
            sections: prev.sections.map((sec) =>
              sec.section === data.section
                ? {
                    ...sec,
                    substories: sec.substories.map((s) =>
                      s.id === articleId ? (data.replacement as Substory) : s
                    ),
                  }
                : sec
            ),
          }));
        }
      } catch {
        // Silent fail
      }
    },
    []
  );

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={[styles.content, { paddingTop: insets.top + 20 }]}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#999" />
      }
      showsVerticalScrollIndicator={false}
    >
      <View style={styles.header}>
        <Text style={styles.title}>Daily Digest</Text>
        <Text style={styles.date}>{formatDate(digest.date)}</Text>
      </View>

      {digest.sections.map((section, i) => (
        <View key={section.section}>
          {i > 0 && <View style={styles.sectionDivider} />}
          <SectionCard section={section} onFeedback={handleFeedback} />
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  content: {
    paddingHorizontal: 20,
    paddingBottom: 60,
  },
  header: {
    marginBottom: 32,
  },
  title: {
    fontSize: 32,
    fontWeight: "800",
    color: Colors.text,
    letterSpacing: -0.5,
  },
  date: {
    fontSize: 15,
    color: Colors.textTertiary,
    marginTop: 4,
  },
  sectionDivider: {
    height: 1,
    backgroundColor: Colors.divider,
    marginVertical: 8,
  },
});
