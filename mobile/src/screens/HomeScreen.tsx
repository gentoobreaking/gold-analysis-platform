import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, RefreshControl, ScrollView } from 'react-native';
import { api } from '../services/api';

interface PriceData {
  price: number;
  currency: string;
  change: number;
  change_pct: number;
}

interface Decision {
  action: string;
  confidence: number;
  reasons: string[];
}

export default function HomeScreen() {
  const [price, setPrice] = useState<PriceData | null>(null);
  const [decision, setDecision] = useState<Decision | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [priceData, decisionData] = await Promise.all([
        api.getPrice(),
        api.getDecision(),
      ]);
      setPrice(priceData);
      setDecision(decisionData);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const getActionColor = (action: string) => {
    switch (action) {
      case 'buy': return '#10B981';
      case 'sell': return '#EF4444';
      default: return '#6B7280';
    }
  };

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={<RefreshControl refreshing={loading} onRefresh={loadData} />}
    >
      {/* 價格卡片 */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>當前金價</Text>
        {price && (
          <>
            <Text style={styles.priceText}>
              {price.price.toLocaleString()} {price.currency}
            </Text>
            <Text style={[
              styles.changeText,
              { color: price.change >= 0 ? '#10B981' : '#EF4444' }
            ]}>
              {price.change >= 0 ? '+' : ''}{price.change.toFixed(2)} ({price.change_pct.toFixed(2)}%)
            </Text>
          </>
        )}
      </View>

      {/* 決策推薦 */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>交易建議</Text>
        {decision && (
          <>
            <View style={[styles.actionBadge, { backgroundColor: getActionColor(decision.action) }]}>
              <Text style={styles.actionText}>
                {decision.action.toUpperCase()}
              </Text>
            </View>
            <Text style={styles.confidenceText}>
              信心度: {decision.confidence}%
            </Text>
            {decision.reasons.map((reason, index) => (
              <Text key={index} style={styles.reasonText}>• {reason}</Text>
            ))}
          </>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
    padding: 16,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 12,
  },
  priceText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#111827',
  },
  changeText: {
    fontSize: 16,
    marginTop: 4,
  },
  actionBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  actionText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  confidenceText: {
    fontSize: 14,
    color: '#6B7280',
    marginTop: 12,
  },
  reasonText: {
    fontSize: 14,
    color: '#4B5563',
    marginTop: 4,
  },
});
