import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';

export default function PortfolioScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>投資組合</Text>
      <View style={styles.emptyState}>
        <Text style={styles.emptyText}>尚未建立投資組合</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#9CA3AF',
  },
});
