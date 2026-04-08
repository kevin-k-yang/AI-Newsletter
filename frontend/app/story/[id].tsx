import { View, Text, StyleSheet, Pressable, Linking, ScrollView } from "react-native";
import { useLocalSearchParams, Stack } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { Colors } from "../../constants/colors";

export default function StoryDetailScreen() {
  const { title, summary, url } = useLocalSearchParams<{
    id: string;
    title: string;
    summary: string;
    url: string;
  }>();

  return (
    <>
      <Stack.Screen options={{ title: "" }} />
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>{title}</Text>
        <View style={styles.divider} />
        <Text style={styles.summary}>{summary}</Text>

        {url ? (
          <Pressable
            style={({ pressed }) => [styles.linkButton, pressed && { opacity: 0.8 }]}
            onPress={() => Linking.openURL(url)}
          >
            <Text style={styles.linkText}>Read full article</Text>
            <Ionicons name="arrow-forward" size={16} color="#ffffff" />
          </Pressable>
        ) : null}
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  content: {
    padding: 24,
    paddingBottom: 60,
  },
  title: {
    fontSize: 26,
    fontWeight: "700",
    color: Colors.text,
    lineHeight: 34,
    letterSpacing: -0.3,
  },
  divider: {
    height: 2,
    width: 40,
    backgroundColor: Colors.text,
    marginVertical: 20,
  },
  summary: {
    fontSize: 17,
    color: Colors.textSecondary,
    lineHeight: 28,
  },
  linkButton: {
    backgroundColor: Colors.accent,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    paddingVertical: 16,
    borderRadius: 12,
    marginTop: 32,
  },
  linkText: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "600",
  },
});
